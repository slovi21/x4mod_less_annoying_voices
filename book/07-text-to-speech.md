# 7 · Text-to-Speech (`tools/voice_convert_elevenlabs.py`)

> **What you'll be able to answer after this chapter:** why the German voice is generated from text instead of converted from audio (rationale), how game texts are matched to line ids (flow, data), the API contract and retry behaviour (contracts, failure), how the API key is handled (security), and what a run costs (operations).

## Why it exists

The German original actor has a regional colouring that survived every filter chain, and speech-to-speech conversion with all 21 ElevenLabs premade voices carried it into every result. Text-to-speech starts from the words, not the recording, so it cannot inherit the accent. The price is that line lengths differ from the originals and lip sync is lost, which the author accepted for a character floating in a tank (`docs/HISTORY.md`, "Plan C").

## Public surface

`build\venv\Scripts\python.exe -I tools/voice_convert_elevenlabs.py <command>`; it needs the `requests` package, which is why it runs in the project venv (`:9-16`, `:27`). After the repository moved on 2026-10-24 the venv's absolute paths are stale; recreate it with `python -m venv build\venv` and `build\venv\Scripts\python.exe -m pip install requests`.

| Command | What it does | Lines |
|---|---|---|
| `quota` | Prints plan, used and remaining credits | `:54-60` |
| `voices [--filter s]` | Lists the account's voices with gender, age, accent, use case; substring filter on the printed line | `:63-77` |
| `tts --voice --text --out [--model …]` | One text → one WAV (for samples) | `:104-109` |
| `tts-batch --voice --tfile --ids-from --dst [--page 10201] [--model] [--files] [--limit] [--dry-run] [--jobs 2]` | Every line id of a folder → one WAV each | `:129-167` |

Voice settings default to stability 0.5, similarity 0.75, style 0, speaker boost on (`:82`, `:183-186`). The published German set used voice `bIHbv24MWmeRgasZH58o` ("Will") and model `eleven_v4_turbo`; the CLI default model is `eleven_multilingual_v2`, so the model must be passed explicitly (`config/variants.json:130`).

## Matching texts to line ids

```python
texts = load_texts(args.tfile, args.page)                 # → {"30201131": "There are actually …", …}
ids = sorted(p.stem for p in Path(args.ids_from).glob("*.ogg"))   # → the ids come from the ORIGINAL audio files
for i in ids:
    base = re.sub(r"[a-z]+$", "", i)                      # → "30201430fp" → "30201430"
    txt = texts.get(i) or texts.get(base)                 # → alternate takes reuse the base line's text
    (plan if txt else missing).append((i, txt))
```
(`tools/voice_convert_elevenlabs.py:133-139`)

`load_texts` (`:112-126`) cuts page `10201` out of the text file with a regex and cleans each entry: stage directions in parentheses `(eager; interjects)` are removed (`:121`), references like `{20102,1051}` are removed (`:122`), colour codes `\033X` are removed (`:123`), whitespace is collapsed (`:124`). Driving the plan from the original audio files, not from the text page, guarantees that exactly the ids the game will request are generated and that text entries without audio are ignored.

**Five ids have no text** (`10417`, `10603`, `30226001`–`30226003`); they are listed as "without text" and must be filled from another variant. The recipe copies them from `build/audio/d12_alien_mid_g9` (`config/variants.json:130`). On a fresh clone that folder does not exist yet; render just these five first:

```powershell
python -I tools/process_audio.py --variant d12_alien_mid --gain-db 9 --files 10417,10603,30226001,30226002,30226003 --src build\orig\voice-l049\10201\normal --dst build\audio\d12_alien_mid_g9
```

They then sound like the processed original (Alien chain, +9 dB), not like Will: a deliberate compromise for five lines without text.

## The API call

```python
for attempt in range(5):
    r = requests.post(f"{API}/text-to-speech/{voice_id}",
                      headers={**headers(), "Content-Type": "application/json"},
                      params={"output_format": output_format},          # → mp3_44100_128
                      json={"text": text, "model_id": model, "voice_settings": settings},
                      timeout=180)
    if r.status_code == 429 or r.status_code >= 500:
        time.sleep(3 * (attempt + 1))                                    # → 3, 6, 9, 12, 15 s
        continue
    if r.status_code != 200:
        return f"HTTP {r.status_code}: {r.text[:160]}"                   # → 4xx other than 429: no retry
    break
else:
    return "gave up after retries"
p = subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", "pipe:0", "-ar", "44100", "-ac", "1", str(dst)], input=r.content, …)
```
(`tools/voice_convert_elevenlabs.py:82-101`)

The MP3 from the API is converted to 44.1 kHz mono WAV through ffmpeg's stdin.

**Failure behaviour in a batch:**

- **429 and 5xx** are retried five times with growing pauses; then the line fails with "gave up after retries".
- **Any other 4xx** (invalid key 401, no credits left, library voice on a free plan 402) fails that line immediately without retry. The batch continues, so every remaining line fails fast the same way; the run ends with exit code 1. After fixing the cause (new key, top-up), rerun the same command: finished WAVs are skipped.
- **A network exception** (`requests` timeout, connection reset) is not caught inside `tts_one`. `fut.result()` re-raises it in the main thread inside the `with ThreadPoolExecutor` block (`:156-159`). Leaving that block calls `shutdown(wait=True)`, which does **not** cancel queued work: every remaining line is still generated and billed, then the traceback appears and the summary line is lost. Rerunning afterwards finds those WAVs and skips them.

## Resumability and concurrency

`todo` excludes every id whose WAV already exists (`:146`), so an interrupted run is restarted with the same command and only pays for what is missing. A partially written WAV would count as done; ffmpeg writes the file only after the response is complete, which makes that unlikely but not impossible. `--jobs` (default 2) controls parallel requests; the published run used 3 and produced about 40 lines per minute.

## Security

- The key comes from `ELEVENLABS_API_KEY` or the file `%USERPROFILE%\.elevenlabs_key` (`:39-47`); it is sent only in the `xi-api-key` header (`:50-51`) and never printed.
- `.gitignore` excludes `.elevenlabs_key` and `*.key`.
- The key must be able to read user data for `quota`; a key without that permission returns 401 for `quota` while TTS still works (`docs/dev-team/LESSONS.md`).

## Cost

Measured on the German run: 183,227 characters after cleaning, 40,286 credits including about 60 test generations, i.e. about 0.2 credits per character with Eleven v4 Turbo, well below the published 0.5. `--dry-run` prints ids and characters before anything is spent (`:148-152`).

## Traced example

`tts-batch --voice bIHbv24MWmeRgasZH58o --model eleven_v4_turbo --tfile build/base/t/0001-l049.xml --ids-from <orig>/voice-l049/10201/normal --dst build/tts/will_de --files 30201131`:

1. Text page 10201 → id `30201131` → "Tatsächlich sind mehrere Schiffe involviert, um eventuelle Verfolger in die Irre zu führen."
2. Plan: 1 id, 1 with text, 0 to skip, about 90 characters.
3. POST, 200, MP3 → `build/tts/will_de/30201131.wav`.
4. Next step outside this tool: `process_audio.py --variant will_dark --src-ext wav --gain-db 6`.

## Where to look

`tools/voice_convert_elevenlabs.py`, `config/variants.json` (`audio_recipe` of `will`), `docs/RELEASE.md` and `docs/HISTORY.md` for licence and decisions.

## Open questions

- ElevenLabs' actual billing for v4 Turbo (0.2 measured versus 0.5 published) may change; budget with the published rate.

→ Check your understanding: [quizzes/07-text-to-speech-quiz.md](quizzes/07-text-to-speech-quiz.md)
