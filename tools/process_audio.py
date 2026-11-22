"""Batch audio processing with ffmpeg for the Boso Ta voice variants.

Each variant is an ffmpeg filter chain. Pitch changes use Rubberband, so the tempo is unchanged. Every file is
normalised in two passes to the loudness of the original recordings (−22 LUFS); an optional gain with a limiter
follows, because dark voices need more level to cut through the game's mix.
Output: Ogg Vorbis, mono, 44.1 kHz like the originals, or WAV for listening samples.

Usage:
  python -I tools/process_audio.py --list
  python -I tools/process_audio.py --variant will_dark --src build/tts/will_de --src-ext wav --gain-db 6 --dst build/audio/will_dark_g6
  python -I tools/process_audio.py --variant alien_mid_50 --gain-db 4 --src <voice-l044/10201/normal> --dst build/audio/alien_mid_50_g4
         [--files id1,id2] [--limit N] [--wav] [--no-normalize] [--jobs 8] [--ffmpeg <path>]
ffmpeg is taken from PATH, else from %LOCALAPPDATA%\\Microsoft\\WinGet (package Gyan.FFmpeg), else --ffmpeg / FFMPEG.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")


def rb(pitch, formant="shifted"):
    """Rubberband pitch factor 2^(semitones/12): -4 = 0.7937, -6 = 0.7071, -12 = 0.5."""
    return f"rubberband=pitch={pitch}:formant={formant}:pitchq=quality"


# Mid-range focus for intelligibility: band 220 Hz–5.5 kHz, speech band raised, gentle compression
MID = ("highpass=f=220,lowpass=f=5500,equalizer=f=1400:t=q:w=1.0:g=4,equalizer=f=2800:t=q:w=1.2:g=2,"
       "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=150")


def alien_mid_scaled(k):
    """The 'alien with mid-range focus' chain at strength k (1.0 = German full strength).
    Scaled: depth (k octaves), frequency shift, chorus amount. The mid-range focus stays at full strength."""
    pitch = round(2 ** (-k), 4)
    shift = round(-70 * k)
    d1, d2 = round(0.4 * k, 3), round(0.32 * k, 3)
    p1, p2 = round(2 * k, 2), round(1.3 * k, 2)
    return ",".join([rb(pitch), f"afreqshift=shift={shift}", f"chorus=0.6:0.9:50|60:{d1}|{d2}:0.25|0.4:{p1}|{p2}", MID])


VARIANTS = {
    "d12_alien_mid": ("Alien, full strength: one octave down with shifted formants, frequency shift -70 Hz, chorus, mid-range focus "
                      "(German plan-B result, superseded by will_dark)", alien_mid_scaled(1.0)),
    "alien_mid_50":  ("Alien at half strength: -6 semitones, -35 Hz, half chorus, full mid-range focus (published English variant)",
                      alien_mid_scaled(0.5)),
    "will_dark":     ("Post-processing for text-to-speech output (ElevenLabs voice Will): -4 semitones with shifted formants, "
                      "+4 dB below 220 Hz, -4 dB above 4 kHz (published German variant)",
                      ",".join([rb(0.7937), "lowshelf=f=220:g=4", "highshelf=f=4000:g=-4"])),
}

LOUD = "loudnorm=I=-22:TP=-3:LRA=9"   # the original lines measure -21.6 … -22.0 LUFS, true peak -5 dBTP


def find_ffmpeg(explicit=None):
    cand = explicit or os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    if cand and Path(cand).is_file():
        return cand
    local = os.environ.get("LOCALAPPDATA", "")
    for pat in (f"{local}/Microsoft/WinGet/Packages/*FFmpeg*/*/bin/ffmpeg.exe",
                f"{local}/Microsoft/WinGet/Links/ffmpeg.exe", "C:/ffmpeg/bin/ffmpeg.exe"):
        hits = glob.glob(pat)
        if hits:
            return hits[0]
    sys.exit("ERROR: ffmpeg not found. Pass --ffmpeg <path> or set FFMPEG.")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def convert(ffmpeg, src, dst, af, wav, normalize, gain_db=0.0):
    """Process one file. With normalize: pass 1 measures loudness after the chain, pass 2 applies loudnorm linearly
    with the measured values (no pumping). gain_db: extra gain after normalisation, limited at -1 dBFS."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    chain = af
    if normalize:
        r1 = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(src), "-af", f"{af},{LOUD}:print_format=json", "-f", "null", "-"])
        m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r1.stderr, re.S)
        if not m:
            return src.name, 1, "loudnorm measurement failed: " + r1.stderr[-200:]
        j = json.loads(m.group(0))
        chain = (f"{af},{LOUD}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
                 f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    if gain_db:
        chain += f",volume={gain_db}dB,alimiter=limit=0.891:attack=5:release=60:level=false"
    codec = ["-c:a", "pcm_s16le"] if wav else ["-c:a", "libvorbis", "-q:a", "3"]
    r = run([ffmpeg, "-y", "-loglevel", "error", "-i", str(src), "-af", chain, "-ac", "1", "-ar", "44100", *codec, str(dst)])
    return src.name, r.returncode, r.stderr.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="show variants")
    ap.add_argument("--variant", choices=sorted(VARIANTS))
    ap.add_argument("--src", help="source folder")
    ap.add_argument("--dst", help="target folder")
    ap.add_argument("--src-ext", default="ogg", help="source extension (ogg for game files, wav for TTS output)")
    ap.add_argument("--files", help="only these line ids (comma separated, without extension)")
    ap.add_argument("--limit", type=int, help="only the first N files")
    ap.add_argument("--wav", action="store_true", help="write WAV instead of Ogg (listening samples)")
    ap.add_argument("--no-normalize", action="store_true")
    ap.add_argument("--gain-db", type=float, default=0.0, help="gain after normalisation, with limiter at -1 dBFS")
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 4) - 1))
    ap.add_argument("--ffmpeg")
    args = ap.parse_args()

    if args.list or not args.variant:
        for k, (desc, af) in VARIANTS.items():
            print(f"{k:15s} {desc}\n{'':15s} af: {af}")
        return
    if not (args.src and args.dst):
        ap.error("--src and --dst are required")

    ffmpeg = find_ffmpeg(args.ffmpeg)
    src_dir, dst_dir = Path(args.src), Path(args.dst)
    files = sorted(src_dir.glob(f"*.{args.src_ext}"))
    if args.files:
        wanted = set(args.files.split(","))
        files = [f for f in files if f.stem in wanted]
    if args.limit:
        files = files[: args.limit]
    if not files:
        sys.exit(f"ERROR: no files in {src_dir}")
    desc, af = VARIANTS[args.variant]
    ext = ".wav" if args.wav else ".ogg"
    print(f"ffmpeg: {ffmpeg}\nvariant {args.variant}: {desc}\n{len(files)} file(s) -> {dst_dir}  (normalise: {not args.no_normalize}, gain: {args.gain_db} dB)")

    errors = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futs = [pool.submit(convert, ffmpeg, f, dst_dir / (f.stem + ext), af, args.wav, not args.no_normalize, args.gain_db) for f in files]
        for i, fut in enumerate(as_completed(futs), 1):
            name, rc, err = fut.result()
            if rc != 0:
                errors += 1
                print(f"ERROR {name}: {err[:200]}")
            if i % 200 == 0 or i == len(files):
                print(f"  {i}/{len(files)}")
    print(f"done: {len(files) - errors} ok, {errors} errors")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
