# x4mod_less_annoying_voices

**Projektmodus: P1** (mehrere Sitzungen, mehrere Meilensteine). Steuerung nach den Skills `anthropic-skills:projektsteuerung` und `anthropic-skills:dev-team-steuerung`. Sitzungsstart: `docs/projekt/MILESTONES.md`, `docs/projekt/CURRENT_STATE.md`, `git log` lesen, `./init.sh` laufen lassen, dann Standmeldung in fünf Zeilen.

## Was das ist

X4-Foundations-Mod, die Boso Tas Stimme (Stimm-Set 10201) über Engine-Effekte in `libraries/sound_library.xml` tiefer und wärmer macht. Keine Audiodateien im Repo, keine Egosoft-Assets. Fachlicher Stand: `docs/phase0-befund.md`; Herleitung: `docs/X4_Boso_Ta_Voice_Mod_Handoff.md`.

## Aufbau

```
config/variants.json          ← Varianten: 'alien' (Audio-Umleitung, empfohlen), 'de'/'en' (nur Engine-Effekte)
tools/build_mod.py            ← erzeugt dist/<id>/ (content.xml + sound_library.xml-Diff inkl. Attribut-Patches)
tools/validate_mod.py         ← prüft Selektoren und Attribut-Operationen gegen die echte sound_library.xml des Spiels
tools/install_mod.py          ← kopiert genau eine Variante (XML + Audio aus build/audio/) nach <Spiel>\extensions\
tools/process_audio.py        ← ffmpeg/Rubberband-Filterketten, zweistufige Lautheit, --gain-db; --list zeigt Varianten
tools/pitch_flatten.py        ← Praat-Vorstufe (Intonationsspitzen stauchen), läuft in build/venv
tools/x4cat_extract.py        ← .cat/.dat-Extraktor (Textindex + Rohdaten, kein XRCatTool nötig)
dist/                         ← fertige Extensions ohne Audio (committed)
diag/                         ← Diagnose-Extension v6 (Nachweis der Audio-Umleitung)
build/                        ← extrahierte Spieldateien, bearbeitetes Audio, Hörproben, venv – ignoriert
docs/projekt/                 ← MILESTONES.md, CURRENT_STATE.md
docs/dev-team/                ← ROUTING-LOG.md, LESSONS.md
```

## Befehle

```bash
python -I tools/process_audio.py --variant d12_alien_mid --gain-db 9 --src <originale> --dst build/audio/d12_alien_mid_g9
python -I tools/build_mod.py            # alle Varianten bauen
python -I tools/validate_mod.py         # gegen Spiel prüfen (Pflicht vor Install)
python -I tools/install_mod.py alien    # alien | de | en; --remove entfernt alle bosota_*
```
`-I` = isolierter Python-Modus (ignoriert Umgebungsvariablen und Nutzer-Site-Pakete; schützt vor untergeschobenen Modulen). Spielordner per `--game-dir` oder `X4_GAME_DIR`, Standard `C:\Steam\steamapps\common\X4 Foundations`. ffmpeg: vollständiger Build (`winget install Gyan.FFmpeg`), liegt unter `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_*\...\bin\` und ist in der Tool-Shell nicht im PATH (`--ffmpeg <pfad>`).

## Hörproben-Methode (hat sich bewährt)

Slovi entscheidet am Ohr, nicht an Zahlen, und hat nach eigener Aussage ein schlechtes Gehör. Deshalb: WAV-Proben per SendUserFile in Runden, eine Frage pro Runde, alle Proben gleich laut (−22 LUFS), Referenz immer dabei. **Pegel und Verständlichkeit nur im Spiel beurteilen**, nie an der WAV am PC (Verdeckung durch Spielkulisse, 3D-Verarbeitung).

## Regeln

- Kommunikation, Doku und Kommentare auf Deutsch. **Jeder gezeigte Shell-Befehl wird Option für Option erklärt.**
- Keine Egosoft-Dateien (Audio, extrahierte XML) committen; `build/` bleibt ignoriert.
- Es darf immer nur **eine** Variante im Spiel installiert sein (alle patchen dieselben Sound-IDs).
- Parameter nur in `config/variants.json` ändern, dann bauen und validieren; `dist/` nie von Hand editieren.
- Nicht ohne Auftrag committen oder pushen.

## Routing-Pfade

| Berührt | Mindeststufe |
|---|---|
| `tools/install_mod.py` (löscht Ordner im Spielverzeichnis) | S2 |
| `config/variants.json` Sound-ID-Listen (falsche ID = stiller Fehler im Spiel) | S2 |

## Spielfakten (verifiziert 2026-10-22, X4 9.00)

- Boso Ta = Page **10201** (geteiltes Set „Boron NPC 1 / Boron rep / Misc Plot Characters"); 6 Sound-IDs `10201_normal|normal_npc|comm|comm_signalleak|comm_npc|comm_broadcast`, keine hat `<effects>`.
- Effekte laut `sound_library.xsd`: `doppler`, `fade`, `filter`, `reverb`, `pitch(start,end,steps)` – kein Equalizer. Pitch = Resampling (Tempo ändert sich mit).
- Kein DLC patcht `10201_*`; keine Dependency nötig. Audio liegt nur in `01–09.cat`.
- Nutzerordner: `C:\Users\slovi\OneDrive\Documents\Egosoft\X4\34818113\`, Extension-Tabelle `content-MSI-PRODP20Z.xml`.
