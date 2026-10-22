# Release procedure: Steam Workshop and ModDB

Two items, one per voice track. Nothing in this file requires Python on the user's side; the packaged folders contain everything.

| Item | Folder name in the game | Audio | Source for packaging |
|---|---|---|---|
| **DE** – Boso Ta – less annoying VOICE (DE) | `ws_3824406333` (Workshop) / `bosota_voice_will_de` (ModDB) | 2,324 lines re-spoken with the ElevenLabs voice Will (Eleven v4 Turbo), post-processed `will_dark`, +6 dB | `build/workshop/stage2/extensions/ws_3824406333`, `build/workshop/moddb/bosota_voice_will_de` |
| **EN** – Boso Ta – less annoying VOICE (EN) | `ws_3824446410` (Workshop) / `bosota_voice_alien_en` (ModDB) | 1,750 originals processed with the Alien chain at half strength, +4 dB | `build/workshop/stage2_en/extensions/ws_3824446410`, `build/workshop/moddb_en/bosota_voice_alien_en` |

Both Workshop items were created on 2026-10-22 and are hidden until their visibility is changed on the item pages. Two lessons from the EN upload:

- Creating a new item together with 56 MB of audio timed out twice (Steam error 16), while updating an existing item with 90 MB worked. Create new items with XML-only content first (`stage0_<lang>`), then add the audio with `update`.
- The first `update` of a freshly created item failed with Steam error 9 ("file not found") as long as `-preview` was passed; the same command without `-preview` succeeded. The preview set at creation stays; change it later with `updatepreview` if needed. (Copying the staging folder out of OneDrive was tried first and made no difference.)

The Workshop folder name is part of the redirect path inside the mod, so Workshop builds and ModDB builds are different builds of the same audio. `tools/build_mod.py` derives the path from the variant's `id`.

## Steam Workshop

Prerequisites: X Tools installed (`C:\Steam\steamapps\common\X Tools`), Steam running and logged in, Workshop agreement accepted. All commands run from the X Tools folder. Only `.cat`, `.dat`, `.cur`, `.mkv`, `.txt` and `.pdf` are uploaded, so `-buildcat` packs the folders into `ext_01.cat/.dat` first.

**DE (item exists, hidden):**

```
.\WorkshopTool.exe update -path "<repo>\build\workshop\stage2\extensions\ws_3824406333" -preview "<repo>\build\workshop\preview_DE.jpg" -buildcat -namedesc up -changenote "New German voice (Will) and corrected folder name"
```

`-namedesc up` pushes the title and description from `content.xml`. The version in `content.xml` (102) is higher than the first upload (100), so `-minor` is not needed. Then open the item page (`showpage -path ...`) and set visibility to public.

**EN (item 3824446410, created 2026-10-22):** variant `alien_en_ws`, staged under `build/workshop/stage2_en/extensions/ws_3824446410`. Further updates:

```
.\WorkshopTool.exe update -path "<repo>\build\workshop\stage2_en\extensions\ws_3824446410" -buildcat -changenote "<what changed>"
```

Raise `version` of `alien_en_ws` in `config/variants.json` before each update, or pass `-minor`. `-batchmode` skips the y/n prompt.

**Creating a further item (for example another language or speaker):** publish with XML-only content first, read the `ws_` id the tool writes into `content.xml`, add a variant with that id, then `update` with the audio.

**Testing a Workshop item:** subscribe, remove the local copy from `<game>\extensions` (`install_mod.py --remove`, game closed), start the game; Steam installs the item under `Documents\Egosoft\X4\<id>\extensions\ws_<number>`.

## ModDB

1. Account at moddb.com → game page "X4: Foundations" → "Add mod". Profile: name "Boso Ta – less annoying VOICE", summary, description from `docs/release/MODDB_DESCRIPTION.md`, icon from `build/workshop/preview_DE.jpg`, genre "Space Sim", tags such as audio, voice, boron. Submission is reviewed by staff, usually within a day.
2. After approval: "Files" → "Add file", category "Full Version", one file per language: `Boso_Ta_less_annoying_VOICE_DE_v1.0.zip` and `..._EN_v1.0.zip` (built by the packaging step below). Each file is reviewed separately.
3. "Images": upload both preview images.

The ZIPs contain the mod folder as the top level (`bosota_voice_will_de\...`, `bosota_voice_alien_en\...`), so users extract them straight into `<game>\extensions\`. The folder name must not be changed.

## Packaging commands (repository root)

```
python -I tools/install_mod.py will     --game-dir build/workshop/moddb      # DE for ModDB (needs build/workshop/moddb/extensions)
python -I tools/install_mod.py alien_en --game-dir build/workshop/moddb_en   # EN for ModDB
```

Then zip each `extensions\<folder>` with the folder as the archive root (PowerShell `Compress-Archive -Path "<...>\extensions\bosota_voice_will_de" -DestinationPath "<...>.zip"`).

## Checklist before publishing

- `python -I tools/validate_mod.py` → 0 errors.
- `python -I tools/check_coverage.py` for both languages → 0 missing.
- The description says which voice track the item is for, that the game counts as modified, and how to uninstall.
- The ElevenLabs licence: the German audio was generated on a paid plan (commercial licence, no attribution required). Keep the invoice.
- Egosoft audio: the English variant contains processed Egosoft recordings. Publishing is a grey area; the DE Will variant contains none.
