"""Erzeugt aus config/variants.json die installierbaren Extension-Ordner unter dist/.

Je Variante entstehen:
  dist/<id>/content.xml                  Mod-Metadaten (Egosoft-Format)
  dist/<id>/libraries/sound_library.xml  XML-Diff: hängt <effects> (pitch, filter, optional reverb) an die Sound-IDs

Aufruf: python -I tools/build_mod.py [--only de|en|test]
"""
import argparse
import datetime
import json
import sys
from pathlib import Path
from xml.sax.saxutils import quoteattr

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Umlaute auch in Git Bash / Pipes korrekt

ROOT = Path(__file__).resolve().parent.parent
CFG_PATH = ROOT / "config" / "variants.json"
DIST = ROOT / "dist"


def effect_children(v, indent):
    """Die Effekt-Elemente einer Variante als XML-Zeilen (Reihenfolge egal: xs:all im Schema)."""
    pad = " " * indent
    pitch = v["pitch"]
    lines = [
        f'{pad}<pitch start="{pitch}" end="{pitch}" steps="1"/>',
        f'{pad}<filter mode="lowpass" frequency="{v["lowpass"]}"/>',
    ]
    r = v.get("reverb")
    if r:
        lines.append(
            f"{pad}<reverb room={quoteattr(r['room'])} roomsize=\"{r['roomsize']}\" "
            f"drymix=\"{r['drymix']}\" density=\"{r['density']}\"/>"
        )
    return lines


def build_redirect_diff(v, cfg):
    """Audio-Variante: alle Boso-Ta-Einträge auf den Audio-Ordner der Extension umleiten.
    Nachgewiesen (Diagnose v6): die Engine lädt extensions\\<id>\\voice\\10201\\normal\\<zeile>.ogg wörtlich,
    ohne Sprachsuffix. Alle Kontexte (auch comm) nutzen denselben bearbeiteten normal-Satz."""
    target = f"extensions\\{v['id']}\\voice\\10201\\normal"
    out = [
        '<?xml version="1.0" encoding="utf-8"?>',
        "<diff>",
        f"  <!-- generiert von tools/build_mod.py – Audio-Variante {v['id']} (Bearbeitung: {v['audio_variant']}) -->",
        "  <!-- Audiodateien: tools/install_mod.py kopiert build/audio/<variante>/*.ogg nach voice/10201/normal/ -->",
    ]
    for sound_id in cfg["boso_ta_ids"]:
        out.append(f"  <replace sel=\"/soundlibrary/sound[@id='{sound_id}']/sample\">")
        out.append(f'    <sample start="{target}"/>')
        out.append("  </replace>")
    out.append("</diff>")
    return "\n".join(out) + "\n"


def build_diff(v, cfg):
    if v.get("kind") == "audio":
        return build_redirect_diff(v, cfg)
    ids = dict(cfg["boso_ta_ids"])
    if v.get("include_betty"):
        ids.update(cfg["betty_test_ids"])
    reverb_flag = "ja" if v.get("reverb") else "nein"
    out = [
        '<?xml version="1.0" encoding="utf-8"?>',
        "<diff>",
        f"  <!-- generiert von tools/build_mod.py aus config/variants.json – Variante {v['id']} -->",
        f"  <!-- pitch={v['pitch']} lowpass={v['lowpass']} reverb={reverb_flag} -->",
    ]
    for sound_id, has_effects in ids.items():
        sel = f"/soundlibrary/sound[@id='{sound_id}']"
        if has_effects:
            # Eintrag besitzt schon <effects>: Kinder dort einfügen (ein zweites <effects> wäre ein Schemaverstoß)
            out.append(f'  <add sel="{sel}/effects">')
            out += effect_children(v, 4)
            out.append("  </add>")
        else:
            out.append(f'  <add sel="{sel}">')
            out.append("    <effects>")
            out += effect_children(v, 6)
            out.append("    </effects>")
            out.append("  </add>")
    out.append("</diff>")
    return "\n".join(out) + "\n"


def build_content(v, cfg):
    today = datetime.date.today().isoformat()
    q = quoteattr  # XML-sichere Attributwerte: &, <, > und Anführungszeichen werden maskiert
    return (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        f"<content id={q(v['id'])} name={q(v['name_en'])} description={q(v['desc_en'])} "
        f"author={q(cfg['author'])} version={q(cfg['version'])} date={q(today)} enabled=\"1\" save=\"0\">\n"
        f"  <text language=\"44\" name={q(v['name_en'])} description={q(v['desc_en'])}/>\n"
        f"  <text language=\"49\" name={q(v['name_de'])} description={q(v['desc_de'])}/>\n"
        "</content>\n"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="nur diese Variante bauen (Schlüssel aus config/variants.json)")
    args = ap.parse_args()

    cfg = json.loads(CFG_PATH.read_text(encoding="utf-8"))
    for key, v in cfg["variants"].items():
        if args.only and key != args.only:
            continue
        target = DIST / v["id"]
        # Dateien in place überschreiben statt den Ordner zu löschen: OneDrive sperrt frisch
        # angelegte Ordner kurzzeitig, shutil.rmtree läuft dann auf "Zugriff verweigert".
        (target / "libraries").mkdir(parents=True, exist_ok=True)
        (target / "content.xml").write_text(build_content(v, cfg), encoding="utf-8")
        (target / "libraries" / "sound_library.xml").write_text(build_diff(v, cfg), encoding="utf-8")
        if v.get("kind") == "audio":
            audio = ROOT / "build" / "audio" / v["audio_variant"]
            n_audio = len(list(audio.glob("*.ogg"))) if audio.is_dir() else 0
            hint = "" if n_audio else "  ACHTUNG: noch keine Audiodateien – tools/process_audio.py ausführen"
            print(f"gebaut: {target.relative_to(ROOT)}  (Audio-Umleitung, {len(cfg['boso_ta_ids'])} Sound-IDs, {n_audio} ogg in build/audio/{v['audio_variant']}){hint}")
        else:
            n_ids = len(cfg["boso_ta_ids"]) + (len(cfg["betty_test_ids"]) if v.get("include_betty") else 0)
            print(f"gebaut: {target.relative_to(ROOT)}  (pitch={v['pitch']}, lowpass={v['lowpass']}, {n_ids} Sound-IDs)")


if __name__ == "__main__":
    main()
