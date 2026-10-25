# 12 · Cross-Cutting Concerns

> **What you'll be able to answer after this chapter:** how configuration, paths, encoding, error reporting, concurrency, security and the Windows/OneDrive environment are handled across all tools (operations, failure, security).

## Configuration and paths

| Setting | Where | Default | Used by |
|---|---|---|---|
| Game folder | `--game-dir`, else env `X4_GAME_DIR` | `C:\Steam\steamapps\common\X4 Foundations` | `validate_mod.py:28,172`, `install_mod.py:29,79`, `check_coverage.py:29,59` |
| ffmpeg | `--ffmpeg`, env `FFMPEG`, `PATH`, winget folders, `C:\ffmpeg\bin` | first found | `process_audio.py:64-74`, `voice_convert_elevenlabs.py` via import |
| ElevenLabs key | env `ELEVENLABS_API_KEY`, else `%USERPROFILE%\.elevenlabs_key` | none → exit | `voice_convert_elevenlabs.py:39-47` |
| Repository root | `Path(__file__).resolve().parent.parent` | — | every tool that touches `config/`, `dist/`, `build/` |

Repository-relative paths are resolved from the tool's location, so tools can be called from any working directory. Paths passed as arguments (`--src`, `--dst`, `--tfile`) are relative to the **current** directory.

## Invocation conventions

- Always `python -I` (isolated mode). The project venv under `build/venv` is only needed for the ElevenLabs tool (`requests`). After the move out of OneDrive the venv kept working, because `pyvenv.cfg` points at the base interpreter, not at the repository (checked 2026-10-26); launchers such as `pip.exe` embed the old absolute path, so call `build\venv\Scripts\python.exe -m pip` instead.
- On the author's machine the Windows Store `python` alias failed with "Permission denied" while this book was written (2026-10-25, not recorded elsewhere in the repository); the real interpreter is `C:\Users\slovi\AppData\Local\Python\pythoncore-3.14-64\python.exe`.
- `init.sh` assumes `python` on the `PATH` (`init.sh:6-7`).

## Output encoding and messages

All tools except `x4cat_extract.py` reconfigure `stdout` to UTF-8 with `errors="replace"`; `install_mod.py`, `process_audio.py`, `check_coverage.py` and `voice_convert_elevenlabs.py` also reconfigure `stderr`, while `build_mod.py:18-19` and `validate_mod.py:21-22` change only `stdout`. The reason: German umlauts in messages crashed or garbled in Git Bash and pipes. Messages of `install_mod.py`, `validate_mod.py` and `x4cat_extract.py` are German, the others English; this reflects the order in which they were written, not a rule.

## Error reporting

The tools follow one pattern (except `x4cat_extract.py`, which prints its docstring and exits 2 on bad arguments and otherwise lets exceptions propagate): fatal problems call `sys.exit("FEHLER: …")` or `sys.exit("ERROR: …")` with a one-line explanation of the fix; per-file problems in batch tools are counted, printed, and turned into exit code 1 at the end, while the remaining files continue (`process_audio.py:143-149`, `voice_convert_elevenlabs.py:158-167`, `validate_mod.py:179-188`). No tool writes logs; output goes to the console and is redirected to `build/*.log` by the caller when needed.

## Concurrency

Only the two batch tools are concurrent, both with a `ThreadPoolExecutor` over independent files ([ch. 6](06-audio-processing.md), [ch. 7](07-text-to-speech.md)). There are no locks and no shared mutable state; each worker writes its own output file. Running two tools against the same output folder at the same time is not guarded.

The only cross-process concern is X4 itself: the installer refuses to change the game folder while `X4.exe` runs ([ch. 8](08-installing-and-releasing.md)).

## Security and trust boundaries

| Boundary | Handling |
|---|---|
| ElevenLabs API key | read from env or a file outside the repository, sent only as a header, never printed; `.gitignore` excludes key files |
| Game files | read-only input; MD5 checked on extraction and reported by the CLI, but not reported when `validate_mod.py` extracts `sound_library.xml` (`validate_mod.py:37`) |
| XML written into the game | `content.xml` values are escaped with `quoteattr` (`build_mod.py:50`); the diff is built with unescaped f-strings (`build_mod.py:29-44`), safe only because the configuration uses plain identifiers |
| Game folder writes | every folder named `extensions/bosota_*` is deleted, whoever created it, and `extensions/<id>` is written; other mods are untouched only by naming convention (`install_mod.py:92-95`) |
| Copyrighted content | no game audio, texts or generated audio in git (`.gitignore:1-13`) |

## Windows and OneDrive specifics

The repository lived in OneDrive until 2026-10-24, which marks folders read-only. Consequences that shaped the code: in-place overwrites in `build_mod.py:69`, the read-only handling in `install_mod.py:34-47`. Since the move to `C:\#repos\github\` the workarounds are harmless but still useful if the repository goes back into a synced folder.

## Where to look

`CLAUDE.md` (rules), `docs/dev-team/LESSONS.md` (environment lessons).

→ Check your understanding: [quizzes/12-cross-cutting-concerns-quiz.md](quizzes/12-cross-cutting-concerns-quiz.md)
