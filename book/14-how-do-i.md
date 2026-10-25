# 14 · How Do I…? (Cookbook)

> **What you'll be able to answer after this chapter:** where a given change goes, which commands to run, and what to verify (operations & change).

Every recipe ends with: `build_mod.py`, `validate_mod.py`, close X4, `install_mod.py <key>`, listen in the game.

### …change the loudness of a variant?
Rerun `process_audio.py` with the same `--variant`, `--src` and a different `--gain-db` into a new folder (`<chain>_g<N>`), and set `audio_variant` in `config/variants.json` for **every** variant that shares the audio (`alien_en` + `alien_en_ws`, `will` + `alien_ws`). Steps of 3 dB are audible, 2 dB ≈ 20 % perceived. Sample peaks are limited at −1 dBFS (true peaks can be slightly higher), so beyond about +9 dB the limiter works hard.

### …change the character of the English voice?
Edit or add a chain in `VARIANTS` (`tools/process_audio.py:51-59`); `alien_mid_scaled(k)` gives the alien chain at any strength `k`. Render samples first: `--files 30201131,30201057 --wav --dst build/samples_x`, judge character on the PC, judge level in the game.

### …regenerate German lines after a patch?
Re-extract originals and texts first ([ch. 9](09-patch-maintenance.md), steps 1–3), then:

```powershell
python -I tools/check_coverage.py --lang l049 --audio build/audio/will_dark_g6 --tfile build/base/t/0001-l049.xml
build\venv\Scripts\python.exe -I tools/voice_convert_elevenlabs.py tts-batch --voice bIHbv24MWmeRgasZH58o --model eleven_v4_turbo --tfile build/base/t/0001-l049.xml --ids-from build\orig\voice-l049\10201\normal --dst build/tts/will_de
python -I tools/process_audio.py --variant will_dark --src build/tts/will_de --src-ext wav --gain-db 6 --files <new ids> --dst build/audio/will_dark_g6
```

`tts-batch` skips existing WAVs. For a line whose text changed, delete its WAV first.

### …try a different ElevenLabs voice?
`voices --filter male` → pick an id → `tts --voice <id> --model eleven_v4_turbo --text "<line>" --out build\samples_v\<stem>.wav` → post-process with `process_audio.py --variant will_dark --src build\samples_v --src-ext wav --wav --dst build\samples_v_out` (without `--variant` the tool only prints the list and exits). For a full run use a new `--dst` so the Will cache stays intact.

### …add a new variant?
Add a key to `config/variants.json` with `id`, `audio_variant`, names, descriptions, `sound_attr_ops` (copy from an existing variant), optional `version` and `audio_recipe`. Produce the audio, build, validate. The installer offers every key automatically (`tools/install_mod.py:78`).

### …release an update to the Workshop?
Raise `version` of `alien_ws` / `alien_en_ws` above the live version (DE 103, EN 102 after modpub), `build_mod.py`, delete the old staging folder `build/workshop/stage2/extensions/ws_<n>` (or `stage2_en`), `install_mod.py <key> --game-dir build/workshop/stage2` (or `stage2_en`), then `WorkshopTool.exe update -path … -buildcat -changenote "…"` from the X Tools folder ([ch. 8](08-installing-and-releasing.md)). Or let modpub do it from `release/mod.yaml`.

### …create a Workshop item for a new language or speaker?
`publishx4` with an XML-only staging folder, read `ws_<number>` from that folder's `content.xml`, add a variant with that `id`, build, stage with audio, `update` without `-preview`.

### …replace another Boron speaker?
Not supported yet: page `10201` is hard-coded in `build_mod.py:29`, `install_mod.py:112`, `check_coverage.py` and the TTS default. Generalise these to a per-variant page list, look up which contexts exist for each page in the real `sound_library.xml`, and do not apply 2D playback to generic pilot voices. Counts and costs: `docs/projekt/CURRENT_STATE.md`.

### …uninstall?
`install_mod.py --remove` (removes `bosota_*` only), or delete the folder; unsubscribe Workshop items in Steam.

### …debug "the mod does nothing"?
1. Is the extension listed and enabled in the game's Extensions menu? The enable table is the machine-specific `content-<computer name>.xml` in the user folder (here `content-MSI-PRODP20Z.xml`, `docs/phase0-findings.md`).
2. `validate_mod.py` clean?
3. `extensions/<id>/voice/10201/normal/` contains files, and `<id>` equals the folder name? Is a second variant (`ws_*` or `bosota_*`) also present?
4. Start X4 with `-logfile debuglog.txt`, then `Select-String -Path "<Documents>\Egosoft\X4\<Steam user id>\debuglog.txt" -Pattern "No matching node","bosota"` (here the user id is `34818113`).

→ Check your understanding: [quizzes/14-how-do-i-quiz.md](quizzes/14-how-do-i-quiz.md)
