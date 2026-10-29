# Boso Ta – less annoying VOICE

A mod for **X4: Foundations 9.00** that makes the Boron scientist **Boso Ta** bearable to listen to. His original voice is extremely high and squeaky in both the German and the English voice track. This mod replaces his lines with processed or re-generated copies: lower in pitch (by 4 to 12 semitones depending on the variant, see Variants; 12 semitones are one octave), an alien timbre, a mid-range emphasis so he stays intelligible, and playback that no longer depends on where you are standing. In the audio-redirect variants (`alien`, `alien_en`) timing, pauses and lip sync are untouched because the pitch is changed without changing the tempo; the text-to-speech variant `will` re-speaks the lines instead (see Variants).

Two things are worth knowing before you install anything:

- **The game will count as modified.** Every mod does this. A save you make while the mod is active keeps that mark even if you remove the mod later, and a modified game cannot use the online Ventures (which Egosoft has switched off anyway). According to several player reports, Steam achievements still unlock with mods; there is no official Egosoft statement on this. The `save="0"` attribute in the mod's `content.xml` only means the save file does not list the mod as a requirement, so you can uninstall without warnings.
- **The repository contains no game audio.** The processed files are copies of Egosoft's recordings and are not published here. You generate them on your own machine from your own installation (about ten minutes for the `alien` variants; the `will` variant needs an ElevenLabs account, see Variants), or you receive them as part of a packaged release: once published, the Steam Workshop items (subscribe, Steam installs them) or the ModDB downloads (copy the folder from the ZIP into `<game>\extensions\`, see "Distributing the mod").

Boso Ta speaks through voice set `10201` (the game's internal ID of this voice; it is also the folder name of the audio files and the number of the text page). The only other character wired to that set is the Boron faction representative, voiced by the same actor, so he changes too. Random NPCs are not affected.

## Variants

| Key | Kind | What you get |
|---|---|---|
| `will` | text-to-speech | **German voice track, the published DE version.** All lines re-spoken from the game texts by the ElevenLabs voice "Will" (model `eleven_v4_turbo`), then 4 semitones down with shifted formants, warmed, +6 dB. Sounds like a calm, deeper, natural voice; no accent; line lengths differ slightly, lip sync not preserved. Needs an ElevenLabs account to build: 183,227 characters, budget about 92,000 credits at the published rate of 0.5 credits per character (the 2026-10 run was billed at about 0.2). |
| `alien` | audio redirect | German voice track, processed originals: 12 semitones down, formants shifted, frequency shift, chorus, mid-range focus, +9 dB. Sounds clearly alien and somewhat synthetic. Superseded by `will` for publishing; kept as the alternative that needs no ElevenLabs account. |
| `alien_en` | audio redirect | **English voice track, the published EN version.** Half strength: 6 semitones down, half the frequency shift and chorus, same mid-range focus, +4 dB. Sounds deeper and less shrill, only mildly alien. The English original is less shrill, so it needs less correction. |
| `alien_ws`, `alien_en_ws` | Workshop builds | `alien_ws` is the `will` build (Steam Workshop folder `ws_3824406333`), `alien_en_ws` is the `alien_en` build (Steam Workshop folder `ws_3824446410`). |

Names used by the tools: `alien` is built with the audio chain `d12_alien_mid` (output folder `build\audio\d12_alien_mid_g9`), `alien_en` with `alien_mid_50` (output folder `build\audio\alien_mid_50_g4`), and `will` from the text-to-speech output in `build\tts\will_de` with the post-processing chain `will_dark` (output folder `build\audio\will_dark_g6`). All are installed with `tools/install_mod.py <key>`.

An earlier approach with engine effects only (resampling pitch plus low-pass, no audio files) is documented in `docs/HISTORY.md`; it was not good enough and has been removed.

Why text-to-speech for German: converting the original recordings into another voice (speech-to-speech) kept the original actor's regional colouring in every one of 21 voices tried. Generating from the texts avoids it. The texts live in page 10201 of the game's text file under the same ids as the audio files; `tools/voice_convert_elevenlabs.py tts-batch` does the whole run and can be resumed. Five ids have no text entry and keep the `alien` audio.

Only one variant can be active at a time. They all rewrite the same six sound entries (see "How it works" below). The audio variants are tied to one voice language each, because the redirect in `sound_library.xml` is language independent: an English player with the German variant would hear processed German lines.

## How it works, in one paragraph

X4 keeps an index, `libraries/sound_library.xml`, that tells the engine where each character's voice files live and how to play them. The mod patches the six entries `10201_*` with an XML diff (a small patch file that changes only the listed parts of the game's index) so they point at the mod's own folder, `extensions\<mod id>\voice\10201\normal\` (`<mod id>` is the extension's folder name, for example `bosota_voice_alien`), which holds the processed `.ogg` files under their original line IDs. The same diff sets `noocclusion="true"` (no muffling through the glass of his tank) and `is3d="0"` on the conversation entries (no attenuation when you turn away). The engine loads the redirected path literally; it does not insert a language suffix. See `docs/HOW-IT-WORKS.md` for a non-technical explanation and `docs/phase0-findings.md` for the verified facts behind every one of these statements.

## Building it yourself (Windows, PowerShell)

You need Python 3 and a full ffmpeg build that includes the Rubberband filter:

```powershell
winget install Gyan.FFmpeg
```

`winget` is the Windows package manager, `install` installs a package, and `Gyan.FFmpeg` is the full build from gyan.dev. Open a new console afterwards so the path is picked up.

This section builds the `alien` and `alien_en` variants from the original recordings. The `will` variant is generated from the game texts with `tools/voice_convert_elevenlabs.py tts-batch`; its three steps (generate, post-process, copy the five textless lines from `d12_alien_mid_g9`) are stored in the `audio_recipe` of `will` in `config/variants.json` and explained in `book/07-text-to-speech.md`. That tool needs the `requests` package (the project uses a virtual environment in `build\venv`) and an ElevenLabs API key in the environment variable `ELEVENLABS_API_KEY` or the file `%USERPROFILE%\.elevenlabs_key`. Clone the repository and run all commands from its root folder. `<game>` stands for your X4 folder; the examples use `C:\Steam\steamapps\common\X4 Foundations`.

**1. Extract Boso Ta's original lines from your game.** The catalogs `01.cat` … `09.cat` are plain text indexes next to `.dat` files with the raw data; later catalogs override earlier ones, so run this for every catalog that contains the folder. In 9.00 one run with `03.cat` is enough: all of Boso Ta's lines, both languages, live there. The text files `t/0001-l0XX.xml` (`l0XX` is the language number, as in `l049`) live in `09.cat`; they are the basis of the `will` variant. After a patch, repeat the extraction for every catalog that now holds the lines; `Select-String -Path "<game>\0*.cat" -Pattern "^voice-l049/10201/normal/" -List` shows which catalogs these are. Extraction command:

```powershell
python -I tools/x4cat_extract.py "C:\Steam\steamapps\common\X4 Foundations\03.cat" build\orig "voice-l049/10201/normal/*"
```

`-I` runs Python in isolated mode, so no foreign settings or modules interfere. The arguments are the catalog, the output folder, and a path prefix; use `voice-l044/...` for the English track.

**2. Process the audio.** The recipe for each variant is stored in `config/variants.json` under `audio_recipe`. For German:

```powershell
python -I tools/process_audio.py --variant d12_alien_mid --gain-db 9 --src build\orig\voice-l049\10201\normal --dst build\audio\d12_alien_mid_g9
```

`--variant` selects the filter chain (`--list` shows all of them), `--gain-db` adds level after loudness normalisation with a limiter at −1 dBFS (the limiter keeps peaks just below the digital maximum so they cannot clip), `--src` is the folder of originals, `--dst` is the folder the configuration expects. In both examples its name is `<--variant>_g<--gain-db>`; use exactly these names. About ten minutes on eight cores. For English use `--variant alien_mid_50 --gain-db 4` on the `voice-l044` files and write to `build\audio\alien_mid_50_g4`.

**3. Build, validate, install.**

```powershell
python -I tools/build_mod.py
python -I tools/validate_mod.py
python -I tools/install_mod.py alien
```

Run the commands one after another and run the third only if the validator reported no problem. `build_mod.py` writes the extension folders (XML only) to `dist/` from the definitions in `config/variants.json`. `validate_mod.py` extracts the real `sound_library.xml` from your game and checks that every selector hits exactly one node and that no attribute is added twice; it also catches a `content.xml` that is not well-formed. `install_mod.py` removes every `bosota_*` folder from the game's `extensions` directory, copies the chosen variant, and adds the audio from `build/audio/`. It refuses to run while `X4.exe` is open, because the running game would keep looking for files you just deleted. For the English variant do steps 1 to 3 with the English values from above (`voice-l044` files, `--variant alien_mid_50 --gain-db 4`, `install_mod.py alien_en`). Because only one variant can be active, installing one removes the other. A different game location can be passed with `--game-dir` or the `X4_GAME_DIR` environment variable, for example `python -I tools/install_mod.py alien --game-dir "D:\Games\X4 Foundations"`.

In the game, open Extensions from the main menu and check that "Boso Ta – less annoying VOICE (DE)" or "(EN)" is listed and enabled.

**Uninstall:** `python -I tools/install_mod.py --remove`, or delete the folder under `extensions`.

## Listening to the other voice track

X4 lets you pick the voice language independently of the interface language. Add `-voicelanguage 44` to the Steam launch options (Steam library → right-click X4 → Properties → General → Launch Options) for English speech or `-voicelanguage 49` for German; menus and subtitles keep their language. Install the matching variant first, and only that one, since only one variant can be active at a time.

## Tuning

`python -I tools/process_audio.py --list` prints the three production chains (`d12_alien_mid` for `alien`, `alien_mid_50` for `alien_en`, `will_dark` for `will`); `alien_mid_scaled(k)` in that file gives the alien chain at any strength `k` (1.0 = the German full strength, 0.5 = the English half strength; the pitch drops by `k` octaves), and new chains are one dictionary entry. Render a few lines with `--files <id,id> --wav` (line ids are the audio file names without `.ogg`, for example `--files 30201131,30201057`; the WAVs go to the `--dst` folder) and listen to them on the PC to judge character. Judge **loudness and intelligibility only inside the game**: a dark voice sounds just as loud as the original on headphones and still disappears under the station ambience in the game. The chains that were tried and rejected along the way are listed in `docs/HISTORY.md`.

## Distributing the mod

Package the **installed** folder, for example `extensions\bosota_voice_alien\` with its XML and the 2,324 audio files (about 90 MB). Recipients need neither Python nor ffmpeg; they drop the folder into `<game>\extensions\`. The folder name must stay as it is, because the redirect inside `sound_library.xml` spells it out.

- **Nexus Mods / ModDB:** upload a ZIP of that folder. Say clearly which voice track it is for and that the game counts as modified.
- **Steam Workshop:** upload with Egosoft's free "X Tools" (Steam library → Tools). The Workshop installs every mod under a folder named `ws_<number>`, and the number only exists after the first upload. So: upload once hidden, read the number from the `content.xml` the tool rewrites, add a variant whose `id` is that `ws_<number>` (the generator derives the redirect path from the id), build, and run `WorkshopTool update`. The tool uploads only `.cat`, `.dat`, `.cur`, `.mkv`, `.txt` and `.pdf` files and no subfolders (as observed with X Tools in 2026-10), so use `-buildcat` to pack the folders into a catalog. New variants are defined in `config/variants.json`; the complete procedure is in `docs/RELEASE.md`.
- **Legal:** the audio files are processed Egosoft recordings. Private use is unproblematic; publishing is a grey area, even though comparable voice mods have been on Nexus for years. Check Egosoft's modding rules before a Workshop upload.

## Troubleshooting

- The mod is missing from the Extensions list: the `content.xml` is not well-formed. The validator catches this.
- The mod is listed but Boso sounds unchanged: start X4 with `-logfile debuglog.txt` (as a Steam launch option, see the previous section) and run `Select-String -Path "<user folder>\debuglog.txt" -Pattern "No matching node","bosota"`. The user folder is `Documents\Egosoft\X4\<id>\`, where `<id>` is the number of your game profile folder. `No matching node` means that an XML selector found nothing: a wrong sound id, or a game patch changed the entries.
- Boso is silent: the audio folder is missing or the mod was swapped while the game was running. Close the game and run `install_mod.py` again.
- Brief red text in the game: with `-logfile` active, X4 shows its own script errors on screen. Remove the option once you are done testing.

## Repository layout

```
config/variants.json       variant definitions, audio recipes, attribute patches
tools/x4cat_extract.py     .cat/.dat extractor (text index + concatenated data)
tools/process_audio.py     ffmpeg/Rubberband filter chains, two-pass loudness, gain
tools/voice_convert_elevenlabs.py  text-to-speech via ElevenLabs (quota, voices, tts, resumable tts-batch)
tools/check_coverage.py    after a game patch: lists Boso Ta lines missing from a variant folder
tools/build_mod.py         writes dist/<id>/ from the configuration
tools/validate_mod.py      checks the diff against the game's real sound_library.xml
tools/install_mod.py       installs exactly one variant, audio included
dist/                      built extensions without audio (committed)
docs/                      project documentation (see below)
build/                     extracted game files, processed audio, samples, Python virtual environment, Workshop staging (ignored by git)
```

Documentation: `docs/HOW-IT-WORKS.md` (plain language), `docs/phase0-findings.md` (verified engine facts), `docs/RELEASE.md` (Workshop and ModDB procedure), `docs/MAINTENANCE.md` (what a game patch can break and how to check), `docs/HISTORY.md` (development and patch history, including everything that was tried and removed). For contributors: `docs/projekt/MILESTONES.md` and `docs/projekt/CURRENT_STATE.md` (project state), `docs/dev-team/LESSONS.md` (what we learned the hard way).
