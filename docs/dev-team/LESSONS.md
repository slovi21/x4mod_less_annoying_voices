# Lessons learned

Durable, non-obvious findings with evidence. One-offs and generalities do not belong here.

## Working with Slovi

- **Decide by ear, in rounds.** Slovi judges sound, not numbers, and has, in his own words, poor hearing. What worked: WAV samples sent in rounds of four to ten, one question per round, every sample normalised to −22 LUFS, the current favourite always included as a reference. Nine rounds took the project from engine effects to "Alien with mid-range focus" in one session.
- **Judge level and intelligibility only in the game.** A sample that sounds as loud as the original on the PC can still vanish under station ambience and positional audio. Three full renders were spent on level alone.
- **Make diagnostics coarse.** −3 semitones went unnoticed; a volume of 0.03 and a pitch of 0.3 were unmistakable. Use changes that alter duration or loudness, not timbre.
- **His console is Windows PowerShell 5.1.** No `grep`, no `&&`; use `Select-String` and `;` or `if ($?) { … }`. Every command he is shown gets each option explained. He talks to the assistant in German; project documentation is written in English.

## Tooling and environment

- **OneDrive marks folders read-only.** Directories under `OneDrive\Documents\#repos` carry the `R` attribute. `shutil.rmtree` fails with WinError 5 on the `rmdir` even though the files are gone, and `shutil.copytree` copies the attribute to the target. Overwrite in place instead of deleting; when deleting, use an `onexc` handler that calls `os.chmod(path, stat.S_IWRITE)`; clear the attribute on the target after copying. Bash `rm -rf` and PowerShell `Remove-Item -Force` are unaffected.
- **Never build backslash paths inside Python strings fed through a heredoc.** `\b`, `\v` and `\1` were interpreted as escapes and wrecked an XML diff (`extensionsosota…`). Write such files with the Write tool or raw strings.
- **Large Bash heredocs failed in the tool shell** with "unexpected EOF while looking for matching quote". Create big files with the Write tool.
- **ffmpeg from winget is not on the tool shell's PATH.** It lives under `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\ffmpeg-9.0.2-full_build\bin\`; `process_audio.py` finds it there, or pass `--ffmpeg`.
- **`acompressor` rejects `makeup=0`**; the valid range is 1–64 (a multiplier). Leave it out.
- **`x4cat_extract.parse_cat` skips malformed index lines silently** and reads with `errors="replace"` (`tools/x4cat_extract.py`, `parse_cat`). Fine for extraction, wrong for any check whose verdict must not miss a file: `tools/classify_extension.py` therefore has its own strict, fail-closed parser.
- **`os.walk` silently skips folders it cannot list** (access denied, path too long, names Win32 cannot open). Any scan whose verdict must not miss a file passes `onerror` and counts the error against the result. Tested by patching `os.scandir` (`tests/test_classify_extension.py`, `test_unreadable_folder_fails_closed`).
- **Before Python 3.12 there is no `os.path.isjunction`, and `islink()` is False for junctions.** Detect them with `os.lstat(p).st_reparse_tag == stat.IO_REPARSE_TAG_MOUNT_POINT`. Do not test for "any reparse point": OneDrive placeholders are reparse points as well.
- **`tasklist` prints in the OEM code page.** Decode its output as bytes and search for ASCII, or Python's default cp1252 decoder throws.

## Audio

- **LUFS normalisation is not enough for a heavily lowered, low-passed voice.** Boso Ta at −18 semitones with a 2.2 kHz low-pass measured the same integrated loudness as the original (−22 LUFS) and 3 dB more RMS, yet was "far too quiet" in the game: above 1 kHz it carried 11 dB less energy, and that band is what makes speech sound loud and close. Fix: add gain after normalisation with a limiter (`--gain-db`), restore presence with a mid-range focus, and do not go deeper than one octave.
- **Rubberband adds about 60 ms of latency** to every file. Harmless for dialogue and lip sync.
- **Measured levels of the final variants:** German −14.7 LUFS at −0.3 dBTP (+9 dB), English −18.2 LUFS at −1.5 dBTP (+4 dB).

## ElevenLabs

- **Eleven v4 Turbo cost far less than the published 0.5 credits per character.** The German batch (2,319 lines, 183,227 characters after stripping stage directions) plus about 60 test generations consumed 40,286 credits in total, roughly 0.2 credits per character. Budget with the published rate, expect to spend less. *(Creator plan, 2026-10-22: 125,946 → 85,660 credits.)*
- **Speech-to-speech keeps the source actor's regional colouring.** All 21 premade voices converted from the German Boso Ta recordings carried the actor's Saxon intonation; text-to-speech from the game texts does not. Lip sync is lost with TTS, which Slovi accepted.
- **Library voices (professional voice clones) are blocked on the free plan via the API** (HTTP 402 "paid_plan_required"); premade voices work. The `/user/subscription` endpoint needs a key with user-read permission, otherwise 401 while TTS still works.
- **Game texts for TTS:** page 10201 of `t/0001-l0xx.xml` holds every line under the same id as the audio file; alternate takes (`…fp`) share the base id's text; a handful of ids have no text and keep processed original audio.

## X4 modding

- **Boso Ta has no voice page of his own.** He speaks through set `10201`, assigned per actor in the mission scripts, and the page is stored in the save. Speaker pages are not found by character name in the text files; look up the `$speak` ids from the mission scripts, which reappear as file names under `voice-l0xx/<page>/<context>/`.
- **The extension enable table in the user folder is machine specific:** `content-<computer name>.xml`, here `content-MSI-PRODP20Z.xml`.
- **`<effects><pitch start end steps/>` works on speech** and is a resampling factor: tempo changes with it.
- **`<replace sel=".../volume">` is the surest proof that a diff is applied.**
- **The audio redirect works and the path is taken literally.** `<sample start="extensions\<mod>\voice\<page>\<context>"/>` loads `extensions\<mod>\voice\<page>\<context>\<line>.ogg`; no language suffix is inserted. Consequence: one mod can serve only one voice track.
- **Positional audio and occlusion can make a dark voice unintelligible.** Bit-identical files sounded fine facing the speaker and unintelligible with the back turned. `noocclusion="true"` and `is3d="0"` on the conversation entries fixed it; bright original voices survive both without anyone noticing.
- **Attribute patches:** `<add sel="…" type="@name">value</add>` creates an attribute, `<replace sel="…/@name">value</replace>` changes an existing one; adding an existing attribute is an error (`10201_comm_signalleak` already has `noocclusion`).
- **Never swap a mod while X4 is running.** The game reads the diff at start-up; delete the audio folder afterwards and the voice goes silent without a log entry. `install_mod.py` now refuses while `X4.exe` is running.
- **The English track of set 10201 lacks the pilot and crew phrases** (ids 10001 and up). Greetings and small talk exist in both languages. Other sets (10101, 10202) are complete in both.
- **Fast test bed:** the flight-school tutorials load in seconds and the Argon tutor (page 10190) speaks immediately. Use them for speaker-independent questions; use Boso Ta only for the final tuning. The only scenario with Boso Ta as narrator (`x4ep1_gamestart_tutorial2`) is hidden behind `debug="true"`.
- **Launch options:** `-skipintro`, `-logfile debuglog.txt` (also makes script errors flash on screen), `-debug all` (slow, only needed for file I/O messages), `-voicelanguage 44|49`.
