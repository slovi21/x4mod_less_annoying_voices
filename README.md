# Boso Ta – weniger nervige Stimme (X4: Foundations)

Mod für **X4: Foundations 9.00**, die die Stimme des Boronen-Beraters **Boso Ta** erträglich macht. Ergebnis nach sieben Hörrunden: eine Oktave tiefer, fremder Klang („Alien"), Mitten-Filter für Verständlichkeit, Gespräche ohne Raumverarbeitung. Tempo, Pausen und Mundbewegung bleiben exakt wie im Original, weil die Tonhöhe tempoerhaltend (Rubberband) geändert wird.

Die Mod enthält **keine Egosoft-Audiodateien im Repository**. Die bearbeiteten Dateien werden lokal aus deiner Spielinstallation erzeugt (ca. 10 Minuten) und beim Installieren in den Spielordner kopiert. Deinstallation = Ordner löschen. Spielstände werden nicht als modifiziert markiert (`save="0"`).

> Boso Ta spricht über das Stimm-Set **10201**. Der einzige weitere Nutzer ist der Boronen-Fraktionsvertreter (derselbe Sprecher), der die Stimme mitbekommt. Zufalls-NPCs sind nicht betroffen.

## Was die Mod technisch tut

1. `libraries/sound_library.xml` (XML-Diff): Die sechs Sound-Einträge `10201_*` zeigen statt auf die Originaldateien auf `extensions\bosota_voice_alien\voice\10201\normal\`. Die Engine lädt diesen Pfad wörtlich, ohne Sprachsuffix (Nachweis: `diag/`).
2. Dieselben Einträge bekommen `noocclusion="true"` (keine Dämpfung durch die Tank-Scheibe) und die Gesprächseinträge `is3d="0"` (keine Abhängigkeit von Blickrichtung und Abstand).
3. `voice/10201/normal/*.ogg`: 2 324 deutsche Zeilen, bearbeitet mit ffmpeg (Rezept in `config/variants.json` → `audio_recipe`), auf −22 LUFS normalisiert und um 9 dB angehoben, weil die dunkle Stimme sonst im Spielmix untergeht.

Alle Funk-Kontexte nutzen denselben bearbeiteten Satz; das originale Radio-Filter des Funks entfällt.

## Installation (eigene Spielinstallation, Windows, PowerShell)

Voraussetzungen: Python 3, ffmpeg (vollständiger Build mit Rubberband):

```powershell
winget install Gyan.FFmpeg
```
`winget` ist der Windows-Paketmanager, `install` installiert ein Paket, `Gyan.FFmpeg` ist der vollständige ffmpeg-Build von gyan.dev. Danach die Konsole neu öffnen.

Dann im Repo-Ordner:

```powershell
python -I tools/x4cat_extract.py "C:\Steam\steamapps\common\X4 Foundations\01.cat" build\orig "voice-l049/10201/normal/*"
```
`-I` startet Python isoliert (keine Umgebungsvariablen, keine Nutzerpakete). Das Skript liest den Katalogindex `01.cat` und die zugehörige `01.dat`, zieht alle Dateien mit dem Präfix `voice-l049/10201/normal/` (Boso Tas deutsche Zeilen) heraus und legt sie unter `build\orig` ab. Liegen Zeilen auch in `02.cat` bis `09.cat`, den Befehl dafür wiederholen; spätere Kataloge überschreiben frühere.

```powershell
python -I tools/process_audio.py --variant d12_alien_mid --gain-db 9 --src build\orig\voice-l049\10201\normal --dst build\audio\d12_alien_mid_g9
```
`--variant` wählt die Filterkette (`--list` zeigt alle), `--gain-db 9` hebt nach der Normalisierung um 9 dB an (mit Begrenzer), `--src` ist der Ordner mit den Originalen, `--dst` der Zielordner, den `config/variants.json` erwartet. Dauer etwa 10 Minuten auf 8 Kernen.

```powershell
python -I tools/build_mod.py; python -I tools/validate_mod.py; python -I tools/install_mod.py alien
```
`build_mod.py` erzeugt `dist/` aus der Konfiguration. `validate_mod.py` entpackt die echte `sound_library.xml` aus dem Spiel und prüft jeden Selektor. `install_mod.py alien` entfernt alle `bosota_*`-Ordner im Spiel und kopiert XML plus Audio neu. `;` trennt die Befehle. Anderer Spielordner: `--game-dir "<Pfad>"` oder Umgebungsvariable `X4_GAME_DIR`.

Im Spiel: Hauptmenü → Erweiterungen → „Boso Ta – Alien-Stimme (deutsche Audiospur)" aktiv.

**Deinstallation:** `python -I tools/install_mod.py --remove` oder den Ordner `extensions\bosota_voice_alien` löschen.

## Varianten

| Schlüssel | Art | Beschreibung |
|---|---|---|
| `alien` | Audio-Umleitung | **Empfohlen.** Beschrieben oben. |
| `de`, `en` | nur Engine-Effekte | Pitch per Resampling (Stimme wird langsamer) plus Tiefpass. Kein Audio nötig, aber für den Autor nicht ausreichend. |

Eine englische Audio-Variante gibt es nicht; das Rezept ist identisch, nur mit `voice-l044/10201/normal/*` als Quelle und einem eigenen Varianteneintrag.

## Eigene Abstimmung

`tools/process_audio.py --list` zeigt alle Filterketten (tief, Computer, Ringmodulation, Doppelstimme, Alien, Flüstern, Unterwasser, Mitten-Fokus, Oktavstufen). Für Hörproben `--files <zeilen-id,...> --wav` verwenden; `tools/pitch_flatten.py` (Praat, eigene Umgebung unter `build/venv`) staucht vorab die Intonationsspitzen. Pegel nur im Spiel beurteilen: Eine dunkle Stimme klingt am PC gleich laut und geht im Spielmix trotzdem unter.

## Fehlersuche

- Mod fehlt in der Erweiterungsliste → `content.xml` ungültig; der Validator fängt das ab.
- Mod aktiv, Boso unverändert → X4 mit `-logfile debuglog.txt` starten und mit `Select-String -Path "<Nutzerordner>\debuglog.txt" -Pattern "No matching node","bosota"` prüfen. Nutzerordner: `Dokumente\Egosoft\X4\<ID>\`.
- Boso stumm → Audio fehlt im Spielordner (`voice\10201\normal\` muss 2 324 Dateien enthalten); `install_mod.py alien` erneut ausführen.

Herleitung: `docs/X4_Boso_Ta_Voice_Mod_Handoff.md`; am Spiel verifizierte Fakten: `docs/phase0-befund.md`; Erkenntnisse: `docs/dev-team/LESSONS.md`.
