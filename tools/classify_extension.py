"""Checks an X4 extension against the proposed "cosmetic extension" allowlist v1.

Reference implementation for docs/proposals/COSMETIC_EXTENSIONS.md. The rules in classify() are the
normative list; the document explains them. The verdict says whether an extension WOULD qualify under the
proposal. It is not an Egosoft statement and changes nothing about how the game treats the extension.

Fail-closed: anything that cannot be classified with certainty counts against the extension – unknown file
types, catalog lines that do not parse, a .dat without its .cat, a .cat whose .dat does not match the index,
paths with '..', drive letters or characters Windows does not allow, linked folders.

Usage: python -I tools/classify_extension.py <extension folder> [<extension folder> ...]
Exit code: 0 every folder qualifies, 1 at least one does not (or only with candidate classes), 2 usage error.
"""
import os
import re
import sys
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AUDIO_EXT = {"ogg", "wav"}
DOC_EXT = {"txt", "pdf", "md"}
CORE = {"metadata", "documentation", "audio"}
CANDIDATES = {"candidate_text", "candidate_texture"}
WINDOWS_FORBIDDEN = set('<>:"|?*')
# "<path> <size> <mtime> <md5>"; the path may contain spaces (same format as tools/x4cat_extract.py)
CAT_LINE = re.compile(r"^(?P<path>.+) (?P<size>\d+) (?P<mtime>-?\d+) (?P<md5>[0-9a-fA-F]{32})$")


class UsageError(Exception):
    pass


def normalize(rel):
    """The path as the engine resolves it on Windows: '/', lowercase, trailing dots and spaces stripped from
    every component. None if it is not a plain relative path."""
    raw = rel.replace("\\", "/")
    if raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
        return None
    parts = []
    for part in raw.split("/"):
        if part in ("", "."):
            continue
        if any(c in WINDOWS_FORBIDDEN or ord(c) < 32 for c in part):
            return None
        part = part.rstrip(". ")
        if not part:                       # '..', '...', ' ' – would leave the folder or resolve unpredictably
            return None
        parts.append(part.lower())
    return "/".join(parts) if parts else None


def classify(path):
    """Class of one normalized path. Order matters: code beats media, and everything unlisted is 'other'."""
    if path is None:
        return "invalid"
    parts = path.split("/")
    ext = parts[-1].rsplit(".", 1)[1] if "." in parts[-1] else ""
    if path == "content.xml":
        return "metadata"
    if len(parts) == 1 and ext in DOC_EXT:
        return "documentation"
    if parts[0] == "ui" or ext == "lua":
        return "ui_code"                   # Lua can change game state; X4 already has Protected UI Mode for it
    if path == "libraries/sound_library.xml" or ext in AUDIO_EXT:
        return "audio"                     # verified for this mod in X4 9.00 (docs/phase0-findings.md)
    if len(parts) == 2 and parts[0] == "t" and ext == "xml":
        return "candidate_text"            # scripts read text pages too – Egosoft's call
    if ext == "dds" and not path.startswith("assets/fx/"):
        return "candidate_texture"         # textures can still reveal things (alpha) – Egosoft's call
    return "other"                         # gameplay or unknown


def _is_link(path):
    return os.path.islink(path) or getattr(os.path, "isjunction", lambda _p: False)(path)


def scan_catalog(cat, label, siblings):
    """Classifies every entry of a .cat index. siblings: lowercase name -> real name of the files next to it."""
    items, total = [], 0
    try:
        text = cat.read_bytes().decode("utf-8")
    except UnicodeDecodeError:
        return [(f"{label}: not UTF-8", "invalid")]
    for n, line in enumerate(text.split("\n"), 1):
        line = line.removesuffix("\r")
        if not line:
            continue
        m = CAT_LINE.match(line)
        if not m:
            items.append((f"{label}: line {n} does not parse", "invalid"))
            continue
        total += int(m["size"])
        items.append((f"{label} -> {m['path']}", classify(normalize(m["path"]))))
    dat_name = siblings.get(cat.name.lower()[:-4] + ".dat")
    if dat_name is None:
        items.append((f"{label}: .dat missing", "invalid"))
    elif (cat.parent / dat_name).stat().st_size != total:
        items.append((f"{label}: .dat size does not match the index", "invalid"))
    return items


def scan_extension(ext_dir):
    """Returns [(label, class)] for every loose file and every catalog entry of the extension."""
    ext_dir = Path(ext_dir)
    if not ext_dir.is_dir() or "content.xml" not in {f.lower() for f in os.listdir(ext_dir)}:
        raise UsageError(f"{ext_dir}: no content.xml - not an extension folder")
    items = []
    for dirpath, dirnames, filenames in os.walk(ext_dir):
        here = Path(dirpath)
        for d in list(dirnames):
            if _is_link(here / d):
                items.append(((here / d).relative_to(ext_dir).as_posix() + "/ (linked folder)", "invalid"))
                dirnames.remove(d)
        siblings = {f.lower(): f for f in filenames}
        for f in filenames:
            rel = (here / f).relative_to(ext_dir).as_posix()
            low = f.lower()
            if low.endswith(".cat"):
                items.extend(scan_catalog(here / f, rel, siblings))
            elif low.endswith(".dat"):
                if low[:-4] + ".cat" not in siblings:
                    items.append((f"{rel} (no matching .cat)", "invalid"))
            else:
                items.append((rel, classify(normalize(rel))))
    return items


def verdict(items):
    """('qualifies' | 'candidates' | 'fails', text)."""
    classes = {c for _, c in items}
    if not classes - {"metadata", "documentation"}:
        return "fails", "does not qualify: no content files found (wrong folder?)"
    if classes <= CORE:
        return "qualifies", "would qualify under the proposed allowlist v1"
    if classes <= CORE | CANDIDATES:
        return "candidates", "would qualify only if Egosoft accepts the candidate classes"
    return "fails", "does not qualify under the proposed allowlist v1"


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    worst = 0
    for arg in argv:
        try:
            items = scan_extension(arg)
        except (UsageError, OSError) as e:
            print(f"ERROR: {e}")
            return 2
        result, text = verdict(items)
        print(f"\n=== {arg} ===")
        for cls, n in sorted(Counter(c for _, c in items).items()):
            print(f"  {cls:<18} {n}")
        flagged = [(label, c) for label, c in items if c not in CORE]
        for label, c in flagged[:20]:
            print(f"  [{c}] {label}")
        if len(flagged) > 20:
            print(f"  ... and {len(flagged) - 20} more")
        print(f"verdict: {text} - not an Egosoft statement")
        worst = max(worst, 0 if result == "qualifies" else 1)
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
