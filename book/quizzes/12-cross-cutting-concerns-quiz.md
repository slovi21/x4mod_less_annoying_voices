# Quiz: Cross-Cutting Concerns

Chapter: [12 · Cross-Cutting Concerns](../12-cross-cutting-concerns.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Apply]** You run tools from `C:\temp` instead of the repository root, for example `python -I C:\#repos\github\x4mod_less_annoying_voices\tools\process_audio.py --variant will_dark --src build/tts/will_de --src-ext wav --dst build/audio/x`. Which paths are resolved against `C:\temp`?

- A) None; every path is resolved against the repository root
- B) The `--src` and `--dst` arguments; repository paths such as `config/` and `dist/` used by other tools are resolved from the script's own location
- C) All paths, including `config/variants.json` in `build_mod.py`
- D) Only `config/variants.json`

**2. [Apply]** All tools are run with `python -I`, and `init.sh:3` says the game folder comes from `X4_GAME_DIR`. Does `X4_GAME_DIR` still work under `-I`?

- A) No; `-I` hides every environment variable, so only `--game-dir` or the default path works
- B) Yes; `-I` ignores only `PYTHON*` variables and the user site directory, so `os.environ` still holds `X4_GAME_DIR` and `ELEVENLABS_API_KEY`
- C) Only inside Git Bash
- D) Only if it is also passed as `--game-dir`

**3. [Recall]** Which error-reporting pattern do the batch tools follow?

- A) The first failing file raises an exception and stops the run
- B) Fatal setup problems exit with a one-line "FEHLER"/"ERROR" message; per-file failures are printed and counted, the rest continue, and the exit code is 1 at the end
- C) Every problem is written to `build/error.log` and the exit code is always 0
- D) Failures are retried until they succeed

**4. [Recall]** What protects the two concurrent batch tools from data races?

- A) A lock around every file write
- B) Each worker writes its own output file and there is no shared mutable state; the threads mostly wait on subprocesses or HTTP
- C) The GIL serialises all ffmpeg calls
- D) Nothing, and races were observed in practice

**5. [Recall]** How is the ElevenLabs API key protected?

- A) It is stored in `config/variants.json` and masked when printed
- B) It is read from `ELEVENLABS_API_KEY` or `%USERPROFILE%\.elevenlabs_key`, sent only in the `xi-api-key` header, never printed, and key files are ignored by git
- C) It is encrypted with the Windows credential store
- D) It is passed on the command line with `--key`

**6. [Design]** Why do several tools reconfigure `stdout` (and some `stderr`) to UTF-8 with `errors="replace"`?

**7. [Design]** Which two pieces of code exist because the repository used to live in OneDrive, and what problem does each solve?

**8. [Design]** `validate_mod.py`, `check_coverage.py` and `voice_convert_elevenlabs.py` each call `sys.path.insert(0, <own folder>)` before importing a sibling module. Why is that line needed when the tools are run as `python -I tools/<tool>.py`?

---

## Answers

**1. B.** Repository paths come from `Path(__file__).resolve().parent.parent` (`tools/build_mod.py:21`, `tools/install_mod.py:28`). Argument paths are plain `Path(args.src)` (`tools/process_audio.py:125`), which Python resolves against the current directory. A and C ignore one of the two rules. D inverts them.

**2. B.** `-I` implies `-E` (ignore `PYTHON*` variables), `-s` (no user site packages) and `-P` (the script's folder is not put on `sys.path`). Ordinary variables stay visible, and the tools read them through `os.environ.get` (`tools/validate_mod.py:172`, `tools/voice_convert_elevenlabs.py:40`). The comment "no environment variables" in `init.sh:6` is shorthand for that. A takes the comment literally. C and D add conditions the code does not have.

**3. B.** Fatal problems use `sys.exit("…")` (for example `tools/install_mod.py:110`, `tools/process_audio.py:74`). Batch errors are counted and turned into exit code 1 (`tools/process_audio.py:143-149`, `tools/voice_convert_elevenlabs.py:159-167`). A is wrong except for uncaught network exceptions in `tts-batch` (`:156-158`). C is wrong because no tool writes logs. D is wrong because only HTTP 429/5xx are retried, five times (`tools/voice_convert_elevenlabs.py:83-93`).

**4. B.** Each submitted job has its own `dst` (`tools/process_audio.py:140`, `tools/voice_convert_elevenlabs.py:156`). A is wrong: there are no locks. C is wrong: ffmpeg runs in separate processes, so the GIL does not matter. D is wrong: no race has been recorded. Two tool runs into the same folder at once are simply not guarded.

**5. B.** See `tools/voice_convert_elevenlabs.py:39-47` (source), `:50-51` (header only), and `.gitignore:8-9` (`*.key`, `.elevenlabs_key`). A, C and D describe storage or options that do not exist. A key in the configuration would be committed.

**6.** German umlauts in messages crashed or came out garbled in Git Bash and in pipes, whose default encoding is not UTF-8. Reconfiguring the streams makes every message printable (`tools/install_mod.py:24-26`, `tools/build_mod.py:18-19`). Only `x4cat_extract.py` does not do it.

**7.** (1) `build_mod.py` overwrites `dist/<id>/` in place instead of deleting and recreating it, because OneDrive locked freshly created folders (`tools/build_mod.py:69`). (2) `install_mod.py` clears the read-only attribute: `rmtree_retry` with `_clear_readonly_and_retry`, and `clear_readonly_tree` after copying (`tools/install_mod.py:34-47`, `:117`). OneDrive marks folders read-only, `copytree` carries that into the game folder, and Windows then refuses `rmdir` on them (WinError 5).

**8.** Isolated mode leaves the script's own directory off `sys.path`, so `from x4cat_extract import …` or `from process_audio import …` would raise `ModuleNotFoundError`. Each tool adds its folder explicitly, right before the import (`tools/validate_mod.py:24-25`, `tools/check_coverage.py:21-22`, `tools/voice_convert_elevenlabs.py:29-30`). This keeps `-I`'s protection against stray environment and user-site packages, and the sibling imports still work.
