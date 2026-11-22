# Maintenance: what an X4 patch or DLC can do to this mod

The mod has two moving parts: a small XML diff that redirects six sound entries, and a folder of audio files named after the game's line ids. Everything a patch can break falls into one of the cases below. The check for all of them takes a minute; `tools/check_coverage.py` and `tools/validate_mod.py` do most of the work.

## Case 1: Egosoft changes existing audio files

Re-recorded or re-encoded originals have **no effect**. The redirect never reads the originals; the mod's folder is the only source. Nothing to do, unless the *text* of a line changed as well. Then the German Will variant (spoken from the texts) says the old wording while the subtitle shows the new one. `check_coverage.py` reports changed original files when a saved index exists (`--save-index` after each update), and the changed ids can be regenerated with `tts-batch --files <ids>` after deleting their WAVs.

The English variant is derived from the originals. A changed original there means the processed copy is out of date; re-run `process_audio.py` for the changed ids.

## Case 2: New missions add new Boso Ta lines

New line ids appear as new files under `voice-l049/10201/normal/` (and the other contexts). The mod's folder does not have them, and **the engine plays silence** for a missing file; it does not fall back to the original. This is the one case that produces a visible defect: Boso Ta moves his mouth, the subtitle appears, nothing is heard.

Detection: `python -I tools/check_coverage.py --lang l049 --audio build/audio/will_dark_g6 --tfile build/base/t/0001-l049.xml` lists the missing ids and the number of characters to generate. Repair: run `tts-batch` (it skips existing files, so only the new lines cost credits), then `process_audio.py` for those ids, rebuild, re-upload with a change note. For English the same with `process_audio.py` on the new originals. Typical cost: a mission with 50 new lines is about 4,000 characters, a few cents.

New DLCs can also ship voice files inside their own catalogs. The coverage check scans `extensions/ego_dlc_*/ext_*.cat` as well as the base catalogs for that reason.

## Case 3: Egosoft restructures `sound_library.xml`

- Entries renamed or removed: the diff's selectors no longer match. X4 logs "No matching node", skips that patch and plays the original voice. Nothing crashes; the mod simply stops working for that entry. `validate_mod.py` extracts the new base file and reports exactly which selector fails.
- Entries gain new children (for example `<effects>`): no conflict, the diff only replaces `<sample>` and two attributes.
- `noocclusion` added by Egosoft to an entry: the mod's `<add type="@noocclusion">` would then fail for that entry ("attribute exists"). Switch that id to a `replace` in `config/variants.json` → `sound_attr_ops`.

## Case 4: Boso Ta gets a different voice page

Egosoft could give him his own page (the handoff thought that likely; it was not the case in 9.00). Then the mod patches the wrong speaker and Boso Ta is back to his original voice. Detection: the speak ids in `md/x4ep1_mentor_subscription.xml` and `md/story_boron.xml` must still resolve to files under `voice-l0xx/10201/`; the procedure is documented in `docs/phase0-findings.md`. Repair: change `boso_ta_ids` in the configuration to the new page's six entries and move the audio folder accordingly.

## Case 5: Game version checks and the Workshop

- `content.xml` does not pin a game version, so the mod keeps loading after patches. If Egosoft ever introduces a version gate, the Extensions menu will show it.
- Workshop subscribers receive updates automatically when the item is updated with `WorkshopTool update`. A Workshop update is also the way to ship repaired lines.
- The "modified" mark on saves is unaffected by any of this.

## After every patch: the three commands

```
python -I tools/validate_mod.py
python -I tools/check_coverage.py --lang l049 --audio build/audio/will_dark_g6 --tfile build/base/t/0001-l049.xml
python -I tools/check_coverage.py --lang l044 --audio build/audio/alien_mid_50_g4 --tfile build/base/t/0001-l044.xml
```

`validate_mod.py` extracts the patched game's `sound_library.xml` and proves the selectors still match. The two coverage runs list missing or changed lines per language. If all three print no errors, the mod is unaffected by the patch. Before the checks, refresh `build/base/t/` with the patched text files (`tools/x4cat_extract.py ... "t/0001-l049.xml"`), because new lines also bring new texts.
