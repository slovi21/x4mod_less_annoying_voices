# Quiz: Failure Modes & Edge Cases

Chapter: [13 · Failure Modes & Edge Cases](../13-failure-modes.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Apply]** Which of these causes does *not* make Boso Ta completely silent?

- A) The variant was installed without audio
- B) The install folder name differs from the `id` in the redirect
- C) The mod was swapped while X4 was running
- D) One sound id in `boso_ta_ids` is misspelled

**2. [Apply]** After a DLC update, most of Boso's lines play the mod voice but a few play nothing. Which tool tells you why, and what is the usual fix?

- A) `validate_mod.py`; fix the selectors
- B) `check_coverage.py` for that language; generate the missing ids into the variant's audio folder, then rebuild and reinstall
- C) `x4cat_extract.py` with `--verify`; re-extract the catalog
- D) `build_mod.py --only`; rebuild that variant

**3. [Apply]** The extension does not appear in the game's Extensions list at all. What is the classic cause, and which check would have caught it?

- A) An empty audio folder; caught by `install_mod.py`
- B) A malformed `content.xml`, typically a raw `&` from a hand edit; caught by `validate_mod.py`
- C) A missing `-logfile` launch option; caught by `check_coverage.py`
- D) A `ws_*` folder next to it; caught by `install_mod.py`

**4. [Apply]** After you finish testing with `-logfile debuglog.txt`, brief red text keeps appearing on screen. What is it?

- A) Errors from the mod's diff
- B) X4's own script errors, shown while `-logfile` is active; remove the option after testing
- C) Missing audio warnings for the five textless ids
- D) Signature warnings because the save is "modified"

**5. [Apply]** The first `WorkshopTool update` of a freshly created item fails with Steam error 9. What was found to be the cause?

- A) The version in `content.xml` was not raised
- B) `-preview` was passed; the same command without `-preview` succeeded
- C) The item was still hidden
- D) The payload was too large

**6. [Apply]** `install_mod.py will` stops with "keine Audiodateien", and afterwards the previously installed English variant is gone too. Explain both effects and how to recover.

**7. [Design]** Comm messages from Boso no longer sound like radio. Why, and what would restoring the effect take?

---

## Answers

**1. D.** A misspelled id makes that selector match nothing. The game logs it, skips the operation and plays the **original** voice for that entry (`tools/validate_mod.py:111-114`; `docs/MAINTENANCE.md:21`). A, B and C all leave a redirect that points at files that do not exist (`tools/install_mod.py:105-106`; `docs/phase0-findings.md:50`).

**2. B.** Single silent lines mean the game has ids the folder lacks, and that is exactly what the coverage check lists (`tools/check_coverage.py:66`, `:73-77`). A would find broken selectors, which would affect whole entries, not single lines. C: there is no `--verify` option. D does not touch audio (`tools/build_mod.py:7`).

**3. B.** An unescaped `&` makes X4 drop the extension silently. The builder escapes every value (`tools/build_mod.py:50`), and the validator reports a `content.xml` that is not well-formed (`tools/validate_mod.py:62-69`). A stops the install; it does not hide an installed extension. C and D do not affect the list.

**4. B.** This is recorded in the failure table (`book/13-failure-modes.md:18`). A would appear as "No matching node" in the log, not on screen. C would be silence. D is a log-only signature warning (`docs/phase0-findings.md:45`).

**5. B.** Recorded in `docs/RELEASE.md:13`. A causes a refusal for an unchanged version (`docs/RELEASE.md:35`). D is the cause of error 16 when *creating* an item (`docs/RELEASE.md:12`). C is unrelated.

**6.** The installer deletes every `bosota_*` folder first (`tools/install_mod.py:92-95`), and only then checks the new variant's audio folder and exits (`:107-110`). So the old variant is gone and nothing new is installed, and the game falls back to the original voice. Recover by producing the audio for `will_dark_g6` with its recipe (`config/variants.json:130`), then running the install again with X4 closed.

**7.** All six entries, including `10201_comm`, `10201_comm_npc` and `10201_comm_broadcast`, are redirected to the same processed `normal` folder (`tools/build_mod.py:29-35`). The comm recordings, which carry the radio colouring, are no longer read. Restoring it would need a second processed audio set for the comm context. The diff would then have to redirect the comm entries to that folder instead of to `normal`. That means changes to `build_diff`, the installer's target folder (`tools/install_mod.py:112`) and the coverage context (`tools/check_coverage.py:32`).
