# Development history

One day of work, 2026-10-22, from a research handoff to two published Workshop items. This page keeps the path, including the dead ends, so the repository itself can stay lean. Commits are on `main`.

## Starting point

A German research handoff (kept in git history as `docs/X4_Boso_Ta_Voice_Mod_Handoff.md`, removed from the tree on clean-up) proposed to make Boso Ta's voice "deeper and warmer" purely through engine effects in `sound_library.xml`, with a processed-audio redirect as plan B and AI voice conversion as a later option. Its research into catalog format, voice paths and mod loading held up; its guesses about Boso Ta's voice page and about effects on speech had to be verified.

## Phase 0 – verification (commit `152a8db`)

Extracted `sound_library.xml`, its XSD, the text files and all mission scripts straight from the catalogs with a 90-line extractor. Found the voice page (10201) through the speak ids in the mission scripts, the six sound entries, the effect schema (filter, reverb, pitch; no equalizer) and that no DLC touches the entries. Built generator, validator and installer; the installer had to learn about OneDrive's read-only folder attribute.

## Plan A – engine effects (abandoned)

| Build | What it did | Slovi's verdict |
|---|---|---|
| test (pitch 0.841, low-pass 0.25, also on Betty) | first in-game attempt | "no difference" |
| diag v1 (volume 0.03 on one entry) | prove the diff is applied | "Boso is very quiet" → proven |
| diag v2–v4 (pitch 0.3–0.6, filters, 2D) | isolate pitch and filter effects | inconclusive; comm path not findable, hearing coarse |
| diag v5 (pitch 0.3 on the flight-school tutor) | fast test bed | "extremely slow and deep" → pitch works on speech |
| de (pitch 0.75, low-pass 0.2) | first real variant | "slower and quieter, still unpleasantly squeaky" |

Conclusion: resampling pitch cannot go deep enough without slowing speech, and the squeak survives. Slovi asked for a different voice.

## Plan B – processed originals (shipped for English)

| Build | Chain | Verdict |
|---|---|---|
| diag v6 (tutor redirected to Betty/Boso files) | prove the audio redirect | tutor spoke with Betty's voice → path taken literally, folder `voice` |
| round 1: deep7, deep7big, deep12big, computer, computer2 | pitch and robot chains | deep12big best, everything else "too close to the squeak" |
| round 2: deep14/16, computer, ringmod, choir, alien, whisper, underwater | effect families on deep12big | alien best; whisper and ringmod noisy; underwater echo too strong, theme fits |
| round 3–4: alien_tank, strengths 70/60/50 % | fine tuning | tank best; weaker strengths let the squeak back in at high notes |
| round 5–6: multiband compressor, split, Praat pitch-range compression | treat only the high notes | tried; Slovi returned to full-strength alien |
| round 7: octave steps | 1.5, 2, 3, 4 octaves | 1.5 chosen, later "too much" |
| full sets: tank_oct1.5 (−22 LUFS), +6 dB, alien_tank +6 dB, d12_alien +9 dB | in-game level and intelligibility | "far too quiet" → "60 %, unintelligible" → "70 %, unintelligible" → "90 % facing, 60 % back turned" |
| d12_alien_mid +9 dB, `is3d="0"`, `noocclusion="true"` | mid-range focus, no positional audio | **"that works now"** → German plan B result |
| alien_mid_50 +4 dB on the English originals | half strength | **"fits"** → published English variant |

Measurement lessons: equal LUFS is not equal perceived loudness (11 dB missing above 1 kHz); positional audio and occlusion wreck a dark voice; judge levels only in the game.

## Plan C – text-to-speech (shipped for German)

Speech-to-speech with all 21 ElevenLabs premade voices kept the original actor's Saxon colouring; rejected. Text-to-speech from the game texts (page 10201 holds every line under the audio file's id) does not. Slovi chose the voice Will, model Eleven v4 Turbo, darkened by 4 semitones with warmth (`will_dark`), +6 dB. 2,319 lines, 0 failures, 40,286 credits in total (≈ 0.2 credits per character, far below the published 0.5). Five ids without text keep the Alien audio. Verdict: "passt gut".

## Release (commits `2045ac3`, `32aafbb`)

- Workshop DE item 3824406333: created with the Alien audio, updated to the Will voice (version 102).
- Workshop EN item 3824446410: creating it together with the audio timed out twice (Steam error 16); created XML-only, audio added with `update`; the first update failed with error 9 while `-preview` was passed.
- ModDB package assembled under `build/moddb_package/`.

## Removed on clean-up (2026-10-22, after release)

| Removed | Why | Where it lives now |
|---|---|---|
| `diag/` (diagnostic extension v1–v7) | served its purpose | this page, `docs/phase0-findings.md` |
| `dist/bosota_warm_de`, `dist/bosota_warm_en`, variants `de`/`en`, the effects branch of `build_mod.py` | plan A, not good enough | this page |
| experimental filter chains in `process_audio.py` (deep7 … whisper, tank, octave steps, hicut, split, scaled strengths other than 50 %) | listening-round material | table above; git history |
| `tools/pitch_flatten.py` (Praat pre-stage) | tried in round 5–6, not used | git history |
| speech-to-speech subcommand `convert` in `voice_convert_elevenlabs.py` | rejected approach | git history |
| `docs/X4_Boso_Ta_Voice_Mod_Handoff.md` (German research handoff) | superseded by `phase0-findings.md` and this page | git history, commit `152a8db` |

## Patch history

| Date | Game version | Change |
|---|---|---|
| 2026-10-22 | 9.00 | initial release, both items hidden; DE item verified via Workshop subscription |

After a game patch, follow `docs/MAINTENANCE.md` and add a line here.
