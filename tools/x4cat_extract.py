"""Minimaler X4-.cat/.dat-Extraktor (kein XRCatTool nötig).

Format (verifiziert an X4 9.00):
  .cat = Textindex, eine Zeile pro Datei: "<pfad> <größe> <mtime> <md5>"
  .dat = alle Dateien lückenlos in Indexreihenfolge; offset(i) = Summe der Größen 0..i-1

Aufruf:
  python -I tools/x4cat_extract.py <datei.cat> <zielordner> <muster> [<muster> ...]
  Muster: exakter Pfad oder Präfix mit '*' am Ende (z. B. 'voice-l044/10201/*').

Als Modul: find_latest_entry(game_dir, rel_path) und extract(cat_path, dest, patterns).
"""
import hashlib
import os
import sys


def parse_cat(cat_path):
    """Liest den Index und berechnet die Offsets. Rückgabe: Liste (pfad, offset, größe, md5)."""
    entries = []
    offset = 0
    with open(cat_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            # von rechts trennen: md5, mtime, größe; der Rest ist der Pfad (darf Leerzeichen enthalten)
            parts = line.rsplit(" ", 3)
            if len(parts) != 4:
                continue
            path, size, _mtime, md5 = parts
            size = int(size)
            entries.append((path, offset, size, md5))
            offset += size
    return entries


def _matches(path, patterns):
    for p in patterns:
        if p.endswith("*"):
            if path.startswith(p[:-1]):
                return True
        elif path == p:
            return True
    return False


def extract(cat_path, dest, patterns, verbose=True):
    """Extrahiert alle passenden Einträge und prüft die MD5. Rückgabe: Liste der geschriebenen Pfade."""
    dat_path = cat_path[:-4] + ".dat"
    out_paths = []
    with open(dat_path, "rb") as dat:
        for path, off, size, md5 in parse_cat(cat_path):
            if not _matches(path, patterns):
                continue
            dat.seek(off)
            data = dat.read(size)
            ok = hashlib.md5(data).hexdigest() == md5
            out = os.path.join(dest, path)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with open(out, "wb") as o:
                o.write(data)
            out_paths.append(out)
            if verbose:
                print(("OK " if ok else "MD5-MISMATCH ") + f"{path} ({size} B)")
    return out_paths


def find_latest_entry(game_dir, rel_path):
    """Sucht rel_path in 01.cat..09.cat; der höchste Katalog gewinnt (überschreibt niedrigere).
    Rückgabe: Pfad der .cat-Datei oder None."""
    found = None
    for n in range(1, 10):
        cat = os.path.join(game_dir, f"{n:02d}.cat")
        if not os.path.isfile(cat):
            continue
        with open(cat, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith(rel_path + " "):
                    found = cat
                    break
    return found


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(2)
    cat_path, dest, patterns = sys.argv[1], sys.argv[2], sys.argv[3:]
    n = len(extract(cat_path, dest, patterns))
    print(f"-- {n} Datei(en) extrahiert nach {dest}")


if __name__ == "__main__":
    main()
