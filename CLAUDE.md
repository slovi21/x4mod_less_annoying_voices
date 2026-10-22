# x4mod_less_annoying_voices

**Project mode: P1** (several sessions, several milestones). Managed with the skills `anthropic-skills:projektsteuerung` and `anthropic-skills:dev-team-steuerung`. Session start: read `docs/projekt/MILESTONES.md`, `docs/projekt/CURRENT_STATE.md` and `git log`, run `./init.sh`, then report the state in five lines before taking a task.

## What this is

A mod for X4: Foundations that replaces Boso Ta's voice lines (voice set 10201) with processed copies through a redirect in `libraries/sound_library.xml`. No game audio in the repository. Verified engine facts: `docs/phase0-findings.md`. Plain-language explanation: `docs/HOW-IT-WORKS.md`. The research that started the project: `docs/X4_Boso_Ta_Voice_Mod_Handoff.md` (German, kept as the source document).

## Layout

```
config/variants.json       variants: 'alien' (German audio, recommended), 'alien_en' (English audio), 'de'/'en' (engine effects only)
tools/build_mod.py         writes dist/<id>/ (content.xml + sound_library.xml diff incl. attribute patches)
tools/validate_mod.py      checks selectors and attribute operations against the game's real sound_library.xml
tools/install_mod.py       installs exactly one variant (XML + audio from build/audio/); refuses while X4.exe runs
tools/process_audio.py     ffmpeg/Rubberband filter chains, two-pass loudness, --gain-db; --list shows variants
tools/pitch_flatten.py     Praat pre-stage (intonation range compression), runs in build/venv
tools/x4cat_extract.py     .cat/.dat extractor (text index + concatenated data, no XRCatTool needed)
dist/                      built extensions without audio (committed)
diag/                      diagnostic extension that proved the audio redirect
build/                     extracted game files, processed audio, samples, venv, Workshop staging – ignored
docs/projekt/              MILESTONES.md, CURRENT_STATE.md
docs/dev-team/             ROUTING-LOG.md, LESSONS.md
```

## Commands

```bash
python -I tools/process_audio.py --variant d12_alien_mid --gain-db 9 --src <originals> --dst build/audio/d12_alien_mid_g9
python -I tools/build_mod.py            # build all variants
python -I tools/validate_mod.py         # check against the game (mandatory before install)
python -I tools/install_mod.py alien    # alien | alien_en | de | en; --remove deletes every bosota_*
```

`-I` is Python's isolated mode. Game folder via `--game-dir` or `X4_GAME_DIR`, default `C:\Steam\steamapps\common\X4 Foundations`. ffmpeg: full build (`winget install Gyan.FFmpeg`), located under `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\...\bin\` and not on the tool shell's PATH (`--ffmpeg <path>`).

## Rules

- **Talk to Slovi in German. Write project documentation, commit messages and this file in English.** Every shell command shown to Slovi is explained option by option. His console is Windows PowerShell 5.1: no `grep`, no `&&`.
- Never commit Egosoft files (audio, extracted XML); `build/` stays ignored.
- Only one variant may be installed in the game; all of them patch the same sound ids.
- Change parameters only in `config/variants.json`, then build and validate; never edit `dist/` by hand.
- Never install or remove a mod while `X4.exe` is running (the installer enforces it).
- Do not commit or push without being asked.

## Routing paths

| Touches | Minimum level |
|---|---|
| `tools/install_mod.py` (deletes folders in the game directory) | S2 |
| Sound id lists in `config/variants.json` (a wrong id fails silently in the game) | S2 |

## Listening method (proven)

Slovi decides by ear, not by numbers, and has poor hearing. WAV samples via SendUserFile in rounds, one question per round, all samples at −22 LUFS, the reference always included. **Judge level and intelligibility only in the game**, never on PC playback: station ambience and positional audio change everything.

## Game facts (verified 2026-10-22, X4 9.00)

- Boso Ta = page **10201**, shared only with the Boron faction representative. Six sound ids `10201_normal|normal_npc|comm|comm_signalleak|comm_npc|comm_broadcast`, none with effects in the base game.
- The engine takes a redirected `<sample start>` path literally (no language suffix). One mod per voice track; only `voice-l044` and `voice-l049` exist.
- `<effects>` offers `doppler`, `fade`, `filter`, `reverb`, `pitch(start,end,steps)`; no equalizer; pitch is resampling.
- Conversations need `is3d="0"` and `noocclusion="true"` for a dark processed voice to stay intelligible.
- User folder `C:\Users\slovi\OneDrive\Documents\Egosoft\X4\34818113\`, enable table `content-MSI-PRODP20Z.xml`. Any unsigned extension marks the game as modified; `save="0"` does not change that.
