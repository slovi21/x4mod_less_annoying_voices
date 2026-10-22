# Boso Ta – less annoying VOICE

A mod for **X4: Foundations 9.00** that makes the Boron scientist **Boso Ta** bearable to listen to. His original voice is extremely high and squeaky in both the German and the English voice track. This mod replaces his lines with processed copies: one octave lower, an alien timbre, a mid-range emphasis so he stays intelligible, and playback that no longer depends on where you are standing. Timing, pauses and lip sync are untouched because the pitch is changed without changing the tempo.

Two things are worth knowing before you install anything:

- **The game will count as modified.** Every mod that is not signed by Egosoft does this. You lose Steam achievements and online Ventures for any save you make while the mod is active, and the save keeps that mark even if you remove the mod later. The `save="0"` attribute in the mod's `content.xml` only means the save file does not list the mod as a requirement, so you can uninstall without warnings.
- **The repository contains no game audio.** The processed files are copies of Egosoft's recordings and are not published here. You generate them on your own machine from your own installation (about ten minutes), or you receive them as part of a packaged release.

Boso Ta speaks through voice set `10201`. The only other character wired to that set is the Boron faction representative, voiced by the same actor, so he changes too. Random NPCs are not affected.

## Variants

| Key | Kind | What you get |
|---|---|---|
| `alien` | audio redirect | **German voice track.** Full strength: 12 semitones down, formants shifted, frequency shift, chorus, mid-range focus, +9 dB. |
| `alien_en` | audio redirect | **English voice track.** Half strength: 6 semitones down, half the frequency shift and chorus, same mid-range focus, +4 dB. The English original is less shrill, so it needs less correction. |
| `de`, `en` | engine effects only | Pitch via resampling (which also slows the speech) plus a low-pass filter. No audio files needed. Kept as a lightweight fallback; it was not enough for the author. |

Only one variant can be active at a time. They all rewrite the same six sound entries. The audio variants are tied to one voice language each, because the redirect in `sound_library.xml` is language independent: an English player with the German variant would hear processed German lines.

## How it works, in one paragraph

X4 keeps an index, `libraries/sound_library.xml`, that tells the engine where each character's voice files live and how to play them. The mod patches the six entries `10201_*` with an XML diff so they point at the mod's own folder, `extensions\<mod id>\voice\10201\normal\`, which holds the processed `.ogg` files under their original line IDs. The same diff sets `noocclusion="true"` (no muffling through the glass of his tank) and `is3d="0"` on the conversation entries (no attenuation when you turn away). The engine loads the redirected path literally; it does not insert a language suffix. See `docs/HOW-IT-WORKS.md` for a non-technical explanation and `docs/phase0-findings.md` for the verified facts behind every one of these statements.

## Building it yourself (Windows, PowerShell)

You need Python 3 and a full ffmpeg build that includes the Rubberband filter:

```powershell
winget install Gyan.FFmpeg
```

`winget` is the Windows package manager, `install` installs a package, and `Gyan.FFmpeg` is the full build from gyan.dev. Open a new console afterwards so the path is picked up.

**1. Extract Boso Ta's original lines from your game.** The catalogs `01.cat` … `09.cat` are plain text indexes next to `.dat` files with the raw data; later catalogs override earlier ones, so run this for every catalog that contains the folder (in 9.00 the lines live in `01.cat`):

```powershell
python -I tools/x4cat_extract.py "C:\Steam\steamapps\common\X4 Foundations\01.cat" build\orig "voice-l049/10201/normal/*"
```

`-I` runs Python in isolated mode (no environment variables, no user site packages). The arguments are the catalog, the output folder, and a path prefix; use `voice-l044/...` for the English track.

**2. Process the audio.** The recipe for each variant is stored in `config/variants.json` under `audio_recipe`. For German:

```powershell
python -I tools/process_audio.py --variant d12_alien_mid --gain-db 9 --src build\orig\voice-l049\10201\normal --dst build\audio\d12_alien_mid_g9
```

`--variant` selects the filter chain (`--list` shows all of them), `--gain-db` adds level after loudness normalisation with a limiter at −1 dBFS, `--src` is the folder of originals, `--dst` is the folder the configuration expects. About ten minutes on eight cores. For English use `--variant alien_mid_50 --gain-db 4` on the `voice-l044` files and write to `build\audio\alien_mid_50_g4`.

**3. Build, validate, install.**

```powershell
python -I tools/build_mod.py; python -I tools/validate_mod.py; python -I tools/install_mod.py alien
```

`build_mod.py` writes the extension folders (XML only) to `dist/`. `validate_mod.py` extracts the real `sound_library.xml` from your game and checks that every selector hits exactly one node and that no attribute is added twice. `install_mod.py` removes every `bosota_*` folder from the game's `extensions` directory, copies the chosen variant, and adds the audio from `build/audio/`. It refuses to run while `X4.exe` is open, because the running game would keep looking for files you just deleted. Use `alien_en` for the English variant. A different game location can be passed with `--game-dir` or the `X4_GAME_DIR` environment variable.

In the game, open Extensions from the main menu and check that "Boso Ta – less annoying VOICE (DE)" or "(EN)" is listed and enabled.

**Uninstall:** `python -I tools/install_mod.py --remove`, or delete the folder under `extensions`.

## Listening to the other voice track

X4 lets you pick the voice language independently of the interface language. Add `-voicelanguage 44` to the Steam launch options for English speech or `-voicelanguage 49` for German; menus and subtitles keep their language. Install the matching variant first.

## Tuning

`python -I tools/process_audio.py --list` prints every filter chain: plain pitch drops, computer voices, ring modulation, a doubled voice, the alien chain, whisper, underwater, the mid-range focus, octave steps and scaled strengths. Render a few lines with `--files <id,id> --wav` and listen to them on the PC to judge character. Judge **loudness and intelligibility only inside the game**: a dark voice sounds just as loud as the original on headphones and still disappears under the station ambience in the game. `tools/pitch_flatten.py` (Praat, in its own environment under `build/venv`) can compress intonation peaks before processing if the high notes are the problem.

## Distributing the mod

Package the **installed** folder, for example `extensions\bosota_voice_alien\` with its XML and the 2,324 audio files (about 90 MB). Recipients need neither Python nor ffmpeg; they drop the folder into `<game>\extensions\`. The folder name must stay as it is, because the redirect inside `sound_library.xml` spells it out.

- **Nexus Mods / ModDB:** upload a ZIP of that folder. Say clearly which voice track it is for and that the game counts as modified.
- **Steam Workshop:** upload with Egosoft's free "X Tools" (Steam library → Tools). The Workshop installs every mod under a folder named `ws_<number>`, and the number only exists after the first upload. So: upload once hidden, read the number from the `content.xml` the tool rewrites, add a variant whose `id` is that `ws_<number>` (the generator derives the redirect path from the id), build, and run `WorkshopTool update`. Only `.cat`, `.dat`, `.cur`, `.mkv`, `.txt` and `.pdf` files are uploaded, so use `-buildcat` to pack the folders into a catalog.
- **Legal:** the audio files are processed Egosoft recordings. Private use is unproblematic; publishing is a grey area, even though comparable voice mods have been on Nexus for years. Check Egosoft's modding rules before a Workshop upload.

## Troubleshooting

- The mod is missing from the Extensions list: the `content.xml` is not well-formed. The validator catches this.
- The mod is listed but Boso sounds unchanged: start X4 with `-logfile debuglog.txt` and run `Select-String -Path "<user folder>\debuglog.txt" -Pattern "No matching node","bosota"`. The user folder is `Documents\Egosoft\X4\<id>\`.
- Boso is silent: the audio folder is missing or the mod was swapped while the game was running. Close the game and run `install_mod.py` again.
- Brief red text in the game: with `-logfile` active, X4 shows its own script errors on screen. Remove the option once you are done testing.

## Repository layout

```
config/variants.json       variant definitions, audio recipes, attribute patches
tools/x4cat_extract.py     .cat/.dat extractor (text index + concatenated data)
tools/process_audio.py     ffmpeg/Rubberband filter chains, two-pass loudness, gain
tools/pitch_flatten.py     Praat pre-stage (intonation range compression)
tools/build_mod.py         writes dist/<id>/ from the configuration
tools/validate_mod.py      checks the diff against the game's real sound_library.xml
tools/install_mod.py       installs exactly one variant, audio included
dist/                      built extensions without audio (committed)
diag/                      diagnostic extension that proved the redirect mechanism
docs/                      project documentation (see below)
build/                     extracted game files, processed audio, samples, venv (ignored)
```

Documentation: `docs/HOW-IT-WORKS.md` (plain language), `docs/phase0-findings.md` (verified engine facts), `docs/projekt/MILESTONES.md` and `docs/projekt/CURRENT_STATE.md` (project state), `docs/dev-team/LESSONS.md` (what we learned the hard way). The original research handoff that started the project is kept in German as `docs/X4_Boso_Ta_Voice_Mod_Handoff.md`.
