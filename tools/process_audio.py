"""Batch-Audiobearbeitung mit ffmpeg für Boso Tas Zeilen (Plan B: eigene Audiodateien per Umleitung).

Jede Variante ist eine ffmpeg-Filterkette. Tonhöhe wird mit Rubberband geändert, also OHNE Tempoänderung
(Mundbewegung und Dialoglänge bleiben erhalten). Standardmäßig wird jede Datei in zwei Durchgängen auf die
Lautheit des Originals normalisiert (-22 LUFS, gemessen an Boso Tas Originalzeilen), damit Varianten
vergleichbar bleiben und im Spiel nicht lauter oder leiser als andere NPCs sind.
Ausgabe: Ogg Vorbis, Mono, 44,1 kHz wie das Original, oder WAV für Hörproben in Windows.

Aufruf:
  python -I tools/process_audio.py --list
  python -I tools/process_audio.py --variant deep12big --src <ordner mit .ogg> --dst <zielordner>
         [--files 30201131,30201057] [--limit N] [--wav] [--no-normalize] [--jobs 8] [--ffmpeg <pfad>]
ffmpeg wird im PATH gesucht, sonst unter %LOCALAPPDATA%\\Microsoft\\WinGet (Paket Gyan.FFmpeg); Pfad auch per --ffmpeg oder Umgebungsvariable FFMPEG.
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

# Halbton-Faktoren 2^(n/12):  -6 = 0.7071, -7 = 0.6674, -12 = 0.5, -14 = 0.4454, -16 = 0.3969, -19 = 0.3350
def rb(pitch, formant="shifted"):
    return f"rubberband=pitch={pitch}:formant={formant}:pitchq=quality"

DEEP12 = rb(0.5)
ROBOT = "afftfilt=real='hypot(re,im)*sin(0)':imag='hypot(re,im)*cos(0)':win_size=512:overlap=0.75"
WHISPER = "afftfilt=real='hypot(re,im)*cos((random(0)*2-1)*2*PI)':imag='hypot(re,im)*sin((random(1)*2-1)*2*PI)':win_size=128:overlap=0.8"
BAND = "highpass=f=200,lowpass=f=4500"
RINGMOD = "aeval=exprs='val(0)*sin(2*PI*t*35)'"          # echte Ringmodulation mit 35 Hz (Dalek/Zylonen-Buzz)
CHOIR = ("asplit=2[a][b];[a]" + rb(0.5) + "[a1];[b]" + rb(0.335) + "[b1];[a1][b1]amix=inputs=2:normalize=0")  # Oktave + Oktave-und-Quinte übereinander

VARIANTS = {
    # Runde 1
    "deep7":      ("-7 Halbtöne, Formanten erhalten: dieselbe Person, nur tief", rb(0.6674, "preserved")),
    "deep7big":   ("-7 Halbtöne, Formanten mitverschoben: größer, dunkler", rb(0.6674)),
    "deep12big":  ("-12 Halbtöne (Oktave), Formanten mitverschoben – Favorit Runde 1", DEEP12),
    "computer":   ("Computerstimme hart: -6 Halbtöne, Robot-Phasenfilter, Bandbegrenzung", ",".join([rb(0.7071), ROBOT, BAND])),
    "computer2":  ("Computerstimme weich: -6 Halbtöne, 45-Hz-Modulation, Bitcrush, Bandbegrenzung",
                   ",".join([rb(0.7071), "tremolo=f=45:d=0.7", "acrusher=bits=10:mode=log:mix=0.25", BAND])),
    # Runde 2 – alles auf Basis Oktave tiefer oder tiefer
    "deep14big":  ("-14 Halbtöne, Formanten mitverschoben: noch tiefer als deep12big", rb(0.4454)),
    "deep16big":  ("-16 Halbtöne, Formanten mitverschoben: Grenze, wird dumpf", rb(0.3969)),
    "d12_computer":   ("deep12big + harter Robot-Phasenfilter + Bandbegrenzung", ",".join([DEEP12, ROBOT, BAND])),
    "d12_computer2":  ("deep12big + 45-Hz-Modulation + Bitcrush + Bandbegrenzung", ",".join([DEEP12, "tremolo=f=45:d=0.7", "acrusher=bits=10:mode=log:mix=0.25", BAND])),
    "d12_ringmod":    ("deep12big + Ringmodulation 35 Hz (Dalek/Zylonen) + Bandbegrenzung", ",".join([DEEP12, RINGMOD, BAND])),
    "d12_choir":      ("zwei tiefe Stimmen übereinander (Oktave + Oktave-und-Quinte): wuchtig, Monster/Gott", CHOIR),
    "d12_alien":      ("deep12big + Frequenzverschiebung -70 Hz + Chorus: metallisch, unharmonisch, fremd",
                       ",".join([DEEP12, "afreqshift=shift=-70", "chorus=0.6:0.9:50|60:0.4|0.32:0.25|0.4:2|1.3"])),
    "d12_whisper":    ("deep12big + Flüster-Phasenfilter: heiser-hauchig, Tonhöhe fast weg", ",".join([DEEP12, WHISPER])),
    "d12_underwater": ("deep12big + Tiefpass 900 Hz + kurzes Echo: dumpf wie unter Wasser (Boron im Tank)",
                       ",".join([DEEP12, "lowpass=f=900", "aecho=0.8:0.6:40|80:0.3|0.2"])),
    # Runde 3 – Feinvarianten des Favoriten d12_alien
    "alien_soft":  ("Alien sanfter: Verschiebung -45 Hz, leichterer Chorus",
                    ",".join([DEEP12, "afreqshift=shift=-45", "chorus=0.7:0.9:45:0.3:0.25:1.5"])),
    "alien_deep":  ("Alien tiefer: -14 Halbtöne, Verschiebung -80 Hz, Chorus",
                    ",".join([rb(0.4454), "afreqshift=shift=-80", "chorus=0.6:0.9:50|60:0.4|0.32:0.25|0.4:2|1.3"])),
    "alien_tank":  ("Alien im Tank: d12_alien + Tiefpass 2,2 kHz + sehr kurzes, leises Echo statt Hall",
                    ",".join([DEEP12, "afreqshift=shift=-70", "chorus=0.6:0.9:50|60:0.4|0.32:0.25|0.4:2|1.3",
                              "lowpass=f=2200", "aecho=0.9:0.3:25:0.25"])),
}

LOUD = "loudnorm=I=-22:TP=-3:LRA=9"   # Zielwerte: Originalzeilen messen -21.6 … -22.0 LUFS, True Peak -5 dBTP


def find_ffmpeg(explicit=None):
    cand = explicit or os.environ.get("FFMPEG") or shutil.which("ffmpeg")
    if cand and Path(cand).is_file():
        return cand
    local = os.environ.get("LOCALAPPDATA", "")
    for pat in (
        f"{local}/Microsoft/WinGet/Packages/*FFmpeg*/*/bin/ffmpeg.exe",
        f"{local}/Microsoft/WinGet/Links/ffmpeg.exe",
        "C:/ffmpeg/bin/ffmpeg.exe",
    ):
        hits = glob.glob(pat)
        if hits:
            return hits[0]
    sys.exit("FEHLER: ffmpeg nicht gefunden. --ffmpeg <pfad> oder Umgebungsvariable FFMPEG setzen.")


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def convert(ffmpeg, src, dst, af, wav, normalize):
    """Eine Datei bearbeiten. Mit normalize: Durchgang 1 misst die Lautheit NACH der Filterkette,
    Durchgang 2 wendet loudnorm linear mit den Messwerten an (kein Pumpen)."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    chain = af
    if normalize:
        r1 = run([ffmpeg, "-hide_banner", "-nostats", "-i", str(src), "-af", f"{af},{LOUD}:print_format=json", "-f", "null", "-"])
        m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r1.stderr, re.S)
        if not m:
            return src.name, 1, "loudnorm-Messung fehlgeschlagen: " + r1.stderr[-200:]
        j = json.loads(m.group(0))
        chain = (f"{af},{LOUD}:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
                 f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
    codec = ["-c:a", "pcm_s16le"] if wav else ["-c:a", "libvorbis", "-q:a", "3"]
    r = run([ffmpeg, "-y", "-loglevel", "error", "-i", str(src), "-af", chain, "-ac", "1", "-ar", "44100", *codec, str(dst)])
    return src.name, r.returncode, r.stderr.strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--list", action="store_true", help="Varianten anzeigen")
    ap.add_argument("--variant", choices=sorted(VARIANTS))
    ap.add_argument("--src", help="Quellordner mit .ogg")
    ap.add_argument("--dst", help="Zielordner")
    ap.add_argument("--files", help="nur diese Zeilen-IDs (kommagetrennt, ohne .ogg)")
    ap.add_argument("--limit", type=int, help="nur die ersten N Dateien")
    ap.add_argument("--wav", action="store_true", help="WAV statt Ogg schreiben (Hörproben)")
    ap.add_argument("--no-normalize", action="store_true", help="keine Lautheitsnormalisierung")
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 4) - 1))
    ap.add_argument("--ffmpeg")
    args = ap.parse_args()

    if args.list or not args.variant:
        for k, (desc, af) in VARIANTS.items():
            print(f"{k:15s} {desc}\n{'':15s} af: {af}")
        return
    if not (args.src and args.dst):
        ap.error("--src und --dst sind nötig")

    ffmpeg = find_ffmpeg(args.ffmpeg)
    src_dir, dst_dir = Path(args.src), Path(args.dst)
    files = sorted(src_dir.glob("*.ogg"))
    if args.files:
        wanted = set(args.files.split(","))
        files = [f for f in files if f.stem in wanted]
    if args.limit:
        files = files[: args.limit]
    if not files:
        sys.exit(f"FEHLER: keine Dateien in {src_dir}")
    desc, af = VARIANTS[args.variant]
    ext = ".wav" if args.wav else ".ogg"
    print(f"ffmpeg: {ffmpeg}\nVariante {args.variant}: {desc}\n{len(files)} Datei(en) -> {dst_dir}  (normalisieren: {not args.no_normalize})")

    errors = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futs = [pool.submit(convert, ffmpeg, f, dst_dir / (f.stem + ext), af, args.wav, not args.no_normalize) for f in files]
        for i, fut in enumerate(as_completed(futs), 1):
            name, rc, err = fut.result()
            if rc != 0:
                errors += 1
                print(f"FEHLER {name}: {err[:200]}")
            if i % 200 == 0 or i == len(files):
                print(f"  {i}/{len(files)}")
    print(f"fertig: {len(files) - errors} OK, {errors} Fehler")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
