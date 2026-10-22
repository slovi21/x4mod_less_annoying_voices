# Boso Ta – wärmere Stimme (X4: Foundations)

Kleine Mod für **X4: Foundations 9.00**, die die Stimme des Boronen-Beraters **Boso Ta** tiefer und wärmer klingen lässt. Sie ändert **keine Audiodateien**, sondern hängt per XML-Diff Engine-Effekte (Pitch, Tiefpass) an seine Sound-Einträge in `libraries/sound_library.xml`. Keine Egosoft-Assets enthalten, Deinstallation = Ordner löschen, Spielstände werden nicht als modifiziert markiert (`save="0"`).

> **Hinweis zum Umfang:** Boso Ta spricht mit dem Stimm-Set **10201** („Boron NPC 1"). Dieses Set teilen sich auch der Boronen-Fraktionsvertreter und einige Nebenfiguren – sie klingen mit dieser Mod ebenfalls tiefer.

## Varianten (immer nur **eine** installieren)

| Ordner | Für | Pitch | Tiefpass |
|---|---|---|---|
| `dist/bosota_warm_de` | deutsche Sprachspur – stark | 0.841 (−3 Halbtöne) | 0.25 |
| `dist/bosota_warm_en` | englische Sprachspur – mittel | 0.891 (−2 Halbtöne) | 0.35 |
| `dist/bosota_warm_test` | Schnelltest: DE-Werte zusätzlich auf Bordcomputer Betty, sofort beim Spielstart hörbar | 0.841 | 0.25 |

Die Pitch-Absenkung ist ein Resampling: Die Stimme wird im gleichen Maß langsamer (−3 Halbtöne ≈ 19 %). Das ist die einzige Form von Tonhöhenänderung, die die Engine im XML anbietet.

## Installation

**Von Hand:** Den gewünschten Ordner aus `dist/` nach `<X4-Spielordner>\extensions\` kopieren, z. B. `C:\Steam\steamapps\common\X4 Foundations\extensions\bosota_warm_de\`. Im Spiel unter *Hauptmenü → Erweiterungen* prüfen, dass der Eintrag erscheint und aktiv ist.

**Per Skript** (Python 3, im Repo-Ordner):

```bash
python -I tools/install_mod.py de
```
`python -I` startet Python im isolierten Modus (keine Umgebungsvariablen, keine Nutzer-Site-Pakete); `tools/install_mod.py` ist das Installationsskript; `de` wählt die Variante (`en`, `test` ebenso). Das Skript entfernt vorher alle `bosota_warm_*`-Ordner im Spiel und kopiert dann genau eine Variante. Anderer Spielordner: `--game-dir "<Pfad>"` anhängen oder Umgebungsvariable `X4_GAME_DIR` setzen.

**Deinstallation:** Ordner löschen oder `python -I tools/install_mod.py --remove` (`--remove` = nur entfernen, nichts installieren).

## Selbst abstimmen

1. Werte in `config/variants.json` ändern (`pitch`, `lowpass`, optional `reverb`).
2. Bauen und prüfen:
   ```bash
   python -I tools/build_mod.py && python -I tools/validate_mod.py
   ```
   `build_mod.py` schreibt die Varianten nach `dist/`; `&&` führt den zweiten Befehl nur aus, wenn der erste fehlerfrei war; `validate_mod.py` entpackt die echte `sound_library.xml` aus dem Spiel nach `build/` und prüft, ob jeder XPath-Selektor genau einen Eintrag trifft und keine doppelten Elemente entstehen.
3. Installieren (siehe oben) und im Spiel hören. Nur einen Parameter pro Durchlauf ändern.

## Fehlersuche

- Mod erscheint nicht in der Erweiterungsliste → `content.xml` ungültig (meist ein rohes `&`). Der Validator fängt das ab.
- Mod aktiv, aber keine Wirkung → X4 mit `-logfile debuglog.txt -debug all` starten (Steam: Startoptionen) und im Log nach `No matching node` suchen. Log liegt im Egosoft-Nutzerordner unter `Dokumente\Egosoft\X4\<ID>\`.
- Konflikte: andere Mods, die `sound_library.xml` patchen (Sound-Overhauls), können dieselben IDs berühren. Es gewinnt der zuletzt geladene Patch.

## Werkzeuge

| Datei | Zweck |
|---|---|
| `tools/x4cat_extract.py` | Dateien aus `.cat/.dat` holen – `.cat` ist ein Textindex, `.dat` die Rohdaten aneinandergehängt |
| `tools/build_mod.py` | Varianten aus `config/variants.json` erzeugen |
| `tools/validate_mod.py` | Diff gegen die Spieldatei prüfen, ohne das Spiel zu starten |
| `tools/install_mod.py` | Eine Variante ins Spiel kopieren / entfernen |

Recherche und Herleitung: `docs/X4_Boso_Ta_Voice_Mod_Handoff.md`; am Spiel verifizierte Fakten: `docs/phase0-befund.md`.
