# Routing log

One line per task from level S1 upwards, written by the orchestrator.

| Date | Task (short) | Level initial | Level final | Escalation trigger | Optional roles (trigger) | Failed attempts | Effort/model change | Tokens (rough) | Remarks |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-22 | Phase 0 (verification against the game) plus mod scaffold: generator, validator, installer, three variants | S1 | S1 | – | none | 0 | – | ~250k | Orchestrator did it directly instead of `implementierer`: all context (catalog findings) was here and the files were small; review replaced by a deterministic validator against the real game file. Large Bash heredocs failed → Write tool. Installer fixed twice (OneDrive read-only attribute). |
| 2026-10-22 | Debugging "no audible difference" (systematic-debugging): log analysis, diagnostic build with three independent observations, speaker analysis of set 10201 | S1 | S1 | – | none | 0 | – | ~120k | Result depended on Slovi's listening test. |
| 2026-10-22 | Plan B: audio pipeline (ffmpeg/Rubberband, loudness, gain), redirect variant, attribute patches, nine listening rounds, six full renders until "works" | S2 | S2 | scope (new dependencies ffmpeg, parselmouth) | none; review by validator and Slovi's in-game tests | 2 (heredoc escapes, acompressor makeup) | – | ~700k | Direction changed by Slovi (different voice instead of effect). Most of the effort was iteration by ear, not code. |
| 2026-10-22 | English variant at half strength, Workshop preparation (staging folders, preview image, X Tools), installer guard against a running game, documentation rewritten in English | S1 | S1 | – | none | 1 (mod swapped while the game was running) | – | ~250k | The failed attempt produced the "never swap while running" lesson and the installer guard. |
