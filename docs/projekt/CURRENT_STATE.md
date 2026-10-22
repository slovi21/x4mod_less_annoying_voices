# Current state

**Milestone:** 5 in progress (packaging and distribution). Milestones 1, 2, 3, 4 and 6 reached on 2026-10-22.

## Installed in the game right now
`bosota_voice_alien_en` – the English variant (`alien_mid_50` + 4 dB, folder `build/audio/alien_mid_50_g4`, −18.2 LUFS). It was installed for Slovi's English test with `-voicelanguage 44`. Slovi's verdict at +6 dB: "voice fits, about 20 % too loud", hence the drop to +4 dB; the check of that final level is still open. To return to German: close the game, run `python -I tools/install_mod.py alien`, remove `-voicelanguage 44` from the launch options.

## Done
- German variant `alien`: `d12_alien_mid` + 9 dB (one octave down, formants shifted, frequency shift −70 Hz, chorus, mid-range focus 220 Hz–5.5 kHz with +4 dB at 1.4 kHz and +2 dB at 2.8 kHz, gentle compression), `is3d="0"` on both conversation entries, `noocclusion="true"` on five entries. Slovi: "that works now, I can start a new game without being annoyed by Boso".
- English variant `alien_en`: same chain at half strength (6 semitones, −35 Hz, half chorus), full mid-range focus, +4 dB.
- Pipeline: `x4cat_extract.py` → `process_audio.py` (ffmpeg/Rubberband, two-pass loudness to −22 LUFS, optional gain with limiter) → `build_mod.py` (redirect diff plus attribute patches) → `validate_mod.py` → `install_mod.py` (refuses to run while `X4.exe` is open).
- Workshop preparation: staging copies in `build/workshop/stage1/extensions/bosota_voice_alien` (DE) and `build/workshop/stage1_en/extensions/bosota_voice_alien_en` (EN), preview image `build/workshop/preview.jpg`, X Tools installed at `C:\Steam\steamapps\common\X Tools`.
- Documentation rewritten in English (README, HOW-IT-WORKS, phase0-findings, these project files, LESSONS, CLAUDE.md). The original German handoff is kept as the source document.

## Open
- Confirm the English level (+4 dB) in the game, then switch back to German.
- Workshop upload (Slovi runs the tool): publish hidden → read `ws_<number>` → add a variant with that id → `update`. One item per voice track.
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
