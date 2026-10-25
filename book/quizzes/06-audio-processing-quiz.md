# Quiz: Audio Processing

Chapter: [6 · Audio Processing](../06-audio-processing.md)

How to use: answer closed-book first, then check the answers and reread the cited code.

**1. [Recall]** Why are the pitch changes done with Rubberband instead of resampling?

- A) Rubberband is faster on many cores
- B) It changes pitch without changing tempo, so line lengths and the English lip sync are kept
- C) It normalises loudness at the same time
- D) It changes only the formants and leaves the pitch alone

**2. [Apply]** `alien_mid_50` is `alien_mid_scaled(0.5)`. Which part of the chain is *not* scaled by `k`?

- A) The pitch factor (0.7071, i.e. −6 semitones)
- B) The frequency shift (−35 Hz)
- C) The chorus depths
- D) The mid-range focus (band limits, EQ, compressor)

**3. [Apply]** With normalisation on and `--gain-db 4`, in what order is the second ffmpeg pass's filter chain built?

- A) Gain, limiter, variant chain, then `loudnorm` to −22 LUFS
- B) Variant chain, `loudnorm` in linear mode with the values from pass 1, `volume=4dB`, then `alimiter` at 0.891
- C) `loudnorm` on the untouched original, then the variant chain, then gain
- D) Variant chain, limiter, then `loudnorm` in dynamic mode

**4. [Apply]** You run `process_audio.py --src build\orig\voice-l044\10201\normal --dst build\audio\x --gain-db 4` and forget `--variant`. What happens?

- A) argparse errors out because `--variant` is required
- B) It prints the list of chains and exits with code 0; no file is written
- C) It processes the files with a default chain
- D) It applies only normalisation and gain

**5. [Apply]** Your ffmpeg build has no Rubberband filter. What does a full run do?

- A) `find_ffmpeg` rejects that build and the tool exits before any file
- B) Each file fails with an ffmpeg filter error, the error is printed and counted, the other files are still tried, and the exit code is 1
- C) The files are written without pitch change
- D) The tool falls back to `asetrate` resampling

**6. [Apply]** You point `--src` at `build/tts/will_de` (WAV output of the TTS tool) and leave the other options as for the originals. What happens?

- A) The WAVs are processed as usual
- B) The tool exits with "no files in build\tts\will_de", because it looks for `*.ogg` by default
- C) Each WAV fails in ffmpeg
- D) It processes the WAVs but writes WAV output

**7. [Design]** Why does the tool add gain (with a limiter) after normalising to −22 LUFS, when −22 LUFS is the measured loudness of the originals? And what does the limiter not guarantee?

---

## Answers

**1. B.** The chains use `rubberband=pitch=…` (`tools/process_audio.py:31-33`). The module docstring states the tempo is unchanged (`:3`). A is not a stated reason, and the work runs in ffmpeg anyway. C is wrong: loudness is a separate `loudnorm` step (`:61`). D is wrong: the formant mode is a separate option on top of the pitch change.

**2. D.** `alien_mid_scaled` scales the pitch (`2 ** (-k)`), the shift (`-70 * k`) and the chorus parameters, then appends the constant `MID` (`tools/process_audio.py:41-48`, `MID` at `:37-38`). The mid-range focus serves intelligibility, not character. A, B and C are all derived from `k`.

**3. B.** Pass 2 uses `{af},{LOUD}:measured_…:linear=true` (`tools/process_audio.py:92-93`), then adds `volume` and `alimiter=limit=0.891` (`:94-95`). Pass 1 measures loudness after the chain (`:87`). A, C and D change the order or the mode. The chain must run before the measurement because pitch and EQ change loudness.

**4. B.** `if args.list or not args.variant:` prints the chains and returns (`tools/process_audio.py:117-120`). A is wrong: `--variant` is optional in argparse (`:104`). C and D are wrong because no chain is applied without a variant.

**5. B.** `find_ffmpeg` only looks for the executable (`tools/process_audio.py:64-74`). The filter error comes back per file as a non-zero return code (`:97-98`), and it is counted and printed while the pool continues (`:141-145`). The exit code is 1 (`:149`). A, C and D assume a feature check or fallback that does not exist.

**6. B.** The source glob is `*.{args.src_ext}` with default `ogg` (`tools/process_audio.py:107`, `:126`). An empty list exits with "no files in …" (`:132-133`). You need `--src-ext wav`. A and C would require WAVs to be found. D confuses the source extension with `--wav`, which controls the output format (`:110`, `:135`).

**7.** Equal LUFS did not mean equal perceived loudness in the game. Dark voices lose the 1–4 kHz energy that cuts through the mix, so they need extra level (`tools/process_audio.py:4-5`; `docs/HISTORY.md:39`). The limiter caps the **sample** peak at 0.891 (−1 dBFS, `:95`). True peaks between samples can still be higher; the final Will set measures about −0.5 dBTP.
