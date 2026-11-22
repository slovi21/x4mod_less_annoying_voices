# 15 · Glossary

| Term | Meaning in this codebase |
|---|---|
| **Alien chain** | Filter chain: Rubberband pitch with shifted formants, frequency shift, chorus, mid-range focus; `alien_mid_scaled(k)` in `tools/process_audio.py:41-48`. |
| **`audio_variant`** | Folder name under `build/audio/` holding a variant's `.ogg` files. |
| **Boso Ta** | Boron scientist at the player HQ; voice page 10201. |
| **Catalog** | `NN.cat` index + `NN.dat` data; see [ch. 3](03-game-archives-and-extraction.md). |
| **Context** | Playback situation of a line: `normal`, `comm`, `comm_npc`, `comm_broadcast` (+ `normal_npc`, `comm_signalleak` as sound entries). |
| **Coverage** | Every game line id of page 10201 has a file in the variant's folder; `tools/check_coverage.py`. |
| **Diff** | X4's XML patch format (`<diff>` with `add`/`replace`/`remove`). |
| **`dist/`** | Generated, committed extension folders without audio. |
| **ElevenLabs** | Commercial text-to-speech service used for the German voice. |
| **Extension** | An X4 mod folder with `content.xml`. |
| **Formants** | Resonances that define how "large" a voice sounds; `formant=shifted` moves them with the pitch. |
| **`fp` suffix** | Alternate take of a line (`30201430fp`); shares the base line's text. |
| **Gain** | Level added after normalisation (`--gain-db`), limited at −1 dBFS. |
| **`is3d`** | Sound attribute; `0` = no positional audio. |
| **Line id** | Numeric id of a line = audio file name = text id in page 10201. |
| **LUFS** | Loudness units; originals measure about −22 LUFS. |
| **Mid-range focus (`MID`)** | Band-limit 220 Hz–5.5 kHz, +4 dB at 1.4 kHz, +2 dB at 2.8 kHz, compression 2.5:1. |
| **modpub** | External release tool (other repository) driven by `release/mod.yaml`. |
| **Modified** | Game state after loading unsigned files; sticky on saves, no online Ventures. Achievements reportedly still unlock (unverified). |
| **`noocclusion`** | Sound attribute; `true` = no muffling by geometry. |
| **Redirect** | Replacing `<sample start>` so the engine reads the mod's folder. |
| **Rubberband** | Tempo-preserving pitch shifter available in full ffmpeg builds. |
| **Sound entry / sound id** | `<sound id="10201_normal">` in `libraries/sound_library.xml`. |
| **Staging** | Copies of installed-layout folders under `build/workshop/` used for uploads. |
| **TTS** | Text-to-speech. |
| **Variant** | One entry in `config/variants.json` = one buildable mod. |
| **Voice page** | Numeric speaker id (10201). |
| **Voice language** | `l044` English, `l049` German; launch option `-voicelanguage 44|49`. |
| **`will_dark`** | Post-processing chain for the TTS voice "Will": −4 semitones, warm EQ. |
| **Workshop build** | Variant whose `id` is `ws_<item number>`. |
| **WorkshopTool** | Egosoft's upload tool in "X Tools". |
| **`ws_<number>`** | Folder name under which Steam installs a Workshop item. |

→ Final check: [quizzes/16-final-exam.md](quizzes/16-final-exam.md)
