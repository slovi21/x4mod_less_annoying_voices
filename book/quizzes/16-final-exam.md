# Final Exam: The Boso Ta Voice Mod

Book: [Table of contents](../README.md)

How to use: answer closed-book first, then check the answers and reread the cited code. The questions are mixed across all chapters on purpose. Questions 5, 10 and 15 are scenarios; answer them as a numbered list of steps.

**1. [Apply]** Nobody is subscribed to the English Workshop item. You run `install_mod.py alien_en_ws` against your own game folder, so `extensions\ws_3824446410\` now holds loose files. Does Boso speak with the mod voice?

- A) No; `ws_*` builds work only when Steam installs them as a catalog
- B) Yes; the folder name, the `content.xml` id and the redirect segment are all `ws_3824446410`, so the redirect resolves
- C) No; the installer refuses `ws_*` keys outside a staging folder
- D) Only after `WorkshopTool update` registers the folder

**2. [Apply]** `bosota_voice_alien` is installed. Someone deletes `dist/bosota_voice_will_de/`, and you run `install_mod.py will` with X4 closed. What happens?

- A) The installer exits at once with "fehlt – zuerst build_mod.py", and `bosota_voice_alien` stays
- B) `bosota_voice_alien` is removed first, then the installer exits with "fehlt – zuerst build_mod.py", so no variant is left
- C) The installer runs `build_mod.py` and continues
- D) It installs the audio without XML

**3. [Apply]** What does `tts-batch … --dry-run` do?

- A) Sends one test request per line with zero credits charged
- B) Prints how many ids there are, with and without text, how many are to generate and their character count, then returns before any request and before even looking for ffmpeg
- C) Generates the WAVs but skips the post-processing
- D) Checks the API quota and stops if there is not enough

**4. [Apply]** Someone changes the `is3d` operation in `sound_attr_ops` from `"replace"` to `"add"`. What does `validate_mod.py` report?

- A) Nothing; `add` and `replace` are equivalent for attributes
- B) An error for each id that the attribute `is3d` already exists ("replace statt add verwenden"), because the base entries carry `is3d="1"`
- C) "No matching node", because `add` needs a different selector
- D) A warning that the value 0 is out of range

**5. [Apply] (Scenario)** An X4 patch adds 40 new Boso Ta lines in both languages. List every step until Workshop subscribers hear them in both languages. Then say what goes wrong if you skip re-extracting the originals.

**6. [Recall]** In X4 9.00, which catalogs hold Boso Ta's voice lines, the text files and `libraries/sound_library.xml`?

- A) Lines `01.cat`, texts `09.cat`, sound library `08.cat`
- B) Lines `03.cat`, texts `09.cat`, sound library `08.cat`
- C) Lines `03.cat`, texts `08.cat`, sound library `09.cat`
- D) All three in `09.cat`, because the highest catalog overrides everything

**7. [Apply]** `check_coverage.py` reports "missing in mod: 0   not in game any more: 3". What is its exit code, and do the three extra files matter?

- A) Exit 1; the extra files mean the mod is out of date
- B) Exit 0; files the game no longer has are harmless, and only missing ids fail the check
- C) Exit 1, but only with `--save-index`
- D) Exit 0, but the three files are deleted automatically

**8. [Design]** Why does `validate_mod.py` extract `sound_library.xml` from the game on every run instead of using a copy committed to the repository?

**9. [Apply]** You run `install_mod.py will --game-dir build/workshop/moddb` on a fresh clone where `build/workshop/moddb/` exists but has no `extensions/` subfolder. What happens?

- A) The installer creates `extensions/` and installs
- B) It exits with "… extensions existiert nicht – Spielordner prüfen", before deleting or copying anything
- C) It installs into `build/workshop/moddb/` directly
- D) It falls back to the default game folder

**10. [Apply] (Scenario)** You must make the **German Workshop build** 3 dB louder. Name the files and commands, the version number you set, and what could break.

**11. [Apply]** What is the difference between `process_audio.py … --gain-db 0` and leaving `--gain-db` out?

- A) `--gain-db 0` still adds the −1 dBFS limiter; leaving it out adds nothing
- B) None; the default is 0.0, and a gain of 0 adds neither `volume` nor `alimiter`
- C) Leaving it out disables the loudness normalisation
- D) `--gain-db 0` is rejected as invalid

**12. [Apply]** ElevenLabs answers every request for one line with HTTP 429. How long does `tts_one` wait in total before it gives up on that line, and what does it return?

- A) It never gives up on 429
- B) 3 + 6 + 9 + 12 + 15 = 45 s of pauses, then "gave up after retries"
- C) 3 s, then "HTTP 429: …"
- D) 15 s, then it raises an exception

**13. [Apply]** A selector in a diff matches two nodes of the base file. How does `validate_mod.py` treat it?

- A) As an error; every selector must match exactly one node
- B) As a warning; the operation is applied to both nodes
- C) It applies the operation to the first node only
- D) It ignores the operation

**14. [Apply]** On a machine where `tasklist` cannot be run, X4 is open and you run `install_mod.py alien_en` against the default game folder. What does the running-game guard do?

- A) It blocks, because it cannot prove that X4 is closed
- B) Nothing; `game_running()` returns `False` when `tasklist` fails, so the swap goes ahead (with the silent-voice risk)
- C) It asks for confirmation
- D) It falls back to checking the window title

**15. [Apply] (Scenario)** A tester is subscribed to the German Workshop item, which sits in `<game>\extensions\ws_3824406333\`. They also ran `install_mod.py alien` earlier. Now Boso's voice is unpredictable. Then `install_mod.py alien_ws` against the game folder crashes. Explain both symptoms and give a clean way back to a single variant.

**16. [Apply]** A patch re-records the English original of one line (same id, new audio). What does this mean for the two published variants, and what do you do?

**17. [Apply]** A patch adds `noocclusion="true"` to `10201_normal` in the base game. What happens to the mod, and what is the fix?

- A) Nothing; `add` overwrites an existing attribute
- B) That `add` fails ("attribute exists"); the validator reports it. Switch that id from the `add` item to a `replace` item in `sound_attr_ops`
- C) The whole diff is rejected; remove `sound_attr_ops` entirely
- D) The redirect stops working for `10201_normal`

**18. [Design]** Why must a variant's audio folder contain every line id the game has for page 10201 in that language, even lines nobody complained about?

- A) The installer refuses incomplete folders
- B) The redirect replaces the folder for every line, and the engine does not fall back to the original when a file is missing; that line plays as silence
- C) The Workshop rejects incomplete uploads
- D) `validate_mod.py` fails on incomplete folders

**19. [Apply]** `quota` fails with HTTP 401, but you have just generated samples with `tts` using the same key. What is the likely explanation?

- A) The key has expired since the samples were made
- B) The key lacks the user-read permission that `/user/subscription` needs; text-to-speech can still work with it
- C) `quota` uses a different header than `tts`
- D) The key file is read only by `tts`

**20. [Recall]** Which tools read DLC catalogs (`extensions/ego_dlc_*/ext_0N.cat`)?

- A) Both `validate_mod.py` (through `find_latest_entry`) and `check_coverage.py`
- B) Only `check_coverage.py`
- C) Only `validate_mod.py`
- D) Neither

**21. [Apply]** As the very first command after a patch you run `check_coverage.py --lang l044 --audio build/audio/alien_mid_50_g4 --save-index`. Do you lose the report of changed originals?

- A) Yes; the new index is saved first, so nothing appears as changed
- B) No; in the same run the comparison with the old index happens before the new index is saved. Only a second run would show 0 changed
- C) Yes, because `--save-index` turns off the comparison
- D) No, because the index is never overwritten

---

## Answers

**1. B.** The redirect is `extensions\ws_3824446410\voice\10201\normal` (`tools/build_mod.py:29`), and the installer copies `dist/ws_3824446410` to `extensions/ws_3824446410` with the audio (`tools/install_mod.py:100-115`). The central invariant holds, so loose files work. A is wrong: the catalog is a Workshop packaging detail. C is wrong: every key is a valid choice (`:78`). D is wrong because registration plays no part in how the game resolves files.

**2. B.** Removal (`tools/install_mod.py:92-95`) comes before the `dist/` check (`:101-103`). A assumes the check happens first. C is wrong: no tool calls another. D is wrong because the exit happens before any copy.

**3. B.** `--dry-run` returns after the plan is printed (`tools/voice_convert_elevenlabs.py:148-152`), and `find_ffmpeg` is called only after that (`:153`). A and C are wrong because no request is sent. D is not what the flag does; `quota` is a separate command (`:54-60`).

**4. B.** With `op == "add"` the builder writes `<add … type="@is3d">` (`tools/build_mod.py:41-42`). The validator rejects an `add` on an attribute that exists (`tools/validate_mod.py:93-94`). `is3d` exists in the base entries, which is why the configuration uses `replace` (`tools/build_mod.py:37`, `config/variants.json:42-50`). A ignores the precondition. C is wrong because the selector finds the node. D is wrong: there are no range checks for attributes.

**5. Scenario: 40 new lines.**
1. Find the catalogs that now hold `voice-l049/10201/normal/`, `voice-l044/10201/normal/` and the text files (`Select-String … -List`).
2. Re-extract the originals for both languages into `build/orig`, one catalog at a time in ascending order (`tools/x4cat_extract.py:61-62` overwrites, so later catalogs win).
3. Re-extract `t/0001-l049.xml` and `t/0001-l044.xml` into `build/base`.
4. `validate_mod.py`: the selectors still match.
5. `check_coverage.py --lang l049 …` and `--lang l044 …` with `--tfile`: the 40 ids are listed with their character count (`tools/check_coverage.py:66`, `:72-77`).
6. German: `tts-batch --voice bIHbv24MWmeRgasZH58o --model eleven_v4_turbo --tfile build/base/t/0001-l049.xml --ids-from build\orig\voice-l049\10201\normal --dst build/tts/will_de`. A `--dry-run` first shows the cost. Existing WAVs are skipped (`tools/voice_convert_elevenlabs.py:146`), so only the new lines are billed. Then `process_audio.py --variant will_dark --src build/tts/will_de --src-ext wav --gain-db 6 --files <ids> --dst build/audio/will_dark_g6`. A new id without text has to be filled like the five textless ones.
7. English: `process_audio.py --variant alien_mid_50 --gain-db 4 --src build\orig\voice-l044\10201\normal --files <ids> --dst build/audio/alien_mid_50_g4`.
8. Rerun `check_coverage.py`: 0 missing.
9. Raise `version` of `alien_ws` to at least 104 and of `alien_en_ws` to at least 103, above the live 103/102 (`config/variants.json:120`, `:191`; `release/out/workshop/*/content.xml:2`). Run `build_mod.py` and `validate_mod.py`.
10. Delete the old staging folders `build/workshop/stage2/extensions/ws_3824406333` and `stage2_en/extensions/ws_3824446410`; otherwise `copytree` fails (`tools/install_mod.py:111`). Then `install_mod.py alien_ws --game-dir build/workshop/stage2` and `alien_en_ws --game-dir build/workshop/stage2_en`.
11. `WorkshopTool.exe update -path … -buildcat -changenote "…"` for both items, without `-namedesc up` if modpub's titles should stay (`docs/RELEASE.md:27`, `:32`). Subscribers receive the update automatically (`docs/MAINTENANCE.md:32`).
12. Rebuild the ModDB packages too, note the patch in `docs/HISTORY.md`, and save the new baseline with `--save-index` for both languages.

*If you skip re-extracting the originals:* the coverage check still reports the 40 ids, because it reads the catalogs directly (`tools/check_coverage.py:35-40`). But `tts-batch` plans only ids from the stale `--ids-from` folder (`tools/voice_convert_elevenlabs.py:134`) and reports 0 to generate. The English `process_audio.py --files <ids>` finds no source files and exits "no files in …" (`tools/process_audio.py:126-133`). An update shipped anyway leaves the 40 lines silent for every subscriber. Skipping the texts instead shows the new ids as "without text" (`tools/voice_convert_elevenlabs.py:139`).

**6. B.** Lines `03.cat` (`README.md:44`), texts `09.cat` (`book/03-game-archives-and-extraction.md:55`), sound library `08.cat` (`docs/phase0-findings.md:19`). A repeats the old README error. C swaps texts and library. D misreads the override rule: a later catalog wins only for paths it actually contains (`tools/x4cat_extract.py:69-82`).

**7. B.** `extra` is printed as harmless (`tools/check_coverage.py:67`, `:79`), and the exit code depends only on `missing` (`:90`). A, C and D invent consequences the code does not have.

**8.** Patches can change the file and can move it to another catalog. The check has to run against what the game will actually load. `load_base` asks `find_latest_entry` which base catalog wins, and extracts it fresh into `build/base` on every run (`tools/validate_mod.py:32-40`). A committed copy would go stale after the next patch. It would also put Egosoft data into git, which the project avoids (`.gitignore:2`).

**9. B.** The `extensions/` check (`tools/install_mod.py:86-88`) comes before the removal loop (`:92-95`). A is wrong: nothing creates the folder. Create `build/workshop/moddb/extensions/` once (`docs/RELEASE.md:52`). C and D do not happen.

**10. Scenario: German Workshop build +3 dB.**
1. Re-render the Will set at +9 dB instead of +6, from the existing TTS cache. No credits are spent: `process_audio.py --variant will_dark --src build/tts/will_de --src-ext wav --gain-db 9 --dst build/audio/will_dark_g9` (`tools/process_audio.py:94-95`).
2. Add the five textless ids (`10417`, `10603`, `30226001`–`30226003`). They have no WAV (`config/variants.json:94`). Copying them from `d12_alien_mid_g9` keeps them at their old level. Rendering `d12_alien_mid` at `--gain-db 12 --files …` keeps them in step.
3. `check_coverage.py --lang l049 --audio build/audio/will_dark_g9`: 0 missing.
4. `config/variants.json`: set `audio_variant` of `alien_ws` (`:89`) to `will_dark_g9`, and of `will` (`:125`) too, so ModDB and Workshop match. Set `version` of `alien_ws` (`:120`) to **104**. The live item is at 103 (`release/out/workshop/de/content.xml:2`). 103 would not be above it, and 102 is what the configuration still says.
5. `build_mod.py`, `validate_mod.py`. Close X4, run `install_mod.py will`, and listen in the game.
6. Delete `build/workshop/stage2/extensions/ws_3824406333`, then `install_mod.py alien_ws --game-dir build/workshop/stage2`.
7. `WorkshopTool.exe update -path …\stage2\extensions\ws_3824406333 -buildcat -changenote "…"`, without `-namedesc up` if the modpub title "Boso Ta – erträgliche Stimme" should stay (`docs/RELEASE.md:27`).

*What could break:*
- A version of 103 or lower is refused without `-minor` (`docs/RELEASE.md:35`).
- If the five textless files are missing, those lines are silent.
- A stale staging folder makes `copytree` raise `FileExistsError` (`tools/install_mod.py:111`).
- `-namedesc up` overwrites the modpub title.
- At +9 dB the −1 dBFS limiter works much harder (`tools/process_audio.py:95`), and true peaks can come close to 0 dBTP.
- Changing only `alien_ws` leaves the ModDB build at the old level.

**11. B.** The default is `0.0` (`tools/process_audio.py:112`), and the gain step runs only `if gain_db:` (`:94`). 0 is falsy, so neither `volume` nor `alimiter` is added. A is wrong for that reason. C confuses it with `--no-normalize` (`:111`). D is wrong because 0 is a valid float.

**12. B.** On 429 the loop sleeps `3 * (attempt + 1)` for each of its five attempts (`tools/voice_convert_elevenlabs.py:83`, `:91-93`). The `for … else` then returns "gave up after retries" (`:97-98`). C describes the handling of other non-200 codes (`:94-95`). A and D do not match the code.

**13. B.** More than one target adds a warning, and the operation runs for every target (`tools/validate_mod.py:115-117`). A is how the docstring states the goal (`:6`), but the code makes it a warning, not an error. C and D do not match the code.

**14. B.** Any exception from `tasklist` makes `game_running()` return `False` (`tools/install_mod.py:53-57`). The guard therefore does not block (`:89-90`). A, C and D describe behaviour the code does not have. The risk is the one the guard exists for: a swap under a running game silences Boso (`docs/phase0-findings.md:50`).

**15. Scenario: Workshop item and local build together.**
- *Unpredictable voice:* `install_mod.py alien` removed only `bosota_*` folders (`tools/install_mod.py:30`, `:92-95`). Both `ws_3824406333` (Will) and `bosota_voice_alien` (Alien) are active, and both replace the same six `<sample>` elements (`tools/build_mod.py:32-35`). Which one wins depends on X4's extension load order; the book infers the alphabetically later one.
- *Crash:* `install_mod.py alien_ws` first deletes `bosota_voice_alien`. It then calls `shutil.copytree` onto the existing `extensions\ws_3824406333` and raises `FileExistsError` (`tools/install_mod.py:111`).
- *Clean way back:*
  - With X4 closed, choose one source. For the Workshop build, run `install_mod.py --remove` to clear every `bosota_*` folder and keep the subscription.
  - For a local build, unsubscribe in Steam first (or delete `extensions\ws_3824406333` by hand), then run `install_mod.py <key>`.
  - Check `extensions/` for exactly one Boso variant.

**16.** For the German Will variant: no effect. The redirect never reads the originals, and the Will audio comes from text (`docs/MAINTENANCE.md:7`). For the English variant the processed copy is now out of date (`docs/MAINTENANCE.md:9`). The coverage check reports the id as changed only if a baseline was saved (`tools/check_coverage.py:82-85`). Fix: re-extract the English originals, then run `process_audio.py --variant alien_mid_50 --gain-db 4 --src build\orig\voice-l044\10201\normal --files <id> --dst build/audio/alien_mid_50_g4`. Then rebuild, stage `alien_en_ws`, update the item with a version above 102, and save a new baseline.

**17. B.** The validator rejects `add` on an existing attribute (`tools/validate_mod.py:93-94`). The documented fix is to switch that id to a `replace` (`docs/MAINTENANCE.md:23`). The builder writes `replace` for any op other than `"add"` (`tools/build_mod.py:43-44`). A is wrong because the game rejects that operation. C is wrong because only that operation fails. D is wrong because the `<sample>` replace is a separate operation.

**18. B.** A missing file plays as silence, and the engine does not fall back (`tools/check_coverage.py:3-4`; `docs/MAINTENANCE.md:13`). A, C and D are wrong: the installer checks only that the folder has some `.ogg` files (`tools/install_mod.py:108-110`). The validator ignores audio, and the Workshop has no such check.

**19. B.** Recorded in `docs/dev-team/LESSONS.md:31`. `quota` calls `/user/subscription` and fails on `raise_for_status` (`tools/voice_convert_elevenlabs.py:55-56`). A contradicts the working samples. C is wrong: both use `headers()` with `xi-api-key` (`:50-51`, `:86`). D is wrong: both read the key through `api_key()` (`:39-47`).

**20. B.** `game_index` globs `extensions/ego_dlc_*/ext_0[1-9].cat` (`tools/check_coverage.py:35`). `find_latest_entry` scans only `01.cat`–`09.cat` in the game folder (`tools/x4cat_extract.py:73-74`). So A and C are wrong, and D ignores the coverage glob.

**21. B.** The comparison (`tools/check_coverage.py:81-85`) runs before the save (`:86-89`) within one run. A and C have the order wrong. D is wrong: `write_text` replaces the stored index (`:88`).
