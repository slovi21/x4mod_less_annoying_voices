# Quiz: Core Concepts & Domain Model

Chapter: [2 · Core Concepts & Domain Model](../02-core-concepts.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Recall]** With the mod `bosota_voice_will_de` installed, which folder does the sound entry `10201_comm_broadcast` read?

- A) `extensions\bosota_voice_will_de\voice\10201\comm_broadcast`
- B) `extensions\bosota_voice_will_de\voice\10201\normal`
- C) `voice-l049\10201\comm_broadcast` (unchanged, only `normal` is redirected)
- D) `extensions\bosota_voice_will_de\voice-l049\10201\normal`

**2. [Recall]** How are a line id, an audio file and a text entry related?

- A) The line id is the `.ogg` file stem and also the `<t id>` inside page 10201 of `t/0001-l0XX.xml`
- B) The line id is the sound id, for example `10201_normal`
- C) Text ids are offsets into the `.dat` file and are mapped to line ids through the `.cat` index
- D) Each context has its own numbering, so the same line has different ids in `normal` and `comm`

**3. [Apply]** The German track has a file `30201430fp.ogg`, but page 10201 has no `<t id="30201430fp">`. What text does `tts-batch` speak for it?

- A) None; the id is listed as "without text"
- B) The text of `30201430`, because trailing lowercase letters are stripped as a fallback
- C) The literal string "fp"
- D) The request is sent with an empty text and ElevenLabs returns an error

**4. [Recall]** Why is `10201_comm_signalleak` missing from the `noocclusion` list?

- A) Signal leaks are supposed to sound muffled
- B) It already has `noocclusion="true"` in the base game, so an `add` would be an error
- C) It is not one of Boso Ta's entries
- D) The game never plays it

**5. [Apply]** An English-speaking player installs the German Will variant (`install_mod.py will`) and plays with English voices. What do they hear when Boso Ta speaks?

- A) The original English Boso Ta, because the German mod applies only to German voice language
- B) The German Will recordings
- C) Silence for every line
- D) The English originals with the mod's `is3d`/`noocclusion` changes only

**6. [Recall]** Which statement about the "modified" state is correct?

- A) `save="0"` in `content.xml` prevents the game from being marked as modified
- B) Any unsigned extension marks the game as modified; `save="0"` only means saves do not list the mod as a requirement
- C) Only Workshop items mark the game as modified
- D) Only diffs on `sound_library.xml` trigger it; audio-only mods do not

**7. [Recall]** Who besides Boso Ta at the HQ is affected by a mod that redirects page 10201?

- A) Nobody; the page belongs to one character macro
- B) Every Boron NPC, because all Boron voices share page 10201
- C) Also the Boron faction representative (and Boso Ta's clone and the scenario narrator), because the page is assigned per actor
- D) Only Nila, who borrows Boso's lines in the Boron DLC

**8. [Design]** After the redirect all six entries read the same `normal` folder. Name one consequence for what players hear, and one consequence for which line files the project has to produce and check.

---

## Answers

**1. B.** Every entry in `boso_ta_ids` gets the same target, `extensions\<id>\voice\10201\normal` (`tools/build_mod.py:29-35`, `config/variants.json:10-17`). A is wrong because the context is not part of the target. C is wrong because all six entries are redirected, not only `normal`. D is wrong because the path has no language suffix (`docs/phase0-findings.md:47`).

**2. A.** `tts-batch` takes the ids from the original file stems and looks them up in the text page (`tools/voice_convert_elevenlabs.py:134-138`). The texts are keyed by `<t id>` (`tools/voice_convert_elevenlabs.py:120`). B confuses line ids with sound entry ids. C confuses them with catalog offsets (`tools/x4cat_extract.py:33-34`). D is wrong: each context holds a copy of every line under the same id.

**3. B.** `base = re.sub(r"[a-z]+$", "", i)` and `texts.get(i) or texts.get(base)` (`tools/voice_convert_elevenlabs.py:137-138`). A applies only when the base id has no text either (`:139`). C and D misread the fallback: no request is ever made without a text.

**4. B.** The configuration says so (`config/variants.json:39`), and the validator flags an `add` on an attribute that already exists (`tools/validate_mod.py:93-94`). A is the opposite of the intent. C is wrong: it is in `boso_ta_ids` and is redirected (`config/variants.json:14`). D is wrong: it is a real entry for signal leaks.

**5. B.** The redirect ignores the voice language (`tools/build_mod.py:29`). The English game requests its line ids from the German folder, which holds every English id among its 2,324 files, so German lines play (`book/13-failure-modes.md:13`). A assumes a language filter that does not exist. C would only happen if the ids were missing. D is wrong because the whole `<sample>` is replaced, not only the attributes (`tools/build_mod.py:33-35`).

**6. B.** `save="0"` is written by the builder (`tools/build_mod.py:54`), but the modified mark comes from loading any unsigned file (`docs/HOW-IT-WORKS.md:32`). A is the misconception the chapter warns about. C and D are too narrow: every extension counts, including local installs.

**7. C.** The page is set per actor in the mission scripts, and `factionrepresentative_boron` also uses 10201 (`docs/phase0-findings.md:16`, `:18`). A is wrong because the page is not tied to a macro. B is wrong because generic Boron NPCs use 10202–10205. D is wrong because Nila has her own page, 10251.

**8.** For players: the comm recordings' radio colouring is lost, because comm entries now play the processed in-person set (`tools/build_mod.py:32-35`; accepted in `book/13-failure-modes.md:17`). For the project: only context `normal` has to be produced, installed and checked. That is why the installer copies into `voice/10201/normal` only (`tools/install_mod.py:112`) and the coverage check defaults to `context="normal"` (`tools/check_coverage.py:32`).
