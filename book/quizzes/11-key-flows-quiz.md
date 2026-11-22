# Quiz: Key Flows

Chapter: [11 · Key Flows](../11-key-flows.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Apply]** With `bosota_voice_will_de` installed, the mission script plays line `30201131` in context `normal`. Which file does the engine open?

- A) `voice-l049\10201\normal\30201131.ogg` from the game catalog
- B) `extensions\bosota_voice_will_de\voice-l049\10201\normal\30201131.ogg`
- C) `extensions\bosota_voice_will_de\voice\10201\normal\30201131.ogg`
- D) `extensions\bosota_voice_will_de\voice\10201\comm\30201131.ogg`

**2. [Apply]** In Flow A, the normalisation targets −22 LUFS, yet line `30201131` measures −18.2 LUFS after processing. Why?

- A) The normalisation failed for that file
- B) `--gain-db 4` adds 4 dB after the normalisation, with a limiter at −1 dBFS
- C) Rubberband makes the line louder
- D) Ogg Vorbis encoding adds about 4 dB

**3. [Apply]** In Flow B, `tts-batch` produces 2,319 WAVs, yet `build/audio/will_dark_g6/` must hold 2,324 files. Where do the other five come from?

- A) `process_audio.py` makes them from silence
- B) They are copied from `build/audio/d12_alien_mid_g9/`, the processed originals, because those ids have no text
- C) A second `tts-batch` run with `--page 10202`
- D) They are not needed, because the game never requests them

**4. [Apply]** In Flow B you forget step 4 (copying the five textless ids) and run step 5, `check_coverage.py --lang l049 --audio build/audio/will_dark_g6`. What is the result?

- A) 0 missing, because those ids have no text in the game
- B) 5 missing ids listed and exit code 1
- C) A warning only, because the ids are German-only
- D) The tool copies them automatically

**5. [Design]** How was it proven that the engine takes a redirected `<sample start>` path literally, without inserting a language suffix?

**6. [Apply]** In Flow D, why must the old staging folder `build/workshop/stage2/extensions/ws_3824406333/` be deleted by hand, and why must `version` be raised above 103 rather than above the configured 102?

**7. [Apply]** On a German X4 installation, how do you hear the English variant in Flow A without changing the interface language?

- A) Rename `bosota_voice_alien_en` to `bosota_voice_alien_de`
- B) Start X4 with the launch option `-voicelanguage 44`
- C) Install `alien_en` and `alien` together
- D) Set `X4_GAME_DIR` to an English installation

---

## Answers

**1. C.** The diff sets `sample start` to `extensions\bosota_voice_will_de\voice\10201\normal` (`dist/bosota_voice_will_de/libraries/sound_library.xml:5`). The engine appends only the file name, with no language suffix (`docs/phase0-findings.md:47`). A is the behaviour without the mod. B adds a suffix that is not there. D is wrong because all six entries read `normal` (`tools/build_mod.py:32-35`).

**2. B.** `volume={gain_db}dB` and `alimiter` come after the linear `loudnorm` (`tools/process_audio.py:92-95`). −22 + 4 is about −18 LUFS. A would show "loudnorm measurement failed" (`:89-90`). C is wrong because pitch and filters run *before* the measurement. D is not how Vorbis behaves.

**3. B.** The recipe says to copy the five ids without text from `build/audio/d12_alien_mid_g9` (`config/variants.json:94`). `tts-batch` lists them as "without text" (`tools/voice_convert_elevenlabs.py:139`, `:149-150`). A and C are not in the recipe. D is wrong because they are real ids in the German catalog, and missing files play as silence.

**4. B.** The game index holds every `.ogg` id under `voice-l049/10201/normal/`, whether or not it has text (`tools/check_coverage.py:39-40`). The five are missing from the folder (`:66`), so the exit code is 1 (`:90`). A confuses texts with audio. C and D describe behaviour the tool does not have.

**5.** Diagnostic v6 pointed the flight-school tutor's entries at a mod folder. A subfolder named `voice` held Betty's lines and one named `voice-l049` held Boso's. The tutor spoke with Betty's voice, so the engine read `voice\…` exactly as written (`docs/HISTORY.md:29`; `docs/phase0-findings.md:47`).

**6.** The installer removes only `bosota_*` folders (`tools/install_mod.py:30`, `:92-95`), and `copytree` refuses an existing target (`:111`). A second staging run therefore fails with `FileExistsError` unless the old `ws_` copy is deleted first. The version must beat the **live** one. modpub's last upload left the German item at 103 (`release/out/workshop/de/content.xml:2`), while the configuration still says 102 (`config/variants.json:120`). `update` needs a higher version or `-minor` (`docs/RELEASE.md:35`).

**7. B.** Flow A ends with this test (`book/11-key-flows.md:33`). A is wrong: renaming breaks the central invariant, because the redirect still names `bosota_voice_alien_en` (`tools/build_mod.py:29`). C would put two variants on the same entries. D changes only where the tools look for game files (`tools/install_mod.py:79`).
