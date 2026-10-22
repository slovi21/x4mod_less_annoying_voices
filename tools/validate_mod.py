"""Prüft gebaute Extensions gegen die ECHTE sound_library.xml des Spiels – ohne das Spiel zu starten.

Prüfungen:
  1. content.xml ist wohlgeformtes XML (ein rohes '&' lässt X4 die Mod stillschweigend verwerfen).
  2. libraries/sound_library.xml ist ein wohlgeformter <diff>.
  3. Jeder XPath-Selektor trifft genau einen Knoten der Basisdatei ("No matching node" wäre ein stiller Fehler).
  4. Keine doppelten Kindelemente (sound_library.xsd: <effects> und seine Kinder sind xs:all, maxOccurs=1).
  5. Wertebereiche: pitch > 0, filter frequency in [0, 1].
Zum Schluss wird das Ergebnis der Patch-Anwendung je Sound-ID ausgegeben.

Aufruf: python -I tools/validate_mod.py [--game-dir "<X4-Ordner>"] [dist/<id> ...]
Spielordner: --game-dir, sonst Umgebungsvariable X4_GAME_DIR, sonst C:\\Steam\\steamapps\\common\\X4 Foundations
"""
import argparse
import copy
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Umlaute auch in Git Bash / Pipes korrekt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from x4cat_extract import extract, find_latest_entry  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GAME_DIR = r"C:\Steam\steamapps\common\X4 Foundations"
REL = "libraries/sound_library.xml"


def load_base(game_dir):
    cache = ROOT / "build" / "base"
    cat = find_latest_entry(game_dir, REL)
    if not cat:
        sys.exit(f"FEHLER: {REL} in keinem Katalog unter {game_dir} gefunden")
    extract(cat, str(cache), [REL], verbose=False)
    path = cache / REL
    print(f"Basis: {path} (aus {os.path.basename(cat)})")
    return ET.parse(path).getroot()


def et_xpath(sel):
    """Egosoft-XPath -> ElementTree-XPath (relativ zur Wurzel <soundlibrary>)."""
    if sel.startswith("/soundlibrary"):
        return "." + sel[len("/soundlibrary"):]
    if sel.startswith("//"):
        return "." + sel
    return sel


def parent_map_of(root):
    return {child: parent for parent in root.iter() for child in parent}


def validate(ext_dir, base_root):
    errors, warnings = [], []
    root = copy.deepcopy(base_root)
    print(f"\n=== {ext_dir} ===")

    # 1. content.xml
    try:
        c = ET.parse(ext_dir / "content.xml").getroot()
        cid = c.get("id")
        if cid != ext_dir.name:
            warnings.append(f"content.xml id='{cid}' weicht vom Ordnernamen ab (erlaubt, aber unüblich)")
        print(f"content.xml OK: id={cid}, version={c.get('version')}, save={c.get('save')}")
    except ET.ParseError as e:
        errors.append(f"content.xml nicht wohlgeformt: {e}")

    # 2. Diff laden
    try:
        diff = ET.parse(ext_dir / "libraries" / "sound_library.xml").getroot()
    except ET.ParseError as e:
        errors.append(f"sound_library.xml nicht wohlgeformt: {e}")
        return errors, warnings
    if diff.tag != "diff":
        errors.append(f"Wurzelelement ist <{diff.tag}>, erwartet <diff>")

    # 3./4. Operationen anwenden
    touched = []
    for op in diff:
        sel = op.get("sel", "")
        targets = root.findall(et_xpath(sel))
        if len(targets) == 0:
            errors.append(f"No matching node: {sel}")
            continue
        if len(targets) > 1:
            warnings.append(f"{len(targets)} Treffer für {sel} (Patch wirkt auf alle)")
        for t in targets:
            if op.tag == "add":
                for child in op:
                    if t.find(child.tag) is not None:
                        errors.append(f"{sel}: <{child.tag}> existiert bereits – xs:all erlaubt nur eines")
                    t.append(copy.deepcopy(child))
            elif op.tag == "replace":
                p = parent_map_of(root).get(t)
                if p is None:
                    errors.append(f"replace auf Wurzel nicht unterstützt: {sel}")
                else:
                    idx = list(p).index(t)
                    p.remove(t)
                    for i, child in enumerate(op):
                        p.insert(idx + i, copy.deepcopy(child))
            elif op.tag == "remove":
                parent_map_of(root)[t].remove(t)
            else:
                errors.append(f"unbekannte Operation <{op.tag}>")
        if "@id='" in sel:
            touched.append(sel.split("@id='")[1].split("'")[0])

        # 5. Wertebereiche
        for el in op.iter():
            if el.tag == "pitch":
                for a in ("start", "end"):
                    if float(el.get(a, "1")) <= 0:
                        errors.append(f"{sel}: pitch {a}={el.get(a)} muss > 0 sein")
            if el.tag == "filter" and el.get("frequency") is not None:
                f = float(el.get("frequency"))
                if not 0 <= f <= 1:
                    errors.append(f"{sel}: filter frequency={f} außerhalb [0, 1]")

    # Ergebnis je Sound-ID zeigen
    for sid in dict.fromkeys(touched):
        node = root.find(f"./sound[@id='{sid}']")
        if node is None:
            continue
        eff = node.find("effects")
        desc = (node.get("description") or "")[:48]
        if eff is None:
            kids = "KEINE"
        else:
            kids = ", ".join(
                e.tag + "(" + " ".join(f"{k}={val}" for k, val in e.attrib.items()) + ")" for e in eff
            )
        print(f"  {sid:24s} [{desc}] -> effects: {kids}")
    return errors, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--game-dir", default=os.environ.get("X4_GAME_DIR", DEFAULT_GAME_DIR))
    ap.add_argument("ext_dirs", nargs="*", help="Extension-Ordner; Standard: alle unter dist/")
    args = ap.parse_args()

    base = load_base(args.game_dir)
    dirs = [Path(d) for d in args.ext_dirs] or sorted(p for p in (ROOT / "dist").iterdir() if p.is_dir())
    total_err = 0
    for d in dirs:
        errs, warns = validate(d, base)
        for w in warns:
            print(f"  WARNUNG: {w}")
        for e in errs:
            print(f"  FEHLER:  {e}")
        total_err += len(errs)
        print("  -> " + ("OK" if not errs else f"{len(errs)} Fehler"))
    print(f"\nGesamt: {total_err} Fehler in {len(dirs)} Extension(s)")
    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
