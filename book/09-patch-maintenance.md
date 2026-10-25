# 9 · Patch Maintenance (`tools/check_coverage.py`, `docs/MAINTENANCE.md`)

> **What you'll be able to answer after this chapter:** what an X4 patch or DLC can break (failure), how the coverage check detects it (flow, data), what it does not detect (contracts), and the repair procedure (operations).

## Why it exists

The redirect sends **every** request for a Boso Ta line to the mod's folder. If a patch adds a line id the mod does not have, the engine plays silence for it; it does not fall back to the original. Boso's mouth moves, the subtitle shows, nothing is heard. This is the one patch scenario that produces a visible defect, and it is silent in the log. The tool detects it in seconds.

## Public surface

`python -I tools/check_coverage.py --lang l044|l049 --audio <folder> [--game-dir <X4>] [--tfile <text file>] [--save-index]` (`tools/check_coverage.py:55-62`). Exit code 1 if any id is missing (`:90`).

## Mechanism

1. **Game index** (`game_index`, `:32-41`): parses `01.cat`…`09.cat` and every `extensions/ego_dlc_*/ext_0N.cat` (signature catalogs are excluded by the glob), keeps entries under `voice-<lang>/10201/normal/` ending in `.ogg`, and maps line id → `(size, md5)`. Later catalogs overwrite earlier ones, matching the game's override order.
2. **Comparison** (`:64-68`): `missing` = ids in the game but not in the folder; `extra` = files in the folder the game no longer has (harmless).
3. **Text** (optional, `:70-79`): with `--tfile`, prints the text of up to 40 missing ids and the total characters to regenerate, using the same cleaning as the TTS tool (`load_texts`, `:44-52`) and the same `fp`-suffix fallback.
4. **Change detection** (`:81-89`): if `build/index/10201_<lang>.json` exists, every id whose `(size, md5)` differs from the stored index is reported as changed; `--save-index` stores the current index.

```text
$ python -I tools/check_coverage.py --lang l049 --audio build/audio/will_dark_g6 --tfile build/base/t/0001-l049.xml
game: 2324 lines for 10201/l049   mod folder: 2324 files   missing in mod: 0   not in game any more: 0
changed original files since last saved index: 0
```

## What it covers and what not

| Covered | Not covered |
|---|---|
| New line ids in context `normal` | Other contexts (all six entries read `normal` after the redirect, so only `normal` matters) |
| Changed original files (size/MD5), **if** a baseline was saved with `--save-index`; without one the "changed" line is silently omitted | Changed **texts** whose audio did not change (the German TTS would be outdated; compare text files by hand) |
| DLC catalogs | Mods from other authors that add Boso lines |
| | A changed `sound_library.xml` structure → use `validate_mod.py` |
| | Boso getting a different voice page → see `docs/MAINTENANCE.md`, case 4 |

### False passes

- Wrong `--game-dir` or `X4_GAME_DIR`: the catalog glob finds nothing, the tool prints "game: 0 lines" and exits **0** (`:35`, `:90`). Always read the line count.
- Missing `--audio` folder: every id counts as missing (exit 1), which at least fails loudly.

## The procedure after a patch

Based on `docs/MAINTENANCE.md`, with the steps that tool cannot do itself:

1. **Find the catalogs** that now hold page 10201 and the texts: `Select-String -Path "<game>\0*.cat" -Pattern "^voice-l049/10201/normal/","^t/0001-l049.xml " -List`.
2. **Re-extract the originals** for both languages from those catalogs (ascending order, same destination), e.g. `x4cat_extract.py "<game>\03.cat" build\orig "voice-l049/10201/normal/*"`. Without this step `tts-batch` never sees new ids, because it takes them from the `--ids-from` folder (`tools/voice_convert_elevenlabs.py:134`), and `process_audio.py` never sees new originals.
3. **Re-extract the texts** into `build/base`: `x4cat_extract.py "<game>\09.cat" build\base "t/0001-l049.xml" "t/0001-l044.xml"` → `build/base/t/…`.
4. `validate_mod.py` → selectors still match?
5. `check_coverage.py` for both languages → missing or changed lines?
6. **German repair:** `tts-batch --voice bIHbv24MWmeRgasZH58o --model eleven_v4_turbo --tfile build/base/t/0001-l049.xml --ids-from build\orig\voice-l049\10201\normal --dst build/tts/will_de` (skips existing WAVs, so only new lines cost credits), then `process_audio.py --variant will_dark --src build/tts/will_de --src-ext wav --gain-db 6 --files <new ids> --dst build/audio/will_dark_g6`. For a line whose **text** changed, delete its WAV in `build/tts/will_de` first, then run the same two commands with `--files <id>`.
7. **English repair:** `process_audio.py --variant alien_mid_50 --gain-db 4 --src build\orig\voice-l044\10201\normal --files <new ids> --dst build/audio/alien_mid_50_g4`.
8. Rebuild, validate, update the Workshop items (version above the live one, change note), add a line to the patch table in `docs/HISTORY.md`.
9. **Save the new baseline:** `check_coverage.py … --save-index` for both languages, so the next patch can report changed files.

## Where to look

`tools/check_coverage.py`, `docs/MAINTENANCE.md`, `build/index/` (ignored, created by `--save-index`).

→ Check your understanding: [quizzes/09-patch-maintenance-quiz.md](quizzes/09-patch-maintenance-quiz.md)
