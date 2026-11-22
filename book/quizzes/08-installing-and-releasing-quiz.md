# Quiz: Installing & Releasing

Chapter: [8 · Installing & Releasing](../08-installing-and-releasing.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Apply]** `bosota_voice_alien_en` is installed. You run `install_mod.py will`, but `build/audio/will_dark_g6/` is empty. What is the state of the game folder afterwards?

- A) Unchanged; the installer checks the audio before touching anything
- B) `bosota_voice_alien_en` is gone and nothing new is installed, so the game plays the original voice
- C) `bosota_voice_will_de` is installed with XML only
- D) `bosota_voice_will_de` is installed with the English audio left over from the previous install

**2. [Apply]** You staged the German Workshop build once with `install_mod.py alien_ws --game-dir build/workshop/stage2`. You run the same command again after a rebuild. What happens?

- A) The old `ws_3824406333` folder is replaced
- B) `shutil.copytree` raises `FileExistsError`, because only `bosota_*` folders are removed and `extensions/ws_3824406333` still exists
- C) The new files are merged into the existing folder
- D) The installer asks whether to overwrite

**3. [Apply]** X4 is running. You run `install_mod.py alien_en --game-dir build/workshop/moddb_en`. What does the running-game guard do?

- A) It refuses, because X4 is running
- B) Nothing; the guard is checked only when the target is the default game folder
- C) It asks for `--force`
- D) It waits until X4 closes

**4. [Recall]** Why does `game_running()` search the raw bytes of the `tasklist` output for `X4.exe`?

- A) Because bytes are faster to compare than strings
- B) `tasklist` writes in the console's OEM code page, and decoding it as another code page crashed; the ASCII name can be found without decoding
- C) Because `X4.exe` may appear in UTF-16
- D) To avoid matching `x4.exe` in lower case

**5. [Design]** Why does the installer refuse to swap the mod while X4 runs, and what does `--force` change?

**6. [Design]** Why are Workshop uploads made from staging copies under `build/workshop/`, never directly from `dist/<id>/` or the game's `extensions/` folder?

**7. [Recall]** Why is a new Workshop item first created with XML-only content?

- A) The Workshop rejects audio in a new item
- B) Creating an item together with 56 MB of audio timed out twice (Steam error 16), and the `ws_` number needed for the real build exists only after the first upload
- C) XML-only items skip Valve's review
- D) `-buildcat` cannot pack audio on the first upload

**8. [Apply]** The next German update is run with `-namedesc up`. What changes on the item page besides the files, and why might you not want that?

---

## Answers

**1. B.** Removal of every `bosota_*` folder (`tools/install_mod.py:92-95`) comes before the audio check that exits (`:107-110`). A describes what the comment at `:105-106` promises for the *new* variant only: nothing new is written before the check. C was the old bug. D is impossible because the old folder was deleted.

**2. B.** `PREFIX = "bosota_"` (`tools/install_mod.py:30`) limits removal to `bosota_*` (`:92-95`). `shutil.copytree(src, dst)` at `:111` has no `dirs_exist_ok`, so an existing `ws_3824406333` makes it raise. A and C would need `dirs_exist_ok=True` or a removal of `ws_*`. D: the installer never prompts. Fix: delete `build/workshop/stage2/extensions/ws_3824406333` by hand first.

**3. B.** The condition is `Path(args.game_dir).resolve() == Path(DEFAULT_GAME_DIR).resolve() and not args.force and game_running()` (`tools/install_mod.py:89-90`). A staging or packaging folder is not the default, so the check is skipped. That is correct, because the running game does not read those folders. A, C and D describe checks that apply only to the default folder or do not exist.

**4. B.** The comment and code are at `tools/install_mod.py:54-58`. Only the ASCII `X4.exe` is searched in the raw output. A is not the reason. C and D are not what the code handles. If `tasklist` is missing, the function returns `False` and does not block (`:56-57`).

**5.** X4 reads the diff at start-up. If the mod folder is deleted and replaced underneath the running game, the loaded redirect points at files that were just removed, and Boso goes silent with nothing in the log (`tools/install_mod.py:50-52`; `docs/phase0-findings.md:50`). `--force` only skips the `tasklist` check (`:81`, `:89`). It does not make the swap safe.

**6.** `publishx4` writes the new `ws_` id back into the uploaded folder's `content.xml` (`docs/RELEASE.md:37`). Uploading from `dist/` or the game folder would rewrite files those places should not have changed. Also, `dist/` holds only XML (`tools/build_mod.py:7`). The installer is what adds the audio in the installed layout (`tools/install_mod.py:107-115`), so staging with `install_mod.py <key> --game-dir build/workshop/stage2` produces exactly what subscribers should get.

**7. B.** Both facts are recorded in `docs/RELEASE.md:12` and `:37`. A and D are wrong: a later `update` with 90 MB of audio worked. C is not a recorded behaviour.

**8.** `-namedesc up` also pushes the title and description from `content.xml` (`docs/RELEASE.md:27`). The builder writes `name_en`, "Boso Ta - new VOICE Will (DE)" (`config/variants.json:90`, `tools/build_mod.py:53`). That would overwrite the title modpub set, "Boso Ta – erträgliche Stimme" (`release/out/workshop/de/content.xml:2`). Leave the flag out if the modpub title should stay.
