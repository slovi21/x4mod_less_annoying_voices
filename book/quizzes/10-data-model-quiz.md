# Quiz: Data Model & Files

Chapter: [10 · Data Model & Files](../10-data-model.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Recall]** The chapter calls one equality "the system's central invariant". Which three strings must be equal?

- A) The variant key, the `audio_variant` name and the folder name
- B) The install folder name, the `id` in `content.xml` and the folder segment in the redirect path
- C) The Workshop item number, the variant key and the `audio_variant`
- D) The line id, the text id and the sound id

**2. [Recall]** Where are the version numbers that are actually live on the Workshop recorded?

- A) `config/variants.json`
- B) `dist/ws_<n>/content.xml`
- C) `release/out/workshop/<lang>/content.xml`, modpub's upload copies (ignored by git)
- D) `release/mod.yaml`

**3. [Apply]** To free disk space you delete `build/tts/will_de/`. What does the next `tts-batch` run for German do?

- A) Generates only lines that are missing in `build/audio/will_dark_g6`
- B) Generates all lines with text again (about 2,319) and spends credits for each
- C) Fails because the destination folder is missing
- D) Reuses the WAVs cached by ElevenLabs on the server

**4. [Apply]** You edit `build/base/libraries/sound_library.xml` by hand to test a selector, then run `validate_mod.py`. Which base does the validator use?

- A) Your edited file, because it already exists in the cache
- B) A fresh copy, because it extracts the effective file from the game catalog into `build/base` on every run and overwrites your edit
- C) The file inside `dist/`
- D) It refuses to run because the cache was changed

**5. [Recall]** Which of these paths is committed to git?

- A) `build/audio/will_dark_g6/`
- B) `release/out/status.json`
- C) `release/assets/`
- D) `.elevenlabs_key`

**6. [Apply]** By mistake you set `audio_variant` of `alien_en` to `will_dark_g6`, then build, validate and install. What happens?

- A) `validate_mod.py` reports a language mismatch
- B) `install_mod.py` refuses because the folder belongs to another variant
- C) Everything passes; English players then hear the German Will recordings
- D) Boso is silent, because German files cannot be played on the English track

**7. [Design]** A subscribed Workshop item has `content.xml`, `ext_01.cat` and `ext_01.dat` instead of loose `libraries/` and `voice/` folders. Why does the same redirect path still work?

---

## Answers

**1. B.** The builder uses `v['id']` for the output folder (`tools/build_mod.py:68`), for `content.xml` (`:53`) and for the redirect target (`:29`). The installer copies `dist/<id>` to `extensions/<id>` (`tools/install_mod.py:100-104`). A, C and D mix in names that code never compares. For the Workshop builds the key (`alien_ws`) is not even similar to the id.

**2. C.** modpub's copies carry the live numbers, DE `version="103"` and EN `version="102"` (`release/out/workshop/de/content.xml:2`, `release/out/workshop/en/content.xml:2`). The configuration and `dist/` still say 102 and 101 (`config/variants.json:120`, `:191`). So A and B are behind. D holds item numbers and staging paths, not versions (`release/mod.yaml:39-43`).

**3. B.** Ids are skipped only if `build/tts/will_de/<id>.wav` exists (`tools/voice_convert_elevenlabs.py:146`), so with the folder gone every planned id is generated. A is wrong: the TTS tool never looks at `build/audio`. C is wrong: the folder is created as needed (`:99`). D does not exist. The folder is the project's only resume cache.

**4. B.** `load_base` calls `extract` into `build/base` on every run and parses the result (`tools/validate_mod.py:32-40`). The write overwrites your edit (`tools/x4cat_extract.py:61-62`). A assumes a cache check that does not exist. C confuses the base file with the diff. D is wrong: nothing compares the file with the catalog.

**5. B.** `.gitignore` excludes `release/out/*` but re-includes `!release/out/status.json` (`.gitignore:11-13`). A is under the ignored `build/` (`:2`), C is ignored at `:10`, and D at `:9`.

**6. C.** The validator checks only XML (`tools/validate_mod.py:56-167`). The installer checks only that the folder has `.ogg` files (`tools/install_mod.py:107-110`). The English game requests its ids, which all exist in the German set, so German lines play. A and B are checks that do not exist. D is wrong because both sets are the same format, Ogg Vorbis mono 44.1 kHz (`tools/process_audio.py:96-97`).

**7.** `-buildcat` packs the folder contents into `ext_01.cat/.dat` (`docs/RELEASE.md:19`). X4 mounts an extension's catalogs relative to the extension folder, as it does for DLC `ext_NN.cat` (`docs/phase0-findings.md:9`). `extensions\ws_3824406333\voice\10201\normal\<id>.ogg` therefore resolves to an entry inside the mounted catalog, just as it would to a loose file.
