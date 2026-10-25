# Quiz: Variants & Configuration

Chapter: [4 · Variants & Configuration](../04-variants-configuration.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Recall]** Which field of a variant is never read by any tool?

- A) `audio_variant`
- B) `audio_recipe`
- C) `version`
- D) `sound_attr_ops`

**2. [Apply]** A variant has no `version` key. What version does its `content.xml` get?

- A) The build fails with `KeyError: 'version'`
- B) The top-level `"version": "100"`
- C) `"0"`
- D) Whatever version the old `dist/<id>/content.xml` had

**3. [Apply]** Which audio does the variant key `alien_ws` install?

- A) `d12_alien_mid_g9`, the processed German originals, as the key name suggests
- B) `will_dark_g6`, the German Will TTS set; the key was kept after the build was switched to Will
- C) `alien_mid_50_g4`, the English set
- D) None; Workshop variants are XML-only

**4. [Apply]** In `sound_attr_ops` someone writes `"op": "Add"` (capital A) for `noocclusion`. What happens on build and validate?

- A) `build_mod.py` raises `KeyError`
- B) The builder writes an `add` as before, because the comparison ignores case
- C) The builder writes a `<replace sel="…/@noocclusion">`; `validate_mod.py` then reports for each id that the attribute is missing ("add statt replace verwenden")
- D) The operation is skipped without a message

**5. [Apply]** You are about to upload a new German Workshop build manually. `config/variants.json` says `alien_ws` is version 102. What do you set?

- A) 103, the next number after the configured 102
- B) 104 or higher, because the last modpub upload made 103 the live version
- C) Leave 102; `WorkshopTool update` accepts any version
- D) 101, to mark it as a hotfix

**6. [Apply]** You are subscribed to the German Workshop item (`extensions\ws_3824406333\` exists in the game folder) and run `install_mod.py alien_en` locally. What is the result?

- A) The installer removes `ws_3824406333` first, so only `bosota_voice_alien_en` is active
- B) Both extensions are active and both patch the same six sound entries
- C) The installer refuses because a Workshop item is present
- D) The game merges both diffs, German lines for German ids and English lines for the rest

**7. [Design]** Why do the Workshop builds need variants of their own (`ws_<number>` ids), and why can such a variant only be added after the first upload?

**8. [Design]** Why is `is3d="0"` applied only to `10201_normal` and `10201_normal_npc`, and what does it cost on `10201_normal_npc`?

---

## Answers

**1. B.** The builder reads `id`, `audio_variant`, names, descriptions, `version` and `sound_attr_ops` (`tools/build_mod.py:29-56`, `:72`). The installer reads `id` and `audio_variant` (`tools/install_mod.py:100`, `:107`). `audio_recipe` (for example `config/variants.json:26`) is prose only. A, C and D are all read by code.

**2. B.** `version=q(v.get('version', cfg['version']))` (`tools/build_mod.py:54`), and the top level holds `"version": "100"` (`config/variants.json:9`). A is wrong because `.get` with a default cannot raise. D is wrong because the builder never reads old output.

**3. B.** `alien_ws` has `"audio_variant": "will_dark_g6"` (`config/variants.json:89`). The note explains it was created with the Alien audio and later switched (`config/variants.json:121`). A trusts the misleading key name. C belongs to the English variants. D is wrong: the installer always copies audio (`tools/install_mod.py:105-116`).

**4. C.** The builder writes an `add` only when `op == "add"` exactly; anything else becomes a `replace` on the attribute (`tools/build_mod.py:41-44`). `noocclusion` does not exist on those five entries in the base game, so the validator reports that the attribute is missing (`tools/validate_mod.py:105-106`). A and D are wrong because there is no lookup or filter on `op`. B is wrong because the comparison is case-sensitive.

**5. B.** The live German copy that modpub uploaded is at `version="103"` (`release/out/workshop/de/content.xml:2`, ignored by git), while the configuration still says 102 (`config/variants.json:120`). An update needs a version above the live one, or `-minor` (`docs/RELEASE.md:35`). A gives a value equal to the live version. C and D ignore the version rule.

**6. B.** The installer deletes only folders starting with `bosota_` (`tools/install_mod.py:30`, `:92-95`), so the `ws_` item stays, and both diffs target the same entries. A is wrong for that reason. C is wrong because there is no such check. D is wrong because a diff replaces each entry's `<sample>` as a whole (`tools/build_mod.py:33-35`); the game does not merge diffs by line id.

**7.** The redirect path contains the mod id (`tools/build_mod.py:29`), and Steam installs an item under the folder name `ws_<number>`. A build with `id: bosota_voice_will_de` would point at a folder that does not exist, and Boso would be silent (`docs/RELEASE.md:15`). The number exists only after the first `publishx4`. So you upload a placeholder first, read the `ws_` id the tool writes into `content.xml`, then add the variant and `update` (`docs/RELEASE.md:37`; history at `config/variants.json:121`, `:192`).

**8.** The audible problem was in-person talk at the HQ. Facing Boso he reached about 90 % of the manager Karee's loudness; with your back turned about 60 %, and he could not be understood (`config/variants.json:49`). Comm lines play through the comm window, where position did not cause trouble, so the comm entries stay positional. The cost on `10201_normal_npc`: his chatter with other NPCs no longer fades with distance and is equally loud anywhere on the platform.
