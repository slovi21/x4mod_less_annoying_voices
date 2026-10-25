# The Boso Ta Voice Mod — Codebase Book

A reference for maintaining `x4mod_less_annoying_voices`, the factory that produces the X4: Foundations mod "Boso Ta – less annoying VOICE". Written 2026-10-25 against commit `7a874f9` plus the fixes listed under "Findings while writing". Reader: an engineer who has never seen the repository and must be able to rebuild, release and repair the mod.

## Table of contents

| # | Chapter | In one line | Quiz |
|---|---|---|---|
| 0 | [Start Here](00-start-here.md) | What it is, how to run it, the five ideas, first change | [quiz](quizzes/00-start-here-quiz.md) |
| 1 | [The Big Picture](01-the-big-picture.md) | Pipeline of file-based tools, boundaries, load-bearing decisions | [quiz](quizzes/01-the-big-picture-quiz.md) |
| 2 | [Core Concepts](02-core-concepts.md) | Voice pages, contexts, line ids, sound entries, variants | [quiz](quizzes/02-core-concepts-quiz.md) |
| 3 | [Game Archives & Extraction](03-game-archives-and-extraction.md) | `.cat/.dat` format and `x4cat_extract.py` | [quiz](quizzes/03-game-archives-and-extraction-quiz.md) |
| 4 | [Variants & Configuration](04-variants-configuration.md) | `config/variants.json` schema and the five variants | [quiz](quizzes/04-variants-configuration-quiz.md) |
| 5 | [Building & Validating](05-building-and-validating.md) | The generated diff and its offline replay | [quiz](quizzes/05-building-and-validating-quiz.md) |
| 6 | [Audio Processing](06-audio-processing.md) | ffmpeg chains, loudness, gain | [quiz](quizzes/06-audio-processing-quiz.md) |
| 7 | [Text-to-Speech](07-text-to-speech.md) | ElevenLabs batch generation from game texts | [quiz](quizzes/07-text-to-speech-quiz.md) |
| 8 | [Installing & Releasing](08-installing-and-releasing.md) | Installer guards, Workshop, ModDB, modpub | [quiz](quizzes/08-installing-and-releasing-quiz.md) |
| 9 | [Patch Maintenance](09-patch-maintenance.md) | Coverage check and the post-patch procedure | [quiz](quizzes/09-patch-maintenance-quiz.md) |
| 10 | [Data Model & Files](10-data-model.md) | Every file, who writes and reads it, invariants | [quiz](quizzes/10-data-model-quiz.md) |
| 11 | [Key Flows](11-key-flows.md) | End-to-end builds, in-game playback, release, repair | [quiz](quizzes/11-key-flows-quiz.md) |
| 12 | [Cross-Cutting Concerns](12-cross-cutting-concerns.md) | Paths, encoding, errors, concurrency, security, Windows | [quiz](quizzes/12-cross-cutting-concerns-quiz.md) |
| 13 | [Failure Modes](13-failure-modes.md) | Symptom → cause → detection → fix | [quiz](quizzes/13-failure-modes-quiz.md) |
| 14 | [How Do I…?](14-how-do-i.md) | Change recipes | [quiz](quizzes/14-how-do-i-quiz.md) |
| 15 | [Glossary](15-glossary.md) | Terms | — |
| — | [Final Exam](quizzes/16-final-exam.md) | Interleaved questions across all chapters | — |

## Coverage map

| Cluster | Chapter | Depth |
|---|---|---|
| `tools/x4cat_extract.py` | 3 | full |
| `config/variants.json` | 4 | full |
| `tools/build_mod.py` | 5 | full |
| `tools/validate_mod.py` | 5 | full |
| `tools/process_audio.py` | 6 | full |
| `tools/voice_convert_elevenlabs.py` | 7 | full |
| `tools/install_mod.py` | 8 | full |
| `tools/check_coverage.py` | 9 | full |
| `dist/*` | 4, 5, 10 | generated output, described by its generator |
| `init.sh` | 0, 5, 12 | two-line wrapper |
| `release/mod.yaml`, `release/out/*` | 8, 10 | manifest and texts for an external tool; tool itself out of scope |
| `docs/*` | referenced throughout | project documentation, not code |
| `.gitignore` | 10, 12 | what stays out of git |
| `CLAUDE.md`, `README.md` | 0 | entry documents |

Entry points: the seven CLIs in `tools/` (`main()` in each) and `init.sh`. There are no tests in the repository; `validate_mod.py` and `check_coverage.py` are the executable checks.

## Findings while writing (fixed in the working tree, not yet committed)

1. **Installer regression:** since the clean-up commit `e5a7438`, `tools/install_mod.py` copied audio only for variants with `kind == "audio"`, a field that clean-up had removed. Installs succeeded without any audio, which would leave Boso silent. Fixed: audio is always copied and checked before anything is written. The Workshop items were built earlier and are not affected.
2. **Corrupted configuration strings:** `config/variants.json` contained control characters in one `_doc` entry and two `audio_recipe` strings (backslash escapes from a shell heredoc). Repaired.
3. **Stale help text:** `tools/voice_convert_elevenlabs.py` still documented the removed `convert` command. Replaced with `tts` and `tts-batch`.
4. **Wrong catalog in the repository README:** it told readers to extract Boso Ta's lines from `01.cat`; they are in `03.cat` (the texts in `09.cat`). Corrected in `README.md`.
5. **Wrong `-I` description:** `README.md` and `init.sh` said isolated mode ignores all environment variables; it ignores only `PYTHON*` variables, so `X4_GAME_DIR` still works. Corrected.
6. **Steam achievements:** the user texts claimed that mods cost Steam achievements. Player reports say they still unlock; only the online Ventures are blocked. Corrected in `README.md` and in this book ([ch. 8](08-installing-and-releasing.md)); the other user texts are unchanged pending a decision.
7. **Workshop install location:** `docs/RELEASE.md` and `docs/projekt/CURRENT_STATE.md` placed subscribed items in the user folder; they are in the game's `extensions` folder. Corrected.

Found by the audit and documented, not changed in code: the installer crashes with `FileExistsError` when a `ws_*` target exists; the diff is not XML-escaped; a wrong game folder makes `check_coverage.py` pass with 0 lines; network exceptions in `tts-batch` do not stop queued requests. See [Failure Modes](13-failure-modes.md).

## Residual open questions

- Behaviour of the external modpub tool (other repository).
- Exact semantics of Egosoft's diff engine beyond what the validator replays.
- ElevenLabs billing rate for Eleven v4 Turbo (measured 0.2, published 0.5 credits per character).
