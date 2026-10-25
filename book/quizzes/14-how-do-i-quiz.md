# Quiz: How Do I…? (Cookbook)

Chapter: [14 · How Do I…? (Cookbook)](../14-how-do-i.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Apply]** You re-render the German Will audio at a new gain into `build/audio/will_dark_g8`. Which variants must get the new `audio_variant`?

- A) Only `will`
- B) Only `alien_ws`, because only the Workshop matters
- C) Both `will` and `alien_ws`, which share the Will audio
- D) `alien` and `will`, because both are German

**2. [Apply]** You add a new variant key `will_quiet` to `config/variants.json`. What must you change in `install_mod.py` so that `install_mod.py will_quiet` works?

- A) Add the key to a hard-coded list of choices
- B) Nothing; the CLI choices are read from the configuration's variant keys
- C) Add a branch for its audio folder
- D) Nothing, but you must pass `--force` the first time

**3. [Apply]** You want to try a new ElevenLabs voice for the whole German set. Why should the full run use a new `--dst` instead of `build/tts/will_de`?

- A) `tts-batch` refuses a folder that already holds WAVs
- B) `tts-batch` skips every id that already has a WAV, so the new voice would only fill gaps and the folder would mix voices; and the Will cache would be lost for later repairs
- C) The new voice needs a different sample rate
- D) ElevenLabs bills twice for a folder it has seen before

**4. [Apply]** What does `install_mod.py --remove` remove?

- A) Every folder in `extensions/` that this project ever installed, including `ws_*`
- B) Every folder whose name starts with `bosota_`, and nothing else; Workshop items are unsubscribed in Steam
- C) Only the variant named in the configuration's last install
- D) Everything in `extensions/` except Egosoft's DLCs

**5. [Apply]** (locate the change) To support another Boron speaker, which places in the code have page `10201` hard-coded?

**6. [Apply]** "The mod does nothing" in the game. Put the cookbook's four checks in a sensible order and say what each one rules out.

**7. [Apply]** You need a Workshop item for a new language. Outline the steps from nothing to a working item, and say why they come in this order.

---

## Answers

**1. C.** `will` and `alien_ws` both use `will_dark_g6` (`config/variants.json:125`, `:89`). Changing one leaves the ModDB build and the Workshop build at different levels. A and B forget one of the pair. D is wrong because `alien` uses its own processed originals (`config/variants.json:21`).

**2. B.** `choices=sorted(CFG["variants"])` (`tools/install_mod.py:78`), and the audio folder comes from the variant's `audio_variant` (`:107`). A and C describe code that does not exist. D: `--force` only skips the running-game check (`:89`).

**3. B.** `todo` excludes ids whose WAV exists (`tools/voice_convert_elevenlabs.py:146`). The Will folder is also the resume cache for future patch repairs. A is wrong: there is no refusal. C is wrong: all output is converted to 44.1 kHz mono (`:100`). D is not how billing works.

**4. B.** With `--remove`, the installer runs the `bosota_` removal loop and returns (`tools/install_mod.py:92-98`). A is wrong because `ws_*` is excluded by `PREFIX` (`:30`). C and D describe logic that does not exist.

**5.** The redirect target in the builder (`tools/build_mod.py:29`). The installer's target folder `voice/10201/normal` (`tools/install_mod.py:112`). The coverage check's default `page="10201"` and the `10201_<lang>.json` index name (`tools/check_coverage.py:32`, `:81`). The TTS default `--page 10201` (`tools/voice_convert_elevenlabs.py:177`). The sound ids also embed the page (`config/variants.json:10-17`). All of these would need a per-variant page list.

**6.** (1) Is the extension listed and enabled in the Extensions menu? This rules out a disabled mod or a malformed `content.xml`. (2) Is `validate_mod.py` clean? This rules out selectors that do not match and bad XML (`tools/validate_mod.py:111-114`). (3) Does `extensions/<id>/voice/10201/normal/` hold files, does the folder name equal `<id>`, and is no second `ws_*`/`bosota_*` variant present? This rules out a broken redirect, missing audio and two variants on the same entries (`tools/install_mod.py:30`). (4) Run with `-logfile debuglog.txt` and search for "No matching node" and the mod id. This shows what the game actually applied.

**7.** Create the item with `publishx4` from an XML-only staging folder; creating it together with audio timed out (`docs/RELEASE.md:12`). Read the `ws_<number>` that the tool writes into that folder's `content.xml`. Add a variant whose `id` is that `ws_<number>`; the redirect path must contain the Workshop folder name (`tools/build_mod.py:29`). Build, validate, stage with audio through `install_mod.py <key> --game-dir <staging>`, then `update` without `-preview` (`docs/RELEASE.md:13`, `:37`). The order is forced: the id the build needs exists only after the first upload.
