"""Kopiert GENAU EINE gebaute Variante in den extensions-Ordner des Spiels.

Vorher werden dort alle Ordner entfernt, deren Name mit 'bosota_' beginnt – es darf immer nur eine
Variante aktiv sein (alle patchen dieselben Sound-IDs). Andere Mods werden nicht angefasst.
Verweigert den Austausch, solange X4 läuft (das laufende Spiel würde sonst gelöschte Dateien suchen).

Kopiert die XML-Dateien aus dist/<id>/ und die Audiodateien aus build/audio/<audio_variant>/ nach
extensions/<id>/voice/10201/normal/.

Aufruf: python -I tools/install_mod.py will|alien|alien_en|alien_ws|alien_en_ws [--game-dir "<X4-Ordner>"] [--force]
        python -I tools/install_mod.py --remove          (alle bosota_* entfernen)
Spielordner: --game-dir, sonst Umgebungsvariable X4_GAME_DIR, sonst C:\\Steam\\steamapps\\common\\X4 Foundations
"""
import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")  # Umlaute auch in Git Bash / Pipes korrekt

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GAME_DIR = r"C:\Steam\steamapps\common\X4 Foundations"
PREFIX = "bosota_"   # alle Varianten dieses Projekts (bosota_warm_*, bosota_voice_*) – es darf nur eine aktiv sein
CFG = json.loads((ROOT / "config" / "variants.json").read_text(encoding="utf-8"))


def _clear_readonly_and_retry(func, path, _exc):
    """rmtree-Fehlerbehandlung: Schreibschutz entfernen und den fehlgeschlagenen Aufruf wiederholen.

    Falle: OneDrive setzt auf Ordner im Repo das ReadOnly-Attribut; shutil.copytree überträgt es ins
    Spielverzeichnis, und Windows verweigert rmdir auf schreibgeschützte Ordner (WinError 5).
    """
    os.chmod(path, stat.S_IWRITE)
    func(path)


def clear_readonly_tree(root):
    """Entfernt das ReadOnly-Attribut von allen Ordnern unter root (Dateien bleiben unverändert)."""
    for dirpath, dirnames, _files in os.walk(root):
        os.chmod(dirpath, stat.S_IWRITE)


def game_running():
    """True, wenn X4.exe läuft. Mod-Wechsel bei laufendem Spiel führen zu stummen Stimmen: Das Spiel hat
    den alten Diff geladen und findet die gelöschten Audiodateien nicht mehr (passiert am 2026-10-22)."""
    try:
        # tasklist schreibt in der OEM-Codepage (deutsch: cp850); nur nach ASCII "X4.exe" suchen, Rest tolerant dekodieren
        raw = subprocess.run(["tasklist", "/FI", "IMAGENAME eq X4.exe", "/NH"], capture_output=True, timeout=10).stdout
    except Exception:  # noqa: BLE001 – kein tasklist (z. B. nicht Windows): nicht blockieren
        return False
    return b"X4.exe" in (raw or b"")


def rmtree_retry(path, tries=5, delay=0.5):
    """Löscht einen Ordner samt Inhalt; räumt Schreibschutz weg und wiederholt bei verzögerter Handle-Freigabe."""
    handler = {"onexc": _clear_readonly_and_retry} if sys.version_info >= (3, 12) else {"onerror": _clear_readonly_and_retry}
    for attempt in range(tries):
        try:
            shutil.rmtree(path, **handler)
            return
        except FileNotFoundError:
            return
        except PermissionError as e:
            if attempt == tries - 1:
                sys.exit(f"FEHLER: {path} konnte nicht entfernt werden ({e}). Ordner von Hand löschen und erneut versuchen.")
            time.sleep(delay)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("variant", nargs="?", choices=sorted(CFG["variants"]))
    ap.add_argument("--game-dir", default=os.environ.get("X4_GAME_DIR", DEFAULT_GAME_DIR))
    ap.add_argument("--remove", action="store_true", help="nur entfernen, nichts installieren")
    ap.add_argument("--force", action="store_true", help="auch bei laufendem X4 ausführen (nicht empfohlen)")
    args = ap.parse_args()
    if not args.variant and not args.remove:
        ap.error("Variante (" + "|".join(sorted(CFG["variants"])) + ") oder --remove angeben")

    ext_root = Path(args.game_dir) / "extensions"
    if not ext_root.is_dir():
        sys.exit(f"FEHLER: {ext_root} existiert nicht – Spielordner prüfen (--game-dir / X4_GAME_DIR)")
    if Path(args.game_dir).resolve() == Path(DEFAULT_GAME_DIR).resolve() and not args.force and game_running():
        sys.exit("FEHLER: X4 läuft. Erst das Spiel beenden, dann installieren – sonst sucht das laufende Spiel gelöschte Dateien und Boso ist stumm. (--force übergeht die Prüfung.)")

    for d in ext_root.iterdir():
        if d.is_dir() and d.name.startswith(PREFIX):
            rmtree_retry(d)
            print(f"entfernt:    {d}")

    if args.remove:
        return
    v = CFG["variants"][args.variant]
    mod_id = v["id"]
    src = ROOT / "dist" / mod_id
    if not src.is_dir():
        sys.exit(f"FEHLER: {src} fehlt – zuerst: python -I tools/build_mod.py")
    dst = ext_root / mod_id
    # Every variant redirects to its own audio folder, so the audio must always be copied. Checked before anything
    # is written: a variant installed without audio would make Boso silent in the game.
    audio = ROOT / "build" / "audio" / v["audio_variant"]
    files = sorted(audio.glob("*.ogg")) if audio.is_dir() else []
    if not files:
        sys.exit(f"FEHLER: keine Audiodateien in {audio} – zuerst das Rezept aus config/variants.json (audio_recipe) ausführen")
    shutil.copytree(src, dst)
    voice_dir = dst / "voice" / "10201" / "normal"
    voice_dir.mkdir(parents=True)
    for f in files:
        shutil.copyfile(f, voice_dir / f.name)
    print(f"Audio:       {len(files)} Dateien nach {voice_dir}")
    clear_readonly_tree(dst)  # sonst erbt das Ziel den OneDrive-Schreibschutz der Quelle
    print(f"installiert: {dst}")
    print("Im Spiel: Hauptmenü > Erweiterungen > Eintrag muss sichtbar und aktiv sein.")


if __name__ == "__main__":
    main()
