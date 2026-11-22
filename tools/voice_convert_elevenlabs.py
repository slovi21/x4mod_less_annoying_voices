"""Text-to-speech generation of Boso Ta's lines with ElevenLabs.

Every line is spoken from the game text (page 10201 of the text file holds each line under the id of its audio
file). The WAVs then go through tools/process_audio.py (--src-ext wav) for colouring, loudness and gain.

API key: environment variable ELEVENLABS_API_KEY, or the file %USERPROFILE%\\.elevenlabs_key (plain text,
one line). The key is never printed.

Usage (run inside build/venv, which has requests, numpy and soundfile):
  build\\venv\\Scripts\\python.exe -I tools\\voice_convert_elevenlabs.py quota
  build\\venv\\Scripts\\python.exe -I tools\\voice_convert_elevenlabs.py voices [--filter male]
  build\\venv\\Scripts\\python.exe -I tools\\voice_convert_elevenlabs.py tts --voice <voice_id> --text "<text>" --out <file.wav> [--model eleven_v4_turbo]
  build\\venv\\Scripts\\python.exe -I tools\\voice_convert_elevenlabs.py tts-batch --voice <voice_id> --tfile build/base/t/0001-l049.xml
         --ids-from <folder with the original .ogg> --dst build/tts/<name> [--model eleven_v4_turbo] [--page 10201]
         [--files id1,id2] [--limit N] [--dry-run] [--stability 0.5] [--similarity 0.75] [--style 0.0] [--jobs 2]
tts-batch skips WAVs that already exist, so an interrupted run can simply be restarted.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from process_audio import find_ffmpeg  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

API = "https://api.elevenlabs.io/v1"


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not key:
        f = Path(os.environ.get("USERPROFILE", str(Path.home()))) / ".elevenlabs_key"
        if f.is_file():
            key = f.read_text(encoding="ascii", errors="ignore").strip()
    if not key:
        sys.exit("ERROR: no API key. Set ELEVENLABS_API_KEY or create %USERPROFILE%\\.elevenlabs_key")
    return key


def headers():
    return {"xi-api-key": api_key()}


def cmd_quota(_args):
    r = requests.get(f"{API}/user/subscription", headers=headers(), timeout=30)
    r.raise_for_status()
    j = r.json()
    used, limit = j.get("character_count", 0), j.get("character_limit", 0)
    print(f"plan: {j.get('tier')}  credits used: {used} of {limit}  remaining: {limit - used}")
    print(f"voice changer available: {j.get('can_use_speech_to_speech', '?')}  resets: {time.strftime('%Y-%m-%d', time.gmtime(j.get('next_character_count_reset_unix', 0)))}")


def cmd_voices(args):
    r = requests.get(f"{API}/voices", headers=headers(), timeout=30)
    r.raise_for_status()
    voices = r.json().get("voices", [])
    flt = (args.filter or "").lower()
    rows = []
    for v in voices:
        lab = v.get("labels") or {}
        line = f"{v['name']:14s} {v['voice_id']}  {v.get('category','?'):9s} {lab.get('gender','?'):7s} {lab.get('age','?'):12s} {lab.get('accent','?'):12s} {lab.get('description') or lab.get('descriptive') or '':14s} {lab.get('use_case') or ''}"
        if not flt or flt in line.lower():
            rows.append(line)
    print(f"{len(rows)} of {len(voices)} voices")
    print(f"{'name':14s} {'voice_id':20s}  {'category':9s} {'gender':7s} {'age':12s} {'accent':12s} {'character':14s} use case")
    for line in sorted(rows):
        print(line)


def tts_one(ffmpeg, voice_id, text, dst, model, stability, similarity, style, output_format="mp3_44100_128"):
    """Text-to-speech for one line; returns a status string. Output is WAV 44.1 kHz mono."""
    settings = {"stability": stability, "similarity_boost": similarity, "style": style, "use_speaker_boost": True}
    for attempt in range(5):
        r = requests.post(
            f"{API}/text-to-speech/{voice_id}",
            headers={**headers(), "Content-Type": "application/json"},
            params={"output_format": output_format},
            json={"text": text, "model_id": model, "voice_settings": settings},
            timeout=180,
        )
        if r.status_code == 429 or r.status_code >= 500:
            time.sleep(3 * (attempt + 1))
            continue
        if r.status_code != 200:
            return f"HTTP {r.status_code}: {r.text[:160]}"
        break
    else:
        return "gave up after retries"
    dst.parent.mkdir(parents=True, exist_ok=True)
    p = subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", "pipe:0", "-ar", "44100", "-ac", "1", str(dst)], input=r.content, capture_output=True)
    return "ok" if p.returncode == 0 else "ffmpeg: " + p.stderr.decode("utf-8", "replace")[-160:]


def cmd_tts(args):
    """Speak one text with one voice (test samples). Batch TTS of all lines is a separate step."""
    ffmpeg = find_ffmpeg(args.ffmpeg)
    status = tts_one(ffmpeg, args.voice, args.text, Path(args.out), args.model, args.stability, args.similarity, args.style)
    print(status)
    sys.exit(0 if status == "ok" else 1)


def load_texts(tfile, page="10201"):
    """Texts of one page of a game text file, keyed by line id; stage directions and markup removed."""
    import re
    s = Path(tfile).read_text(encoding="utf-8", errors="replace")
    m = re.search(rf'<page id="{page}"[^>]*>(.*?)</page>', s, re.S)
    if not m:
        sys.exit(f"ERROR: page {page} not found in {tfile}")
    out = {}
    for tid, txt in re.findall(r'<t id="(\d+)"[^>]*>(.*?)</t>', m.group(1), re.S):
        txt = re.sub(r"\([^)]*\)", "", txt)      # stage directions such as "(eager; interjects)"
        txt = re.sub(r"\{\d+,\d+\}", "", txt)    # references to other text entries
        txt = re.sub(r"\\033[A-Z]", "", txt)     # colour codes
        txt = re.sub(r"\s+", " ", txt).strip()
        out[tid] = txt
    return out


def cmd_tts_batch(args):
    """Speak every line of a voice folder with one voice. Line ids come from the original audio file names,
    texts from the game's text file (page 10201). Resumable: existing WAVs are skipped."""
    import re
    texts = load_texts(args.tfile, args.page)
    ids = sorted(p.stem for p in Path(args.ids_from).glob("*.ogg"))
    plan, missing = [], []
    for i in ids:
        base = re.sub(r"[a-z]+$", "", i)        # alternate takes like 30201430fp share the text of 30201430
        txt = texts.get(i) or texts.get(base)
        (plan if txt else missing).append((i, txt))
    if args.files:
        wanted = set(args.files.split(","))
        plan = [p for p in plan if p[0] in wanted]
    if args.limit:
        plan = plan[: args.limit]
    dst = Path(args.dst)
    todo = [(i, t) for i, t in plan if not (dst / f"{i}.wav").exists()]
    chars = sum(len(t) for _, t in todo)
    print(f"{len(ids)} line ids, {len(plan)} with text, {len(missing)} without text, {len(todo)} to generate, {chars:,} characters")
    if missing:
        print("without text:", " ".join(i for i, _ in missing[:12]), "..." if len(missing) > 12 else "")
    if args.dry_run or not todo:
        return
    ffmpeg = find_ffmpeg(args.ffmpeg)
    ok = failed = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futs = {pool.submit(tts_one, ffmpeg, args.voice, t, dst / f"{i}.wav", args.model, args.stability, args.similarity, args.style): i for i, t in todo}
        for n, fut in enumerate(as_completed(futs), 1):
            status = fut.result()
            if status == "ok":
                ok += 1
            else:
                failed += 1
                print(f"FAILED {futs[fut]}: {status[:160]}")
            if n % 100 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)}")
    print(f"done: {ok} generated, {failed} failed")
    sys.exit(1 if failed else 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("quota")
    pb = sub.add_parser("tts-batch", help="speak all lines of a voice folder with one voice")
    pb.add_argument("--voice", required=True)
    pb.add_argument("--tfile", required=True, help="game text file, e.g. build/base/t/0001-l049.xml")
    pb.add_argument("--page", default="10201")
    pb.add_argument("--ids-from", required=True, help="folder with the original .ogg files (line ids)")
    pb.add_argument("--dst", required=True)
    pb.add_argument("--files")
    pb.add_argument("--limit", type=int)
    pb.add_argument("--dry-run", action="store_true", help="only count lines and characters")
    pb.add_argument("--model", default="eleven_multilingual_v2")
    pb.add_argument("--stability", type=float, default=0.5)
    pb.add_argument("--similarity", type=float, default=0.75)
    pb.add_argument("--style", type=float, default=0.0)
    pb.add_argument("--jobs", type=int, default=2)
    pb.add_argument("--ffmpeg")
    pt = sub.add_parser("tts", help="speak one text with one voice into a WAV file")
    pt.add_argument("--voice", required=True)
    pt.add_argument("--text", required=True)
    pt.add_argument("--out", required=True)
    pt.add_argument("--model", default="eleven_multilingual_v2")
    pt.add_argument("--stability", type=float, default=0.5)
    pt.add_argument("--similarity", type=float, default=0.75)
    pt.add_argument("--style", type=float, default=0.0)
    pt.add_argument("--ffmpeg")
    pv = sub.add_parser("voices")
    pv.add_argument("--filter", help="substring filter on the printed line, e.g. male, female, deep, german")
    args = ap.parse_args()
    {"quota": cmd_quota, "voices": cmd_voices, "tts": cmd_tts, "tts-batch": cmd_tts_batch}[args.cmd](args)


if __name__ == "__main__":
    main()
