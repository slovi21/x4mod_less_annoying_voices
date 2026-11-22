# Quiz: The Big Picture

Chapter: [1 · The Big Picture](../01-the-big-picture.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Recall]** How do the pipeline steps pass work to each other?

- A) `build_mod.py` starts `process_audio.py` as a subprocess when audio is missing
- B) Through folders on disk; a person (or an agent) runs each tool in order, and no tool starts another tool
- C) Through a shared SQLite database under `build/`
- D) Through a Makefile that runs every step when `config/variants.json` changes

**2. [Recall]** Which code dependency between the tools actually exists?

- A) `install_mod.py` imports `build_mod` to rebuild `dist/` before copying
- B) `process_audio.py` imports `voice_convert_elevenlabs` to fetch missing lines
- C) `check_coverage.py` imports `parse_cat` from `x4cat_extract`, and `voice_convert_elevenlabs.py` imports `find_ffmpeg` from `process_audio`
- D) `build_mod.py` imports `validate_mod` and refuses to write an invalid diff

**3. [Apply]** You fix a typo by editing `dist/bosota_voice_alien_en/libraries/sound_library.xml` by hand and then run `./init.sh`. What happens to your edit?

- A) It survives, because `build_mod.py` only writes files that do not exist yet
- B) It is overwritten: `build_mod.py` runs first and rewrites both files of every variant
- C) `init.sh` refuses to run because `dist/` has uncommitted changes
- D) `validate_mod.py` checks your edited file first, and the build overwrites it afterwards

**4. [Recall]** Why does the project check the diff offline instead of simply starting the game?

- A) X4 crashes on a bad diff, so a crash would lose the save
- B) A selector that matches nothing is reported only in the game's log (with `-logfile`) and the operation is skipped, so the mod looks installed but does nothing
- C) X4 refuses unsigned diffs unless they have been validated first
- D) The validator checks that every audio file exists, which the game cannot do

**5. [Apply]** You set up the project on a new PC from a fresh clone. Which input must you regenerate before `install_mod.py` can succeed?

- A) The `dist/<id>/` folders
- B) The audio under `build/audio/<audio_variant>/`
- C) `config/variants.json`
- D) `release/mod.yaml`

**6. [Design]** Why does the mod patch `sound_library.xml` (the index) instead of shipping new files under the game's original voice path, and what does that choice cost?

**7. [Design]** The audio recipe in `config/variants.json` is prose that no tool executes. Give the reason the book offers for this, and the risk it brings.

---

## Answers

**1. B.** Each tool reads and writes files, and orchestration is manual. `build_mod.py`, for example, only counts the audio files and prints a note (`tools/build_mod.py:72-75`). A is wrong: no tool starts another tool. The only subprocess calls are to ffmpeg (`tools/process_audio.py:77-78`). C and D do not exist in the repository; the only entry points are the CLIs and `init.sh` (`init.sh:6-7`).

**2. C.** The real imports are `tools/check_coverage.py:22` (and the same for the validator, `tools/validate_mod.py:25`) and `tools/voice_convert_elevenlabs.py:30`. A is wrong because the installer only reads `config/variants.json` and `dist/` (`tools/install_mod.py:31`, `:101`). B and D invert the real direction. The builder never validates; validation is a separate step (`init.sh:6-7`).

**3. B.** `init.sh` runs the builder before the validator (`init.sh:6-7`), and the builder writes `content.xml` and the diff for every variant without checking what is there (`tools/build_mod.py:69-71`). A is wrong: `exist_ok=True` only stops the folder creation from failing. C is wrong: nothing checks git state. D has the order backwards.

**4. B.** The validator exists because "No matching node" is a silent failure (`tools/validate_mod.py:6`). The game logs it and skips the operation (`docs/phase0-findings.md:45`). A is wrong: nothing crashes. C is wrong: unsigned diffs are applied, and loading one is what marks the game as modified. D is wrong: the validator never looks at audio files (`tools/validate_mod.py:150-166` only reports XML state).

**5. B.** `build/` is ignored (`.gitignore:2`), and the installer stops when the audio folder has no `.ogg` (`tools/install_mod.py:107-110`). A is wrong because `dist/` is committed so the diff can be reviewed. C and D are versioned files.

**6.** The redirect of `<sample start>` into the mod folder was proven in the game by diagnostic v6 (`docs/HISTORY.md:29`) and is generated for all six entries (`tools/build_mod.py:32-35`). Shipping files under the original voice path was reported to be ignored for audio (not re-verified). The cost: the redirect path has no language part, so you need one mod per voice language, and every line id the game knows must exist in the mod folder. A missing file plays as silence; the engine does not fall back to the original (`tools/check_coverage.py:3-4`).

**7.** The steps include paid ElevenLabs calls and listening decisions that should never run implicitly (the book marks this as inference). The risk: the recipe string can drift from what was actually run, because nothing reads or checks it. Only `id`, `audio_variant`, names, descriptions, `version` and `sound_attr_ops` are used by code (`tools/build_mod.py:29-56`, `tools/install_mod.py:107`). The recipe text is at `config/variants.json:94`.
