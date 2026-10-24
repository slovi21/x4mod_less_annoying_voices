# Boso Ta – less annoying VOICE

**Summary (one line):** Replaces Boso Ta's squeaky voice in X4: Foundations with a calm, deep one. Separate downloads for the German and the English voice track.

## Description

Boso Ta, the Boron scientist at your headquarters, talks a lot, and his original voice is extremely high and shrill in both the German and the English track. This mod gives him a voice you can listen to for hours.

**German (DE):** all 2,324 of his German lines are spoken anew from the original game texts by a calm male voice, then lowered and warmed. Because the lines are generated from text, the pacing is natural and free of the original's accent. Line lengths differ slightly from the originals; lip sync is not preserved, which is barely noticeable with a character floating in a tank.

**English (EN):** his 1,750 English lines are the original recordings, processed: one octave lower, slightly alien timbre, mid-range emphasis for intelligibility. Timing and lip sync are unchanged.

Both versions also fix a playback problem: Boso Ta's conversations no longer get quiet and muffled when you turn away from him or when he is behind the glass of his tank.

## Installation

1. Download the ZIP for your voice track. Use the DE file if the game speaks German, the EN file if it speaks English. Do not install both.
2. Extract it into `<X4 installation>\extensions\`. You should end up with `extensions\bosota_voice_will_de\content.xml` (DE) or `extensions\bosota_voice_alien_en\content.xml` (EN). Do not rename the folder.
3. Start X4, open Extensions from the main menu and make sure the entry is enabled.

**Uninstall:** delete that folder.

## Please read

- Like every mod, this one marks the game as **modified**: no online Ventures in saves made while it is active, and the mark stays on those saves even after you remove the mod. Community reports say Steam achievements still unlock in modified games, except the two Venture-related ones; this is unverified for 9.00, so check before you rely on it.
- The Boron faction representative is voiced by the same actor and shares Boso Ta's voice set, so he gets the new voice too. No random NPCs are affected.
- No game files are changed; the mod only tells the game where to find Boso Ta's lines.
- Compatible with X4: Foundations 9.00. Mods that patch `libraries/sound_library.xml` for the same entries (sound overhauls) may conflict; the one loaded last wins.

## Credits and source

Built with ffmpeg, Rubberband and ElevenLabs (German voice "Will"). Source code, documentation and the build pipeline: https://github.com/slovi21/x4mod_less_annoying_voices

---

*Deutsch:* Die DE-Datei ist für die deutsche Sprachausgabe, die EN-Datei für die englische. ZIP nach `<X4>\extensions\` entpacken, Ordnernamen nicht ändern, im Spiel unter Erweiterungen aktivieren. Das Spiel gilt danach als modifiziert, auch nach dem Entfernen (keine Ventures; Steam-Erfolge funktionieren laut Spielerberichten weiter, außer den zwei Venture-Erfolgen, für 9.00 nicht geprüft). Deinstallation: Ordner löschen.
