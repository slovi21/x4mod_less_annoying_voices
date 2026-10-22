# Release procedure: Steam Workshop and ModDB

Two items, one per voice track. Nothing in this file requires Python on the user's side; the packaged folders contain everything.

| Item | Folder name in the game | Audio | Source for packaging |
|---|---|---|---|
| **DE** – Boso Ta – less annoying VOICE (DE) | `ws_3824406333` (Workshop) / `bosota_voice_will_de` (ModDB) | 2,324 lines re-spoken with the ElevenLabs voice Will (Eleven v4 Turbo), post-processed `will_dark`, +6 dB | `build/workshop/stage2/extensions/ws_3824406333`, `build/workshop/moddb/bosota_voice_will_de` |
| **EN** – Boso Ta – less annoying VOICE (EN) | `ws_<number>` (after first upload) / `bosota_voice_alien_en` (ModDB) | 1,750 originals processed with the Alien chain at half strength, +4 dB | `build/workshop/stage1_en/extensions/bosota_voice_alien_en` for the first upload, then `stage2_en` |

The Workshop folder name is part of the redirect path inside the mod, so Workshop builds and ModDB builds are different builds of the same audio. `tools/build_mod.py` derives the path from the variant's `id`.

## Steam Workshop

Prerequisites: X Tools installed (`C:\Steam\steamapps\common\X Tools`), Steam running and logged in, Workshop agreement accepted. All commands run from the X Tools folder. Only `.cat`, `.dat`, `.cur`, `.mkv`, `.txt` and `.pdf` are uploaded, so `-buildcat` packs the folders into `ext_01.cat/.dat` first.

**DE (item exists, hidden):**

```
.\WorkshopTool.exe update -path "<repo>\build\workshop\stage2\extensions\ws_3824406333" -preview "<repo>\build\workshop\preview_DE.jpg" -buildcat -namedesc up -changenote "New German voice (Will) and corrected folder name"
```

`-namedesc up` pushes the title and description from `content.xml`. The version in `content.xml` (102) is higher than the first upload (100), so `-minor` is not needed. Then open the item page (`showpage -path ...`) and set visibility to public.

**EN (no item yet):**

1. `.\WorkshopTool.exe publishx4 -path "<repo>\build\workshop\stage1_en\extensions\bosota_voice_alien_en" -preview "<repo>\build\workshop\preview_EN.jpg" -buildcat` → answer `y`. The tool writes `id="ws_<number>"` into that folder's `content.xml`. Leave the item hidden.
2. Add a variant `alien_en_ws` in `config/variants.json` with `"id": "ws_<number>"` and `"version": "101"` (copy of `alien_en`), run `build_mod.py`, `validate_mod.py`, then `install_mod.py alien_en_ws --game-dir build/workshop/stage2_en`.
3. `.\WorkshopTool.exe update -path "<repo>\build\workshop\stage2_en\extensions\ws_<number>" -buildcat -namedesc up -changenote "Folder name corrected for the Workshop"`, then set visibility.

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
