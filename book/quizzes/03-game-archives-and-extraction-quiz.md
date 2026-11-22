# Quiz: Game Archives & Extraction

Chapter: [3 · Game Archives & Extraction](../03-game-archives-and-extraction.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Recall]** How does `x4cat_extract.py` find where a file's bytes start inside `NN.dat`?

- A) The offset is the third field of the file's line in `NN.cat`
- B) It adds up the sizes of all earlier entries in index order
- C) It scans `NN.dat` for a block whose MD5 matches the index entry
- D) Files are aligned to 4 KB blocks, so the offset is the index position times 4096

**2. [Design]** Why does `parse_cat` split each index line with `rsplit(" ", 3)` rather than `split(" ")`?

**3. [Apply]** Suppose one line in the middle of a `.cat` has only three fields. What does `parse_cat` do?

- A) It raises an exception and extraction stops
- B) It skips the line, and offsets for later entries stay correct because each entry carries its own offset
- C) It skips the line without a message; that file's size is never added, so every later offset is too small
- D) It treats the missing field as size 0 and continues

**4. [Apply]** You call `x4cat_extract.py 03.cat build\orig "*.ogg"`. What is extracted?

- A) Every `.ogg` file in the catalog
- B) Nothing; only a trailing `*` is a prefix wildcard, and any other pattern must equal a path exactly
- C) Only the first `.ogg` file
- D) The CLI rejects the pattern and prints the docstring

**5. [Recall]** What happens when the MD5 of an extracted file does not match the index?

- A) The file is skipped and the CLI exits with an error
- B) The file is written anyway; `MD5-MISMATCH` is printed only in verbose mode, so `validate_mod.py` would not show it
- C) The extractor retries the read up to five times
- D) The file is written to a `.bad` name so it cannot be used by mistake

**6. [Apply]** Assume `libraries/sound_library.xml` appears in both `01.cat` and `08.cat`, and every DLC ships its own `sound_library.xml` diff in `ext_03.cat`. Which file does `validate_mod.py` use as its base?

- A) The copy from `01.cat`, because the base game is mounted first
- B) The copy from `08.cat`, because the highest base catalog that contains the path wins
- C) The DLC diffs merged onto the `08.cat` copy
- D) Whichever catalog `Select-String` lists first

**7. [Apply]** After a patch, some of Boso Ta's German lines are in `03.cat` and new or changed ones are in a later base catalog. How do you get the effective set into `build\orig`, and why does that order work?

---

## Answers

**1. B.** `offset` starts at 0 and grows by each entry's size (`tools/x4cat_extract.py:21`, `:33-34`). A is wrong: the four fields are path, size, mtime and MD5 (`:31`). C and D describe mechanisms the format does not have. The data is packed back to back with no padding.

**2.** Paths may contain spaces. The last three fields (size, mtime, MD5) never do, so splitting at most three times from the right leaves the full path intact as the first part (`tools/x4cat_extract.py:27-28`).

**3. C.** A line that does not split into four parts is skipped with `continue` (`tools/x4cat_extract.py:29-30`). Because `offset += size` runs only for appended entries (`:34`), the skipped file's bytes are never counted. A is wrong: there is no exception. B is wrong: offsets are computed, not stored. D is wrong: no default size is used.

**4. B.** `_matches` treats a pattern as a prefix only when it ends in `*`, and otherwise compares the whole path (`tools/x4cat_extract.py:38-45`). `"*.ogg"` equals no path, so nothing is written and the CLI reports 0 files (`:90-91`). A assumes shell-style globbing. D is wrong: the docstring is printed only when there are fewer than three arguments (`:86-88`).

**5. B.** `ok` is computed but the file is still written (`tools/x4cat_extract.py:58-62`), and the message is printed only when `verbose` is true (`:64-65`). The validator calls `extract(..., verbose=False)` (`tools/validate_mod.py:37`). A, C and D describe handling that does not exist.

**6. B.** `find_latest_entry` scans `01.cat` to `09.cat` in order and keeps the last match (`tools/x4cat_extract.py:69-82`). `load_base` extracts from that catalog (`tools/validate_mod.py:34-37`). A has the override order backwards (`docs/phase0-findings.md:9`). C is wrong: DLC catalogs are never read here. That is safe only because no DLC diff touches `10201_*` (`docs/phase0-findings.md:20`). D confuses a manual search with the code.

**7.** Find every catalog that holds `voice-l049/10201/normal/` (for example with `Select-String … -List`). Run the extractor once per catalog in ascending order, all into the same destination. Each run opens its output with `"wb"` and overwrites an existing file (`tools/x4cat_extract.py:61-62`), so the later catalog's version wins. That matches the game's own override order (`docs/phase0-findings.md:9`). Running `extract` on a single catalog returns only that catalog's version.
