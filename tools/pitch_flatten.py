"""Tonhöhen-Spanne stauchen (Praat „Change gender" über parselmouth) – Vorstufe vor process_audio.py.

Die Intonationsspitzen (hohe Stimmlaute) werden zur Mitte gezogen: Faktor 0.4 heißt, Ausschläge um den
Median werden auf 40 % gestaucht. Der Median selbst bleibt (new_median=0) oder wird gesetzt. Formanten und
Tempo bleiben unverändert; die Oktave macht danach weiterhin Rubberband in process_audio.py.

Läuft in der abgetrennten Umgebung:  build\\venv\\Scripts\\python.exe -I tools\\pitch_flatten.py ...
Aufruf: ... --src <ordner mit .ogg> --dst <zielordner> [--files id1,id2] [--range 0.4] [--median 0] [--floor 75] [--ceiling 800] [--jobs 4]
Ausgabe: WAV (44,1 kHz, Mono) mit denselben Dateinamen; process_audio.py liest .ogg – daher danach mit --src-ext wav aufrufen
oder die WAVs vorher nach .ogg wandeln. Einfacher: process_audio.py akzeptiert .wav-Quellen über --src-ext.
"""
import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import numpy as np
import soundfile as sf
import parselmouth
from parselmouth.praat import call

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")


def flatten_one(src, dst, rng, median, floor, ceiling):
    try:
        data, sr = sf.read(str(src), dtype="float64", always_2d=True)
        mono = data.mean(axis=1)
        snd = parselmouth.Sound(mono, sampling_frequency=sr)
        # Change gender: pitch floor, pitch ceiling, formant shift ratio, new pitch median (0 = behalten),
        # pitch range factor, duration factor
        out = call(snd, "Change gender", floor, ceiling, 1.0, median, rng, 1.0)
        y = out.values[0]
        peak = float(np.max(np.abs(y))) or 1.0
        if peak > 0.99:
            y = y / peak * 0.99
        dst.parent.mkdir(parents=True, exist_ok=True)
        sf.write(str(dst), y, int(out.sampling_frequency), subtype="PCM_16")
        return src.name, None
    except Exception as e:  # noqa: BLE001
        return src.name, repr(e)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--files")
    ap.add_argument("--range", type=float, default=0.4, help="Pitch range factor (1.0 = unverändert)")
    ap.add_argument("--median", type=float, default=0.0, help="neuer Median in Hz, 0 = behalten")
    ap.add_argument("--floor", type=float, default=75.0)
    ap.add_argument("--ceiling", type=float, default=800.0)
    ap.add_argument("--jobs", type=int, default=max(2, (os.cpu_count() or 4) - 1))
    args = ap.parse_args()

    files = sorted(Path(args.src).glob("*.ogg")) + sorted(Path(args.src).glob("*.wav"))
    if args.files:
        wanted = set(args.files.split(","))
        files = [f for f in files if f.stem in wanted]
    if not files:
        sys.exit(f"FEHLER: keine Dateien in {args.src}")
    dst = Path(args.dst)
    print(f"{len(files)} Datei(en): range={args.range} median={args.median} -> {dst}")
    errors = 0
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        futs = [pool.submit(flatten_one, f, dst / (f.stem + ".wav"), args.range, args.median, args.floor, args.ceiling) for f in files]
        for i, fut in enumerate(as_completed(futs), 1):
            name, err = fut.result()
            if err:
                errors += 1
                print(f"FEHLER {name}: {err[:200]}")
            if i % 200 == 0 or i == len(files):
                print(f"  {i}/{len(files)}")
    print(f"fertig: {len(files) - errors} OK, {errors} Fehler")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
