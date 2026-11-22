# 0 · Start Here

> **What you'll be able to answer after this chapter:** what the project does and for whom (purpose, see "What is this?"), how to build and install it (operations, see "Run it locally"), the five ideas you must keep in your head (domain, see "The mental model"), and where to make your first change (change, see "Your first change").

## What is this?

`x4mod_less_annoying_voices` is a mod for the space game **X4: Foundations** (version 9.00) that replaces the voice of one character, the Boron scientist **Boso Ta**, whose original recordings are very high and shrill. It ships two published variants:

- **German track:** all 2,324 German lines re-spoken from the game's own texts by an ElevenLabs text-to-speech voice ("Will"), darkened afterwards.
- **English track:** the 1,750 original English recordings, processed (pitched down without slowing down, a slight "alien" timbre, mid-range emphasis).

Both counts are for X4 9.00. The German track simply has 574 more lines than the English one; the English game never asks for those ids ([Failure Modes](13-failure-modes.md#edge-cases-in-the-data)).

`config/variants.json` declares five variants. Two of them are the published Workshop builds; the other three are local builds:

| Variant | Language | Audio made by | Audio folder | Status |
|---|---|---|---|---|
| `alien_ws` | German | text-to-speech "Will" (despite the key's name) | `will_dark_g6` | published, Workshop item `ws_3824406333` |
| `alien_en_ws` | English | filter chain over the originals | `alien_mid_50_g4` | published, Workshop item `ws_3824446410` |
| `will` | German | text-to-speech "Will" | `will_dark_g6` | local build of the published German audio |
| `alien` | German | filter chain over the originals | `d12_alien_mid_g9` | local, the only German variant you can build without an ElevenLabs account |
| `alien_en` | English | filter chain over the originals | `alien_mid_50_g4` | local build of the published English audio |

The repository is not the mod itself. It is the **factory** that produces the mod: it extracts Boso Ta's lines from the game, generates or processes audio, writes the XML that tells the game where to find the new audio, validates that XML against the real game file, and installs or packages the result. Users of the Steam Workshop items never see this repository; the people who use it are the mod's author and anyone who wants to rebuild, tune or extend it.

No game audio is committed. Audio lives in the ignored `build/` folder (`.gitignore:2`) and in the game folder after installation.

## Run it locally

Prerequisites: Windows, X4 installed at `C:\Steam\steamapps\common\X4 Foundations` (or set `X4_GAME_DIR`), Python 3 (the project is developed with 3.14), and a full ffmpeg build with the Rubberband filter (`winget install Gyan.FFmpeg`). ElevenLabs is only needed if you regenerate the German voice. Run all commands from the repository root in PowerShell. The commands below spell out the default game path; if X4 is installed elsewhere, replace it in them.

```powershell
# 1. Get Boso Ta's original German lines out of the game (catalog 03 holds all of them in 9.00)
python -I tools/x4cat_extract.py "C:\Steam\steamapps\common\X4 Foundations\03.cat" build\orig "voice-l049/10201/normal/*"

# 2. Produce the audio of a variant (here: the German variant that needs no ElevenLabs account, because it filters the original recordings instead of using text-to-speech)
python -I tools/process_audio.py --variant d12_alien_mid --gain-db 9 --src build\orig\voice-l049\10201\normal --dst build\audio\d12_alien_mid_g9

# 3. Write dist/, check it against the game, install it (X4 must be closed)
python -I tools/build_mod.py
python -I tools/validate_mod.py
python -I tools/install_mod.py alien
```

In the paths, `l049` is the German and `l044` the English language id (`l0XX` stands for either), `10201` is Boso Ta's voice page, and `normal` is the line context. A `.cat` file is the plain-text index of the `.dat` archive with the same number.

Step 3 takes no audio arguments: `build_mod.py` reads `config/variants.json`, where each variant's `audio_variant` names the folder under `build\audio\` that holds its audio (the suffix `_g9` just repeats the `--gain-db` value). The variant `alien` points at `d12_alien_mid_g9`, which is why step 2 writes exactly that folder. `--variant` picks the filter chain in `tools/process_audio.py`; `--gain-db` is an absolute gain applied after loudness normalisation to −22 LUFS, with a limiter (`tools/process_audio.py:83,94-95`).

- `-I` runs Python in isolated mode: it ignores `PYTHON*` environment variables and the user site-packages directory and does not put the script directory on `sys.path`. Ordinary variables such as `X4_GAME_DIR` are still read.
- Which catalog holds a path can change with a patch (the catalog numbers above are verified for 9.00). After a patch, search the plain-text indexes: `Select-String -Path "<game>\0*.cat" -Pattern "^voice-l049/10201/normal/" -List` lists every catalog with at least one match.
- The text files (`t/0001-l0XX.xml`) are in `09.cat` in 9.00.
- `./init.sh` runs step 3's first two commands in one go (`init.sh:6-7`). It is a Bash script; on Windows, run it in Git Bash.
- The exact recipe for every variant, including the text-to-speech one, is stored in `config/variants.json` under the key `audio_recipe` of each variant (for example the `will` variant, `config/variants.json:130`).
- The full walkthrough is in [Key Flows](11-key-flows.md).

## The mental model

1. **Boso Ta is "voice page 10201".** The game identifies speakers by a numeric page. Every one of his lines is a file `voice-l0XX/10201/<context>/<line id>.ogg` inside the game's archives. → [Core Concepts](02-core-concepts.md)
2. **The game finds audio through `libraries/sound_library.xml`.** Six entries (`10201_normal`, `10201_comm`, …) tell the engine which folder to read. The mod never touches audio files of the game; it patches those six entries with an **XML diff** (X4's mechanism for patching a game XML file without replacing it) so they point at the mod's own folder. → [Building & Validating](05-building-and-validating.md)
3. **The redirect path is taken literally.** `extensions\<mod id>\voice\10201\normal` is loaded as written; the engine adds no language suffix. The game's own audio paths carry the language in the folder name (`voice-l049` for German), but the redirect does not, so every game language would read the same folder. So one mod folder serves one voice language only, and the folder name must equal the mod id (the `<id>` in `dist/<id>/`). → [The Big Picture](01-the-big-picture.md)
4. **A variant = an id + an audio folder + XML patches.** All variants are declared in `config/variants.json`; everything else is generated from it. → [Variants & Configuration](04-variants-configuration.md)
5. **Audio is made outside the game in two ways:** filter chains over the originals (`tools/process_audio.py`) or text-to-speech from the game texts (`tools/voice_convert_elevenlabs.py`), followed by the same loudness normalisation. → [Audio Processing](06-audio-processing.md), [Text-to-Speech](07-text-to-speech.md)

## Where things live

| Path | What it is |
|---|---|
| `config/variants.json` | The single source of truth: Boso Ta's six sound-library ids and the five variants |
| `tools/` | Seven Python command-line tools: extract (`x4cat_extract.py`), process (`process_audio.py`), text-to-speech (`voice_convert_elevenlabs.py`), build (`build_mod.py`), validate (`validate_mod.py`), install (`install_mod.py`) and the post-patch check (`check_coverage.py`) |
| `dist/<id>/` | Generated mod folders, XML only, committed so the diff is reviewable |
| `docs/` | Project documentation: findings, history, release and maintenance procedures |
| `release/` | Manifest and texts for `modpub`, an external tool from another repository that uploads the Workshop items. You do not need it to build or install the mod ([Installing & Releasing](08-installing-and-releasing.md)) |
| `book/` | This book |
| `build/` (ignored) | Extracted game files, generated and processed audio, samples, Workshop staging, a Python venv |

## Your first change

**"Make the English variant 2 dB quieter."** Edit nothing in `dist/` by hand. The level is a processing parameter of the English chain. The current English audio `alien_mid_50_g4` was made with `--gain-db 4`. Because the gain is absolute, not relative to the existing files, 2 dB quieter means rendering again with `--gain-db 2`:

```powershell
python -I tools/x4cat_extract.py "C:\Steam\steamapps\common\X4 Foundations\03.cat" build\orig "voice-l044/10201/normal/*"
python -I tools/process_audio.py --variant alien_mid_50 --gain-db 2 --src build\orig\voice-l044\10201\normal --dst build\audio\alien_mid_50_g2
```

Then:

1. Set `audio_variant` to `alien_mid_50_g2` for **both** English variants, `alien_en` (key `variants.alien_en.audio_variant`, `config/variants.json:55`) and the Workshop build `alien_en_ws` (key `variants.alien_en_ws.audio_variant`, `config/variants.json:160`), otherwise the Workshop keeps the old level.
2. Run `python -I tools/build_mod.py` and `python -I tools/validate_mod.py`.
3. Close X4, then run `python -I tools/install_mod.py alien_en`.

Judge the result **in the game**, never by listening to the files on their own (for example on headphones): a dark voice that sounds as loud as the original on the PC can still drown in the station ambience ([Failure Modes](13-failure-modes.md)).

## Where to look

`README.md` (user-facing), `CLAUDE.md` (rules for maintainers and agents), `docs/phase0-findings.md` (verified engine facts), `docs/HISTORY.md` (why it ended up like this).

→ Check your understanding: [quizzes/00-start-here-quiz.md](quizzes/00-start-here-quiz.md)
