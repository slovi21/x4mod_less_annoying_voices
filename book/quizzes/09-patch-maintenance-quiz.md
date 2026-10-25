# Quiz: Patch Maintenance

Chapter: [9 · Patch Maintenance](../09-patch-maintenance.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Recall]** A patch adds new Boso Ta lines. What does a player with the mod hear for them?

- A) The original recording, because the engine falls back when the mod folder lacks a file
- B) Silence; his mouth moves and the subtitle shows, because every request goes to the mod folder and there is no fallback
- C) The nearest existing line by id
- D) The game crashes when it cannot open the file

**2. [Apply]** `X4_GAME_DIR` points at a folder that is not the X4 installation. You run `check_coverage.py --lang l049 --audio build/audio/will_dark_g6`. What is the result?

- A) An error "no catalog found", exit code 1
- B) "game: 0 lines … missing in mod: 0", exit code 0, so it looks like a pass
- C) Every file in the mod folder counts as missing
- D) A traceback from `parse_cat`

**3. [Recall]** Which change does `check_coverage.py` *not* detect?

- A) New line ids in a DLC catalog
- B) A changed text whose audio file is unchanged
- C) New line ids in context `normal` of a base catalog
- D) A changed original audio file, provided a baseline index was saved

**4. [Apply]** You never ran `--save-index`. Egosoft re-encodes 30 English originals in a patch. What does the coverage check say about them?

- A) "changed original files since last saved index: 30"
- B) Nothing; without `build/index/10201_l044.json` the "changed" line is silently left out
- C) It counts them as missing
- D) It saves a baseline and reports them on the same run

**5. [Recall]** Why does the coverage check look only at the `normal` context, although the game has `comm`, `comm_npc` and `comm_broadcast` copies of every line?

- A) The other contexts never get new lines
- B) After the redirect all six sound entries read the mod's `normal` folder, so only ids in `normal` must exist there
- C) Only `normal` is in the base catalogs; the other contexts are in DLCs
- D) To save time; checking all contexts would be too slow

**6. [Apply]** After a patch you skip re-extracting the originals and go straight to the German and English repair commands. `check_coverage.py` lists 12 missing ids. What happens next, and why?

**7. [Apply]** A patch changes the German text of line `30201057`, but not its audio. Describe the repair for the Will variant, and say why a plain `tts-batch` rerun is not enough.

---

## Answers

**1. B.** The redirect sends every request to the mod's folder, and a missing file plays as silence (`tools/check_coverage.py:3-4`; `docs/MAINTENANCE.md:13`). A is the misconception the tool exists to catch. C and D do not happen.

**2. B.** The glob finds no catalogs (`tools/check_coverage.py:35`), so the index is empty, `missing` is empty (`:66`) and the exit code is 0 (`:90`). Always read the line count. A is wrong because there is no check for "no catalogs". C would happen with a missing `--audio` folder instead. D is wrong because `parse_cat` is never called.

**3. B.** The index holds only `(size, md5)` of the audio entries (`tools/check_coverage.py:32-41`). Texts are used only to print and count characters (`:70-77`). A is covered by the DLC glob (`:35`), C by the base glob, and D by the stored index comparison (`:81-85`).

**4. B.** The comparison runs only `if store.is_file()` (`tools/check_coverage.py:82-85`). A needs a saved baseline. C is wrong because the ids still exist in the mod folder. D is wrong: `--save-index` stores the current index after the comparison (`:86-89`), and only when passed, so it cannot report on its own run.

**5. B.** All six entries are redirected to `…\voice\10201\normal` (`tools/build_mod.py:29-35`), and `game_index` defaults to `context="normal"` (`tools/check_coverage.py:32`). A, C and D are not the reason. The other contexts exist in the same catalog as `normal`.

**6.** The coverage check still finds the 12 ids, because it reads the game catalogs directly, not `build/orig` (`tools/check_coverage.py:35-40`). The repairs fail quietly. `tts-batch` takes its ids from the stale `--ids-from` folder (`tools/voice_convert_elevenlabs.py:134`), so the new ids are never planned and it reports 0 to generate. The English `process_audio.py --files <new ids>` finds no source files and exits with "no files in …" (`tools/process_audio.py:126-133`). The update would ship with 12 silent lines.

**7.** Delete `build/tts/will_de/30201057.wav`. Then run `tts-batch … --files 30201057` (with `--model eleven_v4_turbo` and the refreshed `--tfile`) and `process_audio.py --variant will_dark --src build/tts/will_de --src-ext wav --gain-db 6 --files 30201057 --dst build/audio/will_dark_g6`. A plain rerun skips every id whose WAV already exists (`tools/voice_convert_elevenlabs.py:146`), so the old wording would stay. The coverage check would not flag this case either, because the audio in the game did not change (`docs/MAINTENANCE.md:7`).
