"""Patch check: does the game contain Boso Ta lines that a variant's audio folder does not cover?

The mod redirects every `10201_*` entry to its own folder. A line id that exists in the game but not in that
folder plays as silence (the engine does not fall back). After every X4 patch or DLC, run this to see what is
missing, how many characters of text that is (for TTS), and whether the game's own file for a known id changed
(for the English variant, which is derived from the originals).

Usage:
  python -I tools/check_coverage.py --lang l049 --audio build/audio/will_dark_g6 [--game-dir "<X4 folder>"] [--tfile build/base/t/0001-l049.xml]
  python -I tools/check_coverage.py --lang l044 --audio build/audio/alien_mid_50_g4
Add --save-index to store the current catalog index of the page under build/index/, so the next run can report changed files.
"""
import argparse
import glob
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from x4cat_extract import parse_cat  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GAME_DIR = r"C:\Steam\steamapps\common\X4 Foundations"


def game_index(game_dir, lang, page="10201", context="normal"):
    """Map line id -> (size, md5) for voice-<lang>/<page>/<context>/ across base and DLC catalogs; later catalogs win."""
    prefix = f"voice-{lang}/{page}/{context}/"
    cats = sorted(glob.glob(os.path.join(game_dir, "0[1-9].cat"))) + sorted(glob.glob(os.path.join(game_dir, "extensions", "ego_dlc_*", "ext_0[1-9].cat")))
    idx = {}
    for cat in cats:
        for path, _off, size, md5 in parse_cat(cat):
            if path.startswith(prefix) and path.endswith(".ogg"):
                idx[path[len(prefix):-4]] = (size, md5)
    return idx


def load_texts(tfile, page="10201"):
    s = Path(tfile).read_text(encoding="utf-8", errors="replace")
    m = re.search(rf'<page id="{page}"[^>]*>(.*?)</page>', s, re.S)
    out = {}
    if m:
        for tid, txt in re.findall(r'<t id="(\d+)"[^>]*>(.*?)</t>', m.group(1), re.S):
            txt = re.sub(r"\([^)]*\)|\{\d+,\d+\}|\\033[A-Z]", "", txt)
            out[tid] = re.sub(r"\s+", " ", txt).strip()
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lang", required=True, choices=["l044", "l049"])
    ap.add_argument("--audio", required=True, help="folder with the variant's .ogg files")
    ap.add_argument("--game-dir", default=os.environ.get("X4_GAME_DIR", DEFAULT_GAME_DIR))
    ap.add_argument("--tfile", help="game text file for character counts (optional)")
    ap.add_argument("--save-index", action="store_true")
    args = ap.parse_args()

    idx = game_index(args.game_dir, args.lang)
    have = {p.stem for p in Path(args.audio).glob("*.ogg")}
    missing = sorted(i for i in idx if i not in have)
    extra = sorted(i for i in have if i not in idx)
    print(f"game: {len(idx)} lines for 10201/{args.lang}   mod folder: {len(have)} files   missing in mod: {len(missing)}   not in game any more: {len(extra)}")

    texts = load_texts(args.tfile) if args.tfile else {}
    if missing:
        chars = sum(len(texts.get(i) or texts.get(re.sub(r"[a-z]+$", "", i), "")) for i in missing)
        print(f"missing ids ({chars:,} characters of text to generate):")
        for i in missing[:40]:
            print(f"  {i}  {(texts.get(i) or texts.get(re.sub(r'[a-z]+$', '', i), ''))[:90]}")
        if len(missing) > 40:
            print(f"  ... and {len(missing) - 40} more")
    if extra:
        print("files in the mod that no longer exist in the game (harmless):", " ".join(extra[:20]))

    store = ROOT / "build" / "index" / f"10201_{args.lang}.json"
    if store.is_file():
        old = json.loads(store.read_text())
        changed = sorted(i for i in idx if i in old and tuple(old[i]) != idx[i])
        print(f"changed original files since last saved index: {len(changed)}" + (" -> " + " ".join(changed[:20]) if changed else ""))
    if args.save_index:
        store.parent.mkdir(parents=True, exist_ok=True)
        store.write_text(json.dumps(idx))
        print(f"index saved: {store}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
