# Quiz: Start Here

Chapter: [0 · Start Here](../00-start-here.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Recall]** What does this repository actually produce?

- A) Replacement audio files that are written into the game's own `03.cat/03.dat` archive
- B) A pipeline that extracts Boso Ta's lines, makes new audio, writes an XML diff that redirects his six sound entries to a mod folder, checks that diff and installs it
- C) A plugin that runs next to X4 and pitch-shifts Boso Ta's voice while the game plays
- D) A set of `<pitch>` and `<filter>` engine effects that X4 applies to the original recordings

**2. [Apply]** On a fresh clone you run `python -I tools/build_mod.py` and then `python -I tools/install_mod.py alien`, with X4 closed and no other steps. What happens?

- A) Both succeed; the mod is installed with XML only and Boso Ta is silent in the game
- B) `build_mod.py` fails because `build/audio/d12_alien_mid_g9/` is missing
- C) `build_mod.py` writes `dist/` and prints a "no audio yet" note; the installer removes any existing `bosota_*` folders and then stops with "keine Audiodateien in …"
- D) The installer notices the missing audio and extracts and processes it from the game itself

**3. [Recall]** Why can one installed mod folder not serve both German and English players?

- A) X4 loads only one extension per voice language
- B) `content.xml` can declare only one language
- C) The engine uses the redirected path exactly as written and adds no `-l0XX` language suffix, so the folder can hold only one language's set of line files
- D) The German and English `.ogg` files have different sample rates and cannot be mixed in one folder

**4. [Recall]** In X4 9.00, which catalog do you pass to `x4cat_extract.py` to get Boso Ta's original voice lines?

- A) `01.cat`
- B) `03.cat`
- C) `08.cat`
- D) `09.cat`

**5. [Apply]** What does `./init.sh` do?

- A) Extracts the originals, processes the audio, builds, validates and installs the default variant
- B) Builds every variant into `dist/` and validates all of them against the game's real `sound_library.xml`, stopping at the first failing command
- C) Builds all variants and installs the German one
- D) Validates only the variant that is currently installed in the game

**6. [Apply]** (locate the change) You want the English variant 2 dB quieter. Which files or settings do you change, and why is changing only `alien_en` not enough?

**7. [Design]** The chapter insists that loudness is judged in the game, never on headphones. Why does a level that measures right still fail in the game?

---

## Answers

**1. B.** The repository is the factory: it redirects the six `10201_*` sound entries to `extensions\<id>\voice\10201\normal` (`tools/build_mod.py:29-35`) and keeps all audio out of git (`.gitignore:2`). A is wrong because the mod never writes into the game's archives; it only adds an extension folder (`tools/install_mod.py:111-115`). C is wrong because every tool is a one-shot command; nothing runs alongside the game. D is wrong because the generated diff has no effects at all (`dist/ws_3824406333/libraries/sound_library.xml:3-28`); the effect checks in the validator are leftovers (`tools/validate_mod.py:139-148`).

**2. C.** `build_mod.py` never touches audio and only prints a note when the audio folder is empty (`tools/build_mod.py:72-75`). The installer deletes every `bosota_*` folder first (`tools/install_mod.py:92-95`) and only then checks the audio and exits (`tools/install_mod.py:107-110`). A describes the old bug that was fixed. B is wrong because building does not depend on audio. D is wrong because no tool calls another; the audio recipe is only documentation (`config/variants.json:26`).

**3. C.** The redirect target is built from the mod id with no language part (`tools/build_mod.py:29`), and the engine takes that path literally (`docs/phase0-findings.md:47`). A is wrong: a language is not a property of an extension. B is wrong because `content.xml` carries both a language-44 and a language-49 text (`tools/build_mod.py:55-56`). D is wrong because all output is resampled to mono 44.1 kHz anyway (`tools/process_audio.py:97`).

**4. B.** `03.cat` holds all of page 10201 in both languages (`README.md:44`). A was the old mistake in the README that the book corrected (`book/README.md:53`). C holds `libraries/sound_library.xml` (`docs/phase0-findings.md:19`). D holds the text files `t/0001-l0XX.xml` (`book/03-game-archives-and-extraction.md:55`).

**5. B.** The script runs `build_mod.py` and `validate_mod.py` and nothing else (`init.sh:6-7`). With `set -euo pipefail` it stops at the first error (`init.sh:4`). It does no extraction, audio work or installing, so A and C are wrong. D is wrong because the validator checks every folder in `dist/` when given no arguments (`tools/validate_mod.py:177`).

**6.** Re-render the English chain at a lower gain into a new folder (for example `process_audio.py --variant alien_mid_50 --gain-db 2 … --dst build/audio/alien_mid_50_g2`). Then set `audio_variant` to the new folder in **both** `alien_en` (`config/variants.json:55`) and `alien_en_ws` (`config/variants.json:160`), build, validate and install. The installer copies audio from the folder named by the variant's own `audio_variant` (`tools/install_mod.py:107`). If you change only `alien_en`, the Workshop build keeps the old level. Editing `dist/` would not help: it holds no audio (`tools/build_mod.py:7`).

**7.** Equal measured loudness (LUFS) is not equal perceived loudness in the game's mix. A darker voice loses the 1–4 kHz energy that cuts through the station ambience, so it can drown even though its LUFS matches the original (`docs/HISTORY.md:39`). That is why the tool adds a separate gain on top of the normalisation (`tools/process_audio.py:4-5`).
