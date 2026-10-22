# Current state

**Milestone:** 5 in progress (packaging and distribution). Milestones 1, 2, 3, 4 and 6 reached on 2026-10-22.

## Installed in the game right now
`bosota_voice_will_de` – the new German voice (ElevenLabs "Will", Eleven v4 Turbo, `will_dark` + 6 dB, folder `build/audio/will_dark_g6`, −16.0 LUFS, 2,324 files incl. 5 Alien fallbacks). Installed 2026-10-22 after the TTS batch (2,319 lines, 0 failures). Actual credit use: 40,286 for the whole German run including samples; 85,660 credits remain on the Creator plan, enough for an English Will run (129,232 characters) if wanted. Slovi: "passt gut".

## Release packages (2026-10-22)
- DE Workshop: `build/workshop/stage2/extensions/ws_3824406333` (Will, version 102) → `WorkshopTool update`, see `docs/RELEASE.md`.
- DE ModDB: `C:\Users\slovi\Desktop\Boso_Ta_less_annoying_VOICE_DE_v1.0.zip` (folder `bosota_voice_will_de`).
- EN Workshop: `build/workshop/stage1_en/extensions/bosota_voice_alien_en` → first `publishx4`, then a `ws_<number>` variant.
- EN ModDB: `C:\Users\slovi\Desktop\Boso_Ta_less_annoying_VOICE_EN_v1.0.zip` (folder `bosota_voice_alien_en`, +4 dB).
- Previews `build/workshop/preview_DE.jpg`, `preview_EN.jpg`; description `docs/release/MODDB_DESCRIPTION.md`; patch procedure `docs/MAINTENANCE.md`; coverage indexes saved under `build/index/`.

## Done
- German variant `alien`: `d12_alien_mid` + 9 dB (one octave down, formants shifted, frequency shift −70 Hz, chorus, mid-range focus 220 Hz–5.5 kHz with +4 dB at 1.4 kHz and +2 dB at 2.8 kHz, gentle compression), `is3d="0"` on both conversation entries, `noocclusion="true"` on five entries. Slovi: "that works now, I can start a new game without being annoyed by Boso".
- English variant `alien_en`: same chain at half strength (6 semitones, −35 Hz, half chorus), full mid-range focus, +4 dB.
- Pipeline: `x4cat_extract.py` → `process_audio.py` (ffmpeg/Rubberband, two-pass loudness to −22 LUFS, optional gain with limiter) → `build_mod.py` (redirect diff plus attribute patches) → `validate_mod.py` → `install_mod.py` (refuses to run while `X4.exe` is open).
- Workshop preparation: staging copies in `build/workshop/stage1/extensions/bosota_voice_alien` (DE) and `build/workshop/stage1_en/extensions/bosota_voice_alien_en` (EN), preview image `build/workshop/preview.jpg`, X Tools installed at `C:\Steam\steamapps\common\X Tools`.
- Documentation rewritten in English (README, HOW-IT-WORKS, phase0-findings, these project files, LESSONS, CLAUDE.md). The original German handoff is kept as the source document.

## New direction (2026-10-22, later the same day): complete new voice for German via text-to-speech
- Speech-to-speech (ElevenLabs Voice Changer) was tried with all 21 premade voices on one line: rejected by Slovi, every result carried the original actor's Saxon colouring. Text-to-speech from the game texts avoids it; lip sync is explicitly unimportant to Slovi.
- Texts: page 10201 of `t/0001-l049.xml` holds every line under the same id as the audio file; stage directions in parentheses are stripped. 2,319 of 2,324 lines have text (183,227 characters); alternate takes `…fp` reuse the base text; 5 ids without text (10417, 10603, 30226001–3) keep the previous Alien audio.
- Choice: voice **Will** (`bIHbv24MWmeRgasZH58o`), model **Eleven v4 Turbo** (0.5 credits per character), post-processing `will_dark` (−4 semitones formants shifted, +4 dB low shelf 220 Hz, −4 dB high shelf 4 kHz), sample `7_will_minus4_warm_v4_turbo.wav`. English stays on the existing Alien variant.
- Account: Creator plan, 125,946 credits at start; need ≈ 92,000. Key file `%USERPROFILE%\.elevenlabs_key`; the first key was exposed in chat and must be rotated.
- Tooling: `tools/voice_convert_elevenlabs.py` (`quota`, `voices`, `convert`, `tts`, `tts-batch`, resumable), venv `build/venv` with requests. Batch run started into `build/tts/will_de/` (log `build/tts_will_de.log`).

## Open
- Finish the TTS batch, post-process with `will_dark` + loudness + gain, fall back to Alien audio for the 5 textless ids, build variant, test in game.
- Confirm the English level (+4 dB) in the game, then switch back to German.
- Workshop, German item: first upload done 2026-10-22, **item id 3824406333** (hidden). Variant `alien_ws` (`ws_3824406333`, version 101) built and staged under `build/workshop/stage2/extensions/ws_3824406333/`; the `update` upload with the corrected redirect path is the next step, then set visibility. English item not yet created (same procedure with `stage1_en`).
- GitHub release and ModDB upload of the packaged folders, if Slovi decides to publish.
- Optional: separate radio-filtered set for the comm contexts; code comments in `tools/` are still German.

## Decisions
- Engine effects (plan A) rejected: pitch is resampling, Slovi could not perceive −3 semitones and still found −9 unpleasant.
- AI voice conversion (ElevenLabs, RVC) presented and not chosen; ffmpeg processing with listening rounds was sufficient.
- Conversations play in 2D because head orientation changed loudness from 90 % to 60 % of Karee's and destroyed intelligibility.
- All six contexts point at the processed `normal` set; the original radio filter of the comm files is dropped.
- One variant per voice language, because the redirect path is language independent.

## Known risks
- The Boron faction representative shares the voice set and gets the new voice.
- Background chatter (`normal_npc`) is 2D and therefore equally loud everywhere on the platform.
- Levels are limiter-bound (peaks at −0.3 to −1.5 dBTP); further gain would be audible.
- Publishing processed Egosoft audio is a grey area; the repository deliberately contains none.

## Next sensible step
Slovi confirms the English level, switches back to German, commits. Then the first hidden Workshop upload.

## Evidence
- `python -I tools/validate_mod.py` → 0 errors in 4 extensions (2026-10-22)
- `build/process_*.log` → every full run "0 Fehler"
- Slovi's listening verdicts, recorded per round in `docs/dev-team/LESSONS.md`
