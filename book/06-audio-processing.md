# 6 · Audio Processing (`tools/process_audio.py`)

> **What you'll be able to answer after this chapter:** what each of the three filter chains does to the sound and why (rationale, mechanism), how two-pass loudness normalisation and gain work (flow), what the tool guarantees about its output (contracts), and how it fails (failure, concurrency).

## Why it exists

Both published variants need audio that the game can play in place of the originals: same format (Ogg Vorbis, mono, 44.1 kHz), comparable loudness, and for the English variant the same length as the original so lip sync survives. The tool wraps ffmpeg and turns "a folder in, a folder out, a named chain" into one command.

## The chains

Defined in `tools/process_audio.py:31-59`.

```python
def rb(pitch, formant="shifted"):
    return f"rubberband=pitch={pitch}:formant={formant}:pitchq=quality"
    # → pitch factor 2^(semitones/12); Rubberband keeps the tempo, unlike resampling

MID = ("highpass=f=220,lowpass=f=5500,equalizer=f=1400:t=q:w=1.0:g=4,equalizer=f=2800:t=q:w=1.2:g=2,"
       "acompressor=threshold=-20dB:ratio=2.5:attack=8:release=150")
    # → band-limit to speech, lift 1.4 and 2.8 kHz, gentle compression: intelligibility in the game mix

def alien_mid_scaled(k):
    pitch = round(2 ** (-k), 4)                 # → k octaves down: k=1 → 0.5, k=0.5 → 0.7071
    shift = round(-70 * k)                      # → frequency shift in Hz, makes the voice "un-human"
    d1, d2 = round(0.4 * k, 3), round(0.32 * k, 3)
    p1, p2 = round(2 * k, 2), round(1.3 * k, 2)
    return ",".join([rb(pitch), f"afreqshift=shift={shift}", f"chorus=0.6:0.9:50|60:{d1}|{d2}:0.25|0.4:{p1}|{p2}", MID])
```

| Chain | Expression | Used by | Why |
|---|---|---|---|
| `d12_alien_mid` | `alien_mid_scaled(1.0)` | `alien` (DE, +9 dB) | One octave with shifted formants removed the squeak; frequency shift and chorus made it "alien"; the mid-range focus restored intelligibility in the game |
| `alien_mid_50` | `alien_mid_scaled(0.5)` | `alien_en`, `alien_en_ws` (EN, +4 dB) | The English original is less shrill; full strength was "too unintelligible", half was right |
| `will_dark` | `rb(0.7937)` + low shelf +4 dB @220 Hz + high shelf −4 dB @4 kHz | `will`, `alien_ws` (DE TTS, +6 dB) | The TTS voice was good but should be "darker, warmer, deeper": −4 semitones |

Formants `shifted` (the default of `rb`) makes the speaker sound larger rather than the same person singing lower; that choice won in listening tests. The mid-range focus is deliberately **not** scaled by `k`: it serves intelligibility, not character.

## `convert`: one file

```python
if normalize:
    r1 = run([ffmpeg, …, "-i", str(src), "-af", f"{af},{LOUD}:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r1.stderr, re.S)   # → loudnorm prints its JSON to stderr
    …
    chain = (f"{af},{LOUD}:measured_I=…:measured_TP=…:measured_LRA=…:measured_thresh=…:offset=…:linear=true")
if gain_db:
    chain += f",volume={gain_db}dB,alimiter=limit=0.891:attack=5:release=60:level=false"   # → 0.891 = −1 dBFS
codec = ["-c:a", "pcm_s16le"] if wav else ["-c:a", "libvorbis", "-q:a", "3"]
r = run([ffmpeg, "-y", "-loglevel", "error", "-i", str(src), "-af", chain, "-ac", "1", "-ar", "44100", *codec, str(dst)])
```
(`tools/process_audio.py:86-97`)

- **Pass 1** measures the loudness of the **already processed** signal (chain + `loudnorm` in analysis mode).
- **Pass 2** applies the chain and `loudnorm` in **linear** mode with the measured values, i.e. a constant gain to −22 LUFS. −22 LUFS is the measured loudness of the originals; the target also sets a true-peak ceiling of −3 dBTP and a loudness range of 9 LU (`LOUD`, `:61`). Caveat: ffmpeg's `loudnorm` silently falls back to dynamic mode when a constant gain cannot meet the true-peak target, so "no pumping" holds for typical speech lines but is not guaranteed for every file.
- **Gain** comes after normalisation, capped by a limiter at 0.891 linear (−1 dBFS **sample** peak, `:95`). True peaks can still be higher: the final German Will set measures about −0.5 dBTP, the earlier Alien set −0.3 dBTP (`docs/dev-team/LESSONS.md`). It exists because equal LUFS did not mean equal perceived loudness in the game: dark voices lose the 1–4 kHz energy that cuts through the mix ([ch. 13](13-failure-modes.md)).
- Output is always mono 44.1 kHz; Ogg quality 3 (≈ 112 kbit/s, larger than the game's ≈ 48 kbit/s originals; inference: chosen for quality, size was never a constraint).

Returns `(file name, return code, stderr)`; it never raises for ffmpeg failures.

## CLI

`python -I tools/process_audio.py --variant <chain> --src <folder> --dst <folder> [--src-ext ogg|wav] [--files id,id] [--limit N] [--wav] [--no-normalize] [--gain-db X] [--jobs N] [--ffmpeg path]`, or `--list` (`:101-122`).

- `--src-ext wav` is needed for TTS output (`:107,126`).
- `--files` filters by file stem; `--limit` takes the first N in sorted order.
- `--wav` writes samples for listening on the PC.
- Default `--jobs` = CPU count − 1, at least 2 (`:113`).

## Concurrency

A `ThreadPoolExecutor` runs one `convert` per file (`:139-147`); each runs two ffmpeg subprocesses. Threads only wait on subprocesses, so the GIL is irrelevant. Output files are distinct, so there is no shared state. A full German run (2,324 files) takes about ten minutes on eight cores.

## Errors & edge cases

| Situation | Behaviour |
|---|---|
| ffmpeg not found | `find_ffmpeg` checks `--ffmpeg`, `FFMPEG`, `PATH`, then the winget package folders, then `C:\ffmpeg\bin`; otherwise exits (`:64-74`) |
| ffmpeg without Rubberband | every file fails with an ffmpeg filter error; counted and printed |
| `loudnorm` JSON not found | that file fails with "loudnorm measurement failed" (`:89-90`) |
| No input files | exits "no files in …" (`:132-133`) |
| Some files fail | the rest continue; exit code 1, each failure printed (`:143-149`) |
| `acompressor makeup=0` | rejected by ffmpeg (range 1–64); the parameter is therefore omitted |
| Rubberband latency | output is about 60 ms longer than the input; harmless for dialogue |
| Re-run into the same folder | files are overwritten (`-y`); there is no skip logic, unlike the TTS tool |

## Where to look

`tools/process_audio.py`, `config/variants.json` (`audio_recipe`), `docs/HISTORY.md` (every chain that was tried and rejected).

→ Check your understanding: [quizzes/06-audio-processing-quiz.md](quizzes/06-audio-processing-quiz.md)
