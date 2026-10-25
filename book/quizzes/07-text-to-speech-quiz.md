# Quiz: Text-to-Speech

Chapter: [7 · Text-to-Speech](../07-text-to-speech.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Recall]** Where does `tts-batch` get the list of line ids to generate?

- A) Every `<t id>` in page 10201 of the text file
- B) The stems of the `.ogg` files in the `--ids-from` folder
- C) The six sound entries in `sound_library.xml`
- D) The index that `check_coverage.py --save-index` stored

**2. [Apply]** After a patch you run `tts-batch` with `--ids-from build/audio/will_dark_g6` (the processed German set) instead of the freshly extracted originals. What happens to the new lines?

- A) They are generated, because the text page lists them
- B) None are generated: the folder lacks the new ids, so the plan contains only ids that already have WAVs, and the tool reports 0 to generate
- C) The tool refuses because the folder holds processed files
- D) All 2,324 lines are generated again

**3. [Apply]** The API key has been revoked, so every request returns HTTP 401. What does a batch of 300 lines do?

- A) Each request is retried five times with growing pauses
- B) Each line fails at once without retry; the batch goes on through all lines and ends with exit code 1
- C) The first failure stops the batch
- D) The tool waits and retries until the key works again

**4. [Apply]** In the middle of a batch, one request raises a `requests` timeout exception. What happens?

- A) Only that line fails; the summary line counts it as failed
- B) The exception comes back out of `fut.result()`, but leaving the `with ThreadPoolExecutor` block waits for queued work, so the remaining lines are still generated and billed; then a traceback appears and the summary line is lost
- C) The pool is cancelled at once and no more credits are spent
- D) The tool retries that line five times like a 429

**5. [Apply]** You run a repair batch without `--model`. Which model speaks the new lines?

- A) `eleven_v4_turbo`, read from the variant's recipe in `config/variants.json`
- B) `eleven_multilingual_v2`, the CLI default, which does not match the published set
- C) None; `--model` is required
- D) The model of the voice's last use on the account

**6. [Apply]** A text entry reads `<t id="30200001">(eager; interjects)Hello {20102,1051}there</t>`. What text is sent to ElevenLabs?

- A) `(eager; interjects)Hello {20102,1051}there`
- B) `Hello there`
- C) `eager; interjects Hello there`
- D) `Hellothere`

**7. [Apply]** Five German ids (`10417`, `10603`, `30226001`–`30226003`) have no text. What does `tts-batch` do with them, and how does the Will set still reach 2,324 files on a fresh clone?

**8. [Design]** Why was the German voice made with text-to-speech instead of filtering or speech-to-speech conversion, and what did that cost?

---

## Answers

**1. B.** `ids = sorted(p.stem for p in Path(args.ids_from).glob("*.ogg"))` (`tools/voice_convert_elevenlabs.py:134`). That guarantees exactly the ids the game will request. A is wrong because text entries without audio are ignored. C confuses sound entries with line ids. D belongs to the coverage tool (`tools/check_coverage.py:81-89`).

**2. B.** The plan comes from the `--ids-from` folder (`tools/voice_convert_elevenlabs.py:134`). Ids whose WAV already exists are removed from `todo` (`:146`), so nothing is left. A ignores where the ids come from. C is wrong: the folder is not inspected beyond its file names. D is wrong because existing WAVs are skipped.

**3. B.** Only 429 and 5xx are retried (`tools/voice_convert_elevenlabs.py:91-93`). Any other non-200 returns `HTTP …` at once (`:94-95`). The batch counts it as failed and continues (`:159-163`), then exits 1 (`:167`). A applies to 429/5xx. C and D describe behaviour the code does not have.

**4. B.** `tts_one` does not catch `requests` exceptions (`tools/voice_convert_elevenlabs.py:83-90`). `fut.result()` re-raises them inside the `with` block (`:155-158`), and leaving that block waits for the queued futures. A would need a `try`. C is wrong because queued work is not cancelled. D confuses an exception with an HTTP 429 status.

**5. B.** `--model` defaults to `eleven_multilingual_v2` (`tools/voice_convert_elevenlabs.py:183`). The published set used `eleven_v4_turbo`, which appears only in the recipe text (`config/variants.json:94`). A is wrong because no tool reads `audio_recipe`. C is wrong because the option has a default.

**6. B.** Parenthesised stage directions are removed (`tools/voice_convert_elevenlabs.py:121`), then `{n,n}` references (`:122`), then whitespace is collapsed and stripped (`:124`). That leaves `Hello there`. A ignores the cleaning. C keeps the stage direction. D forgets that the space before `{` survives the removal.

**7.** They have no text, so they go to `missing` and are printed as "without text" (`tools/voice_convert_elevenlabs.py:139`, `:149-150`). No WAV is made. The recipe fills them by copying from `build/audio/d12_alien_mid_g9` (`config/variants.json:94`, `:130`). On a fresh clone that folder must first be rendered for just these five ids with `process_audio.py --variant d12_alien_mid --gain-db 9 --files 10417,10603,30226001,30226002,30226003 …`. They then sound like the processed original, not like Will.

**8.** The German actor's regional (Saxon) colouring survived every filter chain. Speech-to-speech with all 21 premade ElevenLabs voices kept it too (`docs/HISTORY.md:43`). TTS starts from the words, so it cannot inherit the accent. The cost: line lengths differ from the originals, so lip sync is lost. Generation also needs a paid API and credits (`tools/voice_convert_elevenlabs.py:1-4`).
