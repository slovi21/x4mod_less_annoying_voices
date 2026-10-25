# 3 · Game Archives & Extraction (`tools/x4cat_extract.py`)

> **What you'll be able to answer after this chapter:** the exact on-disk format of X4 catalogs (data), how the extractor locates and verifies a file (flow, contracts), which catalog wins when several contain a path (rationale), and what happens on corrupt or missing data (failure).

## Why it exists

Everything starts with files that only exist inside the game's archives: Boso Ta's recordings, the text files, and `sound_library.xml` itself. Egosoft ships `XRCatTool` for this, but the format is simple enough that 95 lines of standard-library Python replace it, which keeps the pipeline dependency-free and scriptable (`tools/x4cat_extract.py:1-12`).

## The format

- `NN.cat` is plain text, one line per file: `<path> <size> <mtime> <md5>`. Paths may contain spaces, so the line is split **from the right** into four parts (`tools/x4cat_extract.py:28`).
- `NN.dat` is all files back to back, in index order, no padding, no compression. The offset of entry *i* is the sum of the sizes of entries 0…*i*−1 (`tools/x4cat_extract.py:21,33-34`).

```python
for line in f:
    line = line.rstrip("\n")
    if not line:
        continue
    parts = line.rsplit(" ", 3)          # → md5, mtime, size from the right; rest is the path
    if len(parts) != 4:
        continue                         # → malformed lines are skipped silently
    path, size, _mtime, md5 = parts
    size = int(size)
    entries.append((path, offset, size, md5))
    offset += size                       # → running offset = start of the next file in .dat
```
(`tools/x4cat_extract.py:23-34`)

## Public surface

| Function | Signature | Contract |
|---|---|---|
| `parse_cat(cat_path)` | → `list[(path, offset, size, md5)]` | Index order preserved; offsets computed. Malformed lines are skipped, which would shift every later offset (inference: never observed with Egosoft catalogs). |
| `extract(cat_path, dest, patterns, verbose=True)` | → `list[str]` of written paths | Opens `<cat without .cat>.dat` (`:50`), writes each match under `dest/<path>`, creating folders. MD5 is checked and reported but **a mismatch still writes the file** (`:58,65`). |
| `find_latest_entry(game_dir, rel_path)` | → path of the winning `.cat` or `None` | Scans `01.cat`…`09.cat` in order and remembers the **last** one containing the path, i.e. the overriding one (`:69-82`). Does not look at DLC catalogs. |
| `main()` (CLI) | `x4cat_extract.py <cat> <dest> <pattern…>` | Fewer than three arguments prints the docstring and exits 2 (`:86-88`). |

**Patterns** (`_matches`, `:38-45`): an exact path, or a prefix ending in `*`. There is no other globbing: `voice-l049/10201/normal/*` works, `*.ogg` does not.

## Traced example

`python -I tools/x4cat_extract.py "...\03.cat" build\orig "voice-l049/10201/normal/30201131.ogg"`:

1. `parse_cat` reads `03.cat`; suppose the matching line is the 4,812th and the sizes before it sum to 1,204,559,872. The entry becomes `("voice-l049/10201/normal/30201131.ogg", 1204559872, 41233, "a3f…")`.
2. `extract` seeks to 1,204,559,872 in `03.dat`, reads 41,233 bytes, hashes them, prints `OK voice-l049/... (41233 B)` and writes `build\orig\voice-l049\10201\normal\30201131.ogg`.
3. `main` prints `-- 1 Datei(en) extrahiert nach build\orig`.

(Offset and size are illustrative; the mechanism is exact.)

### Where things are in X4 9.00

| Content | Catalog |
|---|---|
| `voice-l049/10201/normal/*` and `voice-l044/10201/normal/*` (all of Boso Ta's lines, both languages) | `03.cat` |
| `t/0001-l044.xml`, `t/0001-l049.xml` | `09.cat` |
| `libraries/sound_library.xml` | `08.cat` |

Patches can move or add files to other catalogs. The index is plain text, so `Select-String -Path "<game>\0*.cat" -Pattern "^voice-l049/10201/normal/" -List` (PowerShell) shows every catalog that holds at least one matching line; extract from each, in ascending order, into the same destination so later catalogs overwrite earlier ones.

## Collaborators

- `validate_mod.py` uses `find_latest_entry` + `extract` to fetch the current `sound_library.xml` into `build/base/` on every run (`tools/validate_mod.py:32-40`).
- `check_coverage.py` uses `parse_cat` to index line ids across base and DLC catalogs (`tools/check_coverage.py:32-41`).
- Humans call the CLI to fetch originals and text files.

## Errors & edge cases

- **Missing `.dat`:** `open()` raises `FileNotFoundError`; no handling.
- **MD5 mismatch:** reported as `MD5-MISMATCH` only when `verbose=True`; the file is still written. `validate_mod.py` calls `extract(..., verbose=False)` (`tools/validate_mod.py:37`), so a corrupt `sound_library.xml` would pass silently there. Treat any reported mismatch as a corrupt game installation.
- **Output language:** the CLI prints German and does not reconfigure stdout to UTF-8, unlike the other tools.
- **Path in several catalogs:** `extract` on one catalog returns that catalog's version. To get the effective file, either use `find_latest_entry` or run the extractor over all catalogs in order, letting later writes overwrite earlier ones (that is how the originals were extracted during development).
- **`_sig.cat` files:** signature catalogs follow the same naming; callers must not pass them. `check_coverage.py` avoids them by globbing `ext_0[1-9].cat`, which does not match `ext_01_sig.cat`.
- **Encoding:** the index is read as UTF-8 with `errors="replace"`, so odd bytes cannot crash parsing.

## Performance

`parse_cat` reads the whole index (the largest, `03.cat`, is 32 MB) on every call; `check_coverage.py` parses every catalog once per run. Extraction is a single seek and read per file. Good enough for thousands of files.

## Where to look

`tools/x4cat_extract.py`, `docs/phase0-findings.md` ("Catalog format").

## Open questions

- Whether X4 itself tolerates malformed index lines the same way is unknown; it has not mattered in practice.

→ Check your understanding: [quizzes/03-game-archives-and-extraction-quiz.md](quizzes/03-game-archives-and-extraction-quiz.md)
