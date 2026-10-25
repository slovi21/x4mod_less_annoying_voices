# 4 · Variants & Configuration (`config/variants.json`)

> **What you'll be able to answer after this chapter:** the full schema of the configuration (see Schema), what each of the five variants is for and why the Workshop ones exist (see The five variants), which fields are read by code and which are documentation only (see Schema), and what breaks if a field is wrong (see Errors & edge cases).

## Why it exists

Every generated artefact (the mod folders in `dist/`, the installed extension, the Workshop and ModDB packages) is a function of a few decisions: which sound entries to patch, which folder name the mod gets, where its audio is, how it is described. Keeping those decisions in one JSON file makes the generated XML reproducible and reviewable.

## Schema

Background from [Core Concepts](02-core-concepts.md): Boso Ta's voice is played through six entries ("sound entries") in the game's `libraries/sound_library.xml`: `10201_normal`, `10201_normal_npc`, `10201_comm`, `10201_comm_signalleak`, `10201_comm_npc` and `10201_comm_broadcast`. The mod patches them with an XML diff, X4's way of changing a game XML file without replacing it ([ch. 5](05-building-and-validating.md)). The patch "redirects" each entry: it replaces the folder the entry reads its audio from with the mod's own folder.

```text
{
  "_doc": [string, …],                 documentation only
  "author": "Slovi",                    → content.xml author
  "version": "100",                     → default content.xml version
  "boso_ta_ids": [6 sound ids],         → every variant redirects all of them
  "variants": {
    "<key>": {
      "id": string,                     REQUIRED → folder name = extension id = redirect path segment
      "audio_variant": string,          REQUIRED → build/audio/<audio_variant>/ must hold the .ogg files
      "name_en", "name_de": string,     REQUIRED → content.xml name + localised <text>
      "desc_en", "desc_de": string,     REQUIRED → content.xml description + localised <text>
      "version": string,                optional, overrides the top-level version
      "sound_attr_ops": [ {op, attr, value, ids} ], optional attribute patches
      "audio_recipe": string,           documentation only
      "_doc": string                    documentation only
    }
  }
}
```

Read by code: `author`, `version`, `boso_ta_ids` and the variant fields marked REQUIRED/optional, in `tools/build_mod.py:29-56,72` and `tools/install_mod.py:31,99-107`. Nothing reads `audio_recipe` or any `_doc`.

### `sound_attr_ops`

Each item becomes one diff operation per id (`tools/build_mod.py:38-44`):

| `op` | Generated XML | Precondition in the base game |
|---|---|---|
| `"add"` | `<add sel="/soundlibrary/sound[@id='X']" type="@attr">value</add>` | attribute must **not** exist |
| anything else (used: `"replace"`) | `<replace sel="/soundlibrary/sound[@id='X']/@attr">value</replace>` | attribute **must** exist |

In the generated XML, `X` is each sound id from the item's `ids`, `attr` is its `attr` and `value` is its `value`. All current variants carry the same two items (e.g. `config/variants.json:27-50`): `noocclusion=true` on five ids (not `10201_comm_signalleak`, which already has it) and `is3d=0` on `10201_normal` and `10201_normal_npc`. `validate_mod.py` enforces both preconditions ([ch. 5](05-building-and-validating.md)). In the game, `noocclusion="true"` stops level geometry from muffling the sound (Boso sits behind the glass of his tank), and `is3d="0"` plays the entry without positional audio, so the player's position and facing no longer change its level (`config/variants.json:6`).

**Why `is3d=0` only on the two `normal` entries.** In the base game all six entries are `is3d="1"`. The problem the author heard was in an in-person conversation at the HQ with the manager Karee: with the player facing Boso, he was about 90 % as loud as Karee; with the player's back turned, about 60 % as loud and unintelligible (`config/variants.json:49`). Comm entries play through the comm window, where position did not cause audible trouble, so they stay positional (inference: they were never tested in 2D). The cost of 2D on `10201_normal_npc`: his chatter with other NPCs is equally loud anywhere on the platform, no longer fading with distance (`docs/projekt/CURRENT_STATE.md`, "Known risks").

## The five variants

| Key | `id` (folder) | `audio_variant` | Language | Audio | Status |
|---|---|---|---|---|---|
| `will` | `bosota_voice_will_de` | `will_dark_g6` | DE | TTS "Will", `will_dark`, +6 dB | ModDB/manual DE release |
| `alien_ws` | `ws_3824406333` | `will_dark_g6` | DE | same audio as `will` | Steam Workshop DE item (config 102, live 103 after modpub) |
| `alien` | `bosota_voice_alien` | `d12_alien_mid_g9` | DE | processed originals, full strength, +9 dB | no-account alternative |
| `alien_en` | `bosota_voice_alien_en` | `alien_mid_50_g4` | EN | processed originals, half strength, +4 dB | ModDB/manual EN release |
| `alien_en_ws` | `ws_3824446410` | `alien_mid_50_g4` | EN | same audio as `alien_en` | Steam Workshop EN item (config 101, live 102 after modpub) |

How to read the table: an `audio_variant` name is the filter chain (or, for `will_dark`, the processing applied to the text-to-speech output) followed by `_g<n>`, the `--gain-db` value it was rendered with ([ch. 6](06-audio-processing.md)). "Full strength" and "half strength" refer to the alien chain: `alien_mid_50` applies it at 50 % (6 instead of 12 semitones down, half the frequency shift and chorus). "No-account alternative" means it can be built without an ElevenLabs account, because it filters the original recordings instead of using text-to-speech. modpub is explained two paragraphs below.

**Why Workshop variants exist.** The redirect path contains the folder name (`tools/build_mod.py:29`). Steam installs items as `ws_<number>`, so a build with `id: bosota_voice_will_de` installed from the Workshop would point at a folder that does not exist and Boso would be silent. The Workshop number only exists after the first upload, so the procedure is: upload once, read the number, add a variant whose `id` is `ws_<number>`, rebuild, update ([ch. 8](08-installing-and-releasing.md)).

**What is live on the Workshop is not what this file says.** modpub is an external release tool in another repository (`C:\#repos\github\modpub`); it renders videos and images and uploads to YouTube, the Workshop, Reddit and ModDB. You do not need it to build or install the mod. Its Workshop channel copies the staging folders and raises version, name and description in its own copies (`docs/RELEASE.md`, section "modpub"); how it computes the new version is defined in the modpub repository and not documented here. Its last upload on 2026-10-24 left these values (the `release/out/` files are ignored by git):

| Workshop item | `config/variants.json` | live (`release/out/workshop/<lang>/content.xml`) | next manual upload needs |
|---|---|---|---|
| DE `alien_ws` | 102 | **103**, title "Boso Ta – erträgliche Stimme" | `version` ≥ 104 |
| EN `alien_en_ws` | 101 | **102** | `version` ≥ 103 |

The rule in the last column applies to a manual upload with Egosoft's `WorkshopTool update`. That command's option `-namedesc up` pushes the title and description from `content.xml` to the Workshop (`docs/RELEASE.md:27`); leave it out if the modpub title should stay.

**Naming gotcha.** The key `alien_ws` holds the **Will** build; it was created for the Alien audio and switched on 2026-10-22 (`config/variants.json:121`). The key was kept for compatibility (inference: renaming would have been harmless in code, but the key appears in docs and commands).

## Traced example

Build of `alien_en_ws`:

- `id` `ws_3824446410` → `dist/ws_3824446410/` and redirect `extensions\ws_3824446410\voice\10201\normal`.
- `version` `101` → `content.xml version="101"` (the first Workshop upload was 100; `WorkshopTool.exe`, the upload tool in Egosoft's "X Tools", needs an update to carry a higher version than the item's current one or the option `-minor`, `docs/RELEASE.md:27,35`, so 101 was the next free number).
- `audio_variant` `alien_mid_50_g4` → `install_mod.py alien_en_ws` copies `build/audio/alien_mid_50_g4/*.ogg` (1,750 files).
- `sound_attr_ops` → seven extra diff lines (five adds, two replaces).

## Errors & edge cases

| Mistake | Effect | Caught by |
|---|---|---|
| Missing required field | `KeyError` in `build_mod.py` | Python traceback |
| Wrong sound id in `boso_ta_ids` or `ids` | the game skips that patch and plays the original voice; nothing shows in normal play, only the debug log (X4 started with `-logfile debuglog.txt`) contains "No matching node" (`docs/MAINTENANCE.md:21`) | `validate_mod.py` |
| `add` on an attribute that exists | the game rejects that operation | `validate_mod.py` |
| `id` differs from the actual install folder | redirect points nowhere, Boso silent; the diff itself applies, so there is no "No matching node" (whether the engine logs the missing audio file was not checked) | not caught; [ch. 13](13-failure-modes.md) |
| `audio_variant` folder missing, misspelt or without `.ogg` files | `install_mod.py` stops with the same error in all three cases; only `*.ogg` files are copied (`tools/install_mod.py:107-110`) | installer |
| Two variants installed at once | both patch the same entries; which one wins depends on the load order (not verified) | only partly: `install_mod.py` removes every `bosota_*` folder first, but not `ws_*` ([ch. 8](08-installing-and-releasing.md)) |
| Windows paths such as `build\venv` inside a Python string literal, in a script fed to Python through a shell heredoc to rewrite the JSON | Python reads `\v`, `\1…` as escape sequences and writes control characters into the file | not caught; happened once to `_doc` and `audio_recipe`, repaired by hand. Edit the JSON in an editor, or use raw strings (`r"…"`) in such scripts |

## Where to look

`config/variants.json`, `tools/build_mod.py`, `tools/install_mod.py:99-117`.

→ Check your understanding: [quizzes/04-variants-configuration-quiz.md](quizzes/04-variants-configuration-quiz.md)
