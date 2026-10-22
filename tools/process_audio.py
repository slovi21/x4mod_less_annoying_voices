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

def alien_tank(k):
    """Alien im Tank mit skaliertem Effektanteil k (1.0 = Vollstärke). Tonhöhe bleibt eine Oktave tiefer.
    Skaliert: Frequenzverschiebung, Chorus-Anteil (decays) und -Tiefe (depths), Dämpfung (Tiefpass öffnet sich), Echo-Anteil."""
    shift = round(-70 * k)
    d1, d2 = round(0.4 * k, 3), round(0.32 * k, 3)
    p1, p2 = round(2 * k, 2), round(1.3 * k, 2)
    lowpass = round(2200 + (4500 - 2200) * (1 - k))
    echo = round(0.25 * k, 3)
    return ",".join([DEEP12, f"afreqshift=shift={shift}", f"chorus=0.6:0.9:50|60:{d1}|{d2}:0.25|0.4:{p1}|{p2}",
                     f"lowpass=f={lowpass}", f"aecho=0.9:0.3:25:{echo}"])


def alien_tank_tail(k):
    """Nur der Alien-Teil (ohne die Oktave), skaliert mit k – für Ketten, die die Oktave vorher schon haben."""
    return alien_tank(k).split(",", 1)[1]


# Mehrband-Kompressor: Band bis 1,3 kHz unangetastet, 1,3–5 kHz wird oberhalb von -30 dB kräftig gedrückt
# (piepsige Vokalspitzen), darüber moderat. Syntax: "attack,decay knee in/out-Punkte crossover | ..."
HICUT = ("mcompand='0.005,0.1 6 -90/-90,0/0 1300 | 0.003,0.05 6 -90/-90,-30/-30,-20/-34,0/-36 5000"
         " | 0.003,0.05 6 -90/-90,-30/-30,-15/-28,0/-30 22000'")

# Synthesizer-Split: erst Oktave, dann Teilung bei 1,3 kHz; unten 50 % Effekt, oben 100 % Effekt, zusammenmischen
SPLIT = ("asplit=2[lo][hi];[lo]lowpass=f=1300:p=2," + alien_tank_tail(0.5) + "[lo1];"
         "[hi]highpass=f=1300:p=2," + alien_tank_tail(1.0) + "[hi1];[lo1][hi1]amix=inputs=2:normalize=0")

def alien_tank_pitch(pitch):
    """Alien im Tank (100 %) mit frei wählbarem Rubberband-Faktor statt der festen Oktave."""
    return alien_tank(1.0).replace(DEEP12, rb(pitch))


# Mitten-Fokus für Verständlichkeit: Bandbegrenzung 220 Hz–5,5 kHz, Sprachbereich angehoben, sanfte Kompression
MID = ("highpass=f=220,lowpass=f=5500,equalizer=f=1400:t=q:w=1.0:g=4,equalizer=f=2800:t=q:w=1.2:g=2,"
       "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=150")

VARIANTS.update({
    "d12_alien_mid": ("Alien (−12 HT) + Mitten-Fokus: 220 Hz–5,5 kHz, +4 dB bei 1,4 kHz, +2 dB bei 2,8 kHz, sanfte Kompression",
                      ",".join([DEEP12, "afreqshift=shift=-70", "chorus=0.6:0.9:50|60:0.4|0.32:0.25|0.4:2|1.3", MID])),
})

VARIANTS.update({
    "tank_oct1.5": ("Alien im Tank, 1,5 Oktaven unter Original (-18 Halbtöne)", alien_tank_pitch(0.3536)),
    "tank_oct1.5_presence": ("Alien im Tank -18 Halbtöne, Tiefpass auf 3,2 kHz geöffnet, +4 dB um 1,8 kHz: setzt sich im Spielmix durch",
                             alien_tank_pitch(0.3536).replace("lowpass=f=2200", "lowpass=f=3200") + ",equalizer=f=1800:t=q:w=1.2:g=4"),
    "tank_oct2":   ("Alien im Tank, 2 Oktaven unter Original (-24 Halbtöne)", alien_tank_pitch(0.25)),
    "tank_oct3":   ("Alien im Tank, 3 Oktaven unter Original (-36 Halbtöne)", alien_tank_pitch(0.125)),
    "tank_oct4":   ("Alien im Tank, 4 Oktaven unter Original (-48 Halbtöne)", alien_tank_pitch(0.0625)),
})

VARIANTS.update({
    "alien_tank_70": ("Alien im Tank, Effekt auf 70 % (Tiefe unverändert -12 Halbtöne)", alien_tank(0.7)),
    "alien_tank_60": ("Alien im Tank, Effekt auf 60 %", alien_tank(0.6)),
    "alien_tank_50": ("Alien im Tank, Effekt auf 50 %", alien_tank(0.5)),
    # Runde 5 – nur die piepsigen Höhen behandeln
    "tank60_hicut":  ("Alien im Tank 60 % + Mehrband-Kompressor: Höhen 1,3–5 kHz nur bei Spitzen gedrückt", alien_tank(0.6) + "," + HICUT),
    "alien_hicut":   ("Alien im Tank 100 % + Mehrband-Kompressor auf die Höhen", alien_tank(1.0) + "," + HICUT),
    "deep12big_hicut": ("deep12big + Mehrband-Kompressor auf die Höhen", DEEP12 + "," + HICUT),
    "alien_split":   ("Synthesizer-Split: unten 50 % Effekt, oben (ab 1,3 kHz) 100 % Effekt", DEEP12 + "," + SPLIT),
})

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


def convert(ffmpeg, src, dst, af, wav, normalize, gain_db=0.0):
    """Eine Datei bearbeiten. Mit normalize: Durchgang 1 misst die Lautheit NACH der Filterkette,
    Durchgang 2 wendet loudnorm linear mit den Messwerten an (kein Pumpen).
    gain_db: zusätzliche Anhebung nach der Normalisierung, abgefangen von einem Spitzenbegrenzer bei -1 dBFS.
    Nötig, weil tiefe, gedämpfte Stimmen bei gleicher gemessener Lautheit subjektiv deutlich leiser wirken."""
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
    if gain_db:
        chain += f",volume={gain_db}dB,alimiter=limit=0.891:attack=5:release=60:level=false"
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
    ap.add_argument("--src-ext", default="ogg", help="Dateiendung der Quellen (ogg, oder wav aus pitch_flatten.py)")
    ap.add_argument("--gain-db", type=float, default=0.0, help="Anhebung in dB nach der Normalisierung (mit Begrenzer bei -1 dBFS)")
    args = ap.parse_args()

    if args.list or not args.variant:
        for k, (desc, af) in VARIANTS.items():
            print(f"{k:15s} {desc}\n{'':15s} af: {af}")
        return
    if not (args.src and args.dst):
        ap.error("--src und --dst sind nötig")

    ffmpeg = find_ffmpeg(args.ffmpeg)
    src_dir, dst_dir = Path(args.src), Path(args.dst)
    files = sorted(src_dir.glob(f"*.{args.src_ext}"))
    if args.files:
        wanted = set(args.files.split(","))
        files = [f for f in files if f.stem in wanted]
    if args.limit:
        files = files[: args.limit]
    if not files:
        sys.exit(f"FEHLER: keine Dateien in {src_dir}")
    desc, af = VARIANTS[args.variant]
    ext = ".wav" if args.wav else ".ogg"
    print(f"ffmpeg: {ffmpeg}\nVariante {args.variant}: {desc}\n{len(files)} Datei(en) -> {dst_dir}  (normalisieren: {not args.no_normalize}, Anhebung: {args.gain_db} dB)")

    errors = 0
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futs = [pool.submit(convert, ffmpeg, f, dst_dir / (f.stem + ext), af, args.wav, not args.no_normalize, args.gain_db) for f in files]
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
