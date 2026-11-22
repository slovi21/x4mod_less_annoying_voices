# Quiz: Building & Validating

Chapter: [5 · Building & Validating](../05-building-and-validating.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Recall]** For each of the six sound entries, what does the generated diff replace?

- A) Only the `start` attribute of `<sample>`
- B) The whole `<sample>` element; sibling elements such as `<volume>` stay untouched
- C) The whole `<sound>` element, rebuilt from the configuration
- D) Nothing is replaced; a second `<sample>` is added and the engine uses the last one

**2. [Apply]** You run `python -I tools/build_mod.py --only alien-en` (typo; the key is `alien_en`). What happens?

- A) argparse rejects the unknown key and lists the valid ones
- B) Nothing is built, nothing is printed, and the exit code is 0
- C) All variants are built, because the filter matches nothing
- D) `KeyError: 'alien-en'`

**3. [Apply]** A patch renames `10201_comm_npc` in the game's `sound_library.xml`. What does `validate_mod.py` report, and what would the game do without the check?

- A) Nothing; the validator only checks that the XML is well-formed
- B) "No matching node" for both the `<sample>` replace and the `noocclusion` add of that id, exit code 1; in the game that entry would keep its original voice
- C) A warning only, because a missing entry is harmless
- D) A crash of the validator with a traceback

**4. [Recall]** Which mistake does `validate_mod.py` *not* catch?

- A) `add` of an attribute that already exists
- B) A redirect pointing at an `extensions\<id>` folder that will not exist, or an audio folder with no files
- C) A malformed diff
- D) A selector that matches no node

**5. [Apply]** You removed a variant from the configuration, and its old `dist/<id>/` still exists but has lost `content.xml`. What does `./init.sh` do?

- A) `build_mod.py` deletes the stale folder
- B) The validator skips it because it is not in the configuration
- C) The validator raises an uncaught `FileNotFoundError`, and `init.sh` stops with a non-zero exit code
- D) The validator prints a warning and continues

**6. [Design]** `content.xml` values go through `quoteattr`, but the diff is assembled with plain f-strings. Why does the first matter so much, and why has the second never caused trouble?

**7. [Design]** Why does `validate` apply every extension's operations to `copy.deepcopy(base_root)` instead of to the shared parsed base?

**8. [Design]** The validator never applies DLC diffs to the base file. Why is that acceptable today, and what would make it unsafe?

---

## Answers

**1. B.** The selector ends in `/sample`, and the replacement is a new `<sample start="…"/>` (`tools/build_mod.py:33-35`). The validator replays it as removing and inserting an element, leaving the siblings alone (`tools/validate_mod.py:123-131`). A would need a `…/sample/@start` selector. C and D do not match the generated XML.

**2. B.** `--only` is a free string, not a `choices` list (`tools/build_mod.py:62`). The loop simply skips every key that differs (`:65-67`). A is wrong because there are no choices to check. C inverts the filter. D is wrong because the key is never used to index the dict.

**3. B.** The element `replace` finds no target and records "No matching node" (`tools/validate_mod.py:111-114`). The attribute `add` does the same (`:89-91`), and any error gives exit code 1 (`:188`). In the game, X4 logs the failed selector and plays the original voice for that entry (`docs/MAINTENANCE.md:21`). A and C understate the check. D is wrong because a missing node is handled, not an exception.

**4. B.** The validator prints the final `sample start` but never checks that the folder or the audio exists (`tools/validate_mod.py:163-166`). A is caught at `:93-94`, C at `:72-76`, D at `:111-114`.

**5. C.** Without folder arguments the validator checks every folder in `dist/` (`tools/validate_mod.py:177`). Only `ET.ParseError` is caught around `content.xml` (`:62-69`), so a missing file raises. `set -e` stops the script (`init.sh:4`). A is wrong: the builder never deletes (`tools/build_mod.py:69`). B is wrong: the validator does not read the configuration. D is wrong because a missing file is not a parse error.

**6.** An unescaped `&` in `content.xml` makes X4 drop the extension without any message, so every value goes through `quoteattr` (`tools/build_mod.py:50`). The diff is assembled with f-strings (`tools/build_mod.py:29-44`). That is safe only because ids, sound ids, attribute names and values in the configuration are plain identifiers. A quote, `&` or `<` there would break the XML or the selector. The validator would catch broken XML (`tools/validate_mod.py:72-76`).

**7.** Each extension must be checked against the real base file, not against a file already changed by another extension. Without the copy, the second variant's `add` of `noocclusion` would find the attribute set by the first variant and report "existiert bereits" (`tools/validate_mod.py:58`, `:93-94`).

**8.** No DLC diff touches the `10201_*` entries (`docs/phase0-findings.md:20`), so the effective entries equal the base catalog's version that `load_base` uses (`tools/validate_mod.py:32-40`). It would become unsafe if a DLC or patch started to change those entries in a DLC catalog. The validator would then pass against a base the game no longer uses.
