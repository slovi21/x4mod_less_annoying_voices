# Phase 0 – Befund (Verifikation am Spiel)

**Stand:** 2026-10-22 · **Spiel:** X4 Foundations 9.00 (`version.dat` = 900), UI-Sprache 49 = Deutsch (`lang.dat`)
**Spielordner:** `C:\Steam\steamapps\common\X4 Foundations` · **Nutzerordner:** `C:\Users\slovi\OneDrive\Documents\Egosoft\X4\34818113`

Alle Aussagen hier sind an den echten Spieldateien geprüft (Kataloge 01–09 und `extensions/ego_dlc_*/ext_0*.cat`). Extrahiert wurde mit `tools/x4cat_extract.py`; alle MD5-Prüfsummen stimmten.

## 1. Boso Tas Sprach-Page: **10201**

Titel in `t/0001-l044.xml`: `Boron NPC 1 / Boron rep / Misc Plot Characters`.

Beleg: Die Missionsskripte sprechen Boso Ta mit `$actor = '$BosoTa', $speak = <ID>` an. Drei dieser IDs wurden im Katalogindex gesucht; alle liegen unter Page 10201:

| speak-ID | Quelle (MD-Skript) | Gefunden unter |
|---|---|---|
| 302360401 | `md/crisis_xenon_khaak_combo.xml`, `md/cpu_ship_manager.xml` | `voice-l044/10201/{comm,comm_broadcast,comm_npc}/302360401.ogg` |
| 302360101 | `md/crisis_xenon_khaak_combo.xml` | `voice-l044/10201/…/302360101.ogg` |
| 30253525 | `md/story_boron.xml` (Kingdom End) | `voice-l044/10201/…/30253525.ogg` |

Zusätzlich: Boso Tas Charakter-Makro heißt `character_boron_hq_mentor_macro` (`md/story_boron.xml`, Zeile 2048).

**Wer spricht mit Set 10201?** Praktisch nur Boso Ta. Zusammensetzung (EN, Kontext `normal`): 1 681 Plot-Zeilen (Präfixe 30253, 30201, 30222, 30251, 30236 … = HQ-Plot, Boron-Plot, Forschung) und nur **71 generische NPC-Sätze**; die echten Zufalls-Stimmsets 10202/10204/10205 haben je 488 generische Sätze. Ein zufälliger Boronen-NPC mit Set 10201 wäre also bei 434 Standardsätzen stumm – die Engine vergibt es nicht zufällig. Explizit zugewiesen ist 10201 außer Boso Ta nur dem **Boronen-Fraktionsvertreter** (`extensions/ego_dlc_boron/libraries/characters.xml`, Zeile 55, `factionrepresentative_boron`), derselbe Sprecher. Zuweisung bei Boso Ta: `<page exact="10201"/>` in `create_cue_actor` (`md/x4ep1_mentor_subscription.xml` Z. 117 und 876, `md/story_boron.xml` Z. 2049, `md/scenario_advanced.xml` Z. 32); das NPC-Makro `character_boron_hq_mentor_macro` selbst hat keine Page. Die Page ist **im Spielstand gespeichert** (`<component class="npc" macro="character_boron_hq_mentor_macro" … page="10201">`), eine MD-Aktion zum Umsetzen gibt es laut `md.xsd` nicht.

## 2. Sound-IDs für Page 10201 (Basis `08.cat`, Zeilen 12079–12110)

| Sound-ID | Sample-Pfad | Bestehende `<volume>` | Bestehende `<effects>` |
|---|---|---|---|
| `10201_normal` | `voice\10201\normal` | start 1.212, distance 0.090 | **keine** |
| `10201_normal_npc` | `voice\10201\normal` | start 1.0, distance 0.075 | keine |
| `10201_comm` | `voice\10201\comm` | – | keine |
| `10201_comm_signalleak` | `voice\10201\comm` | start 1, distance 0.20 + distancecurve | keine |
| `10201_comm_npc` | `voice\10201\comm_npc` | start 0.9 | keine |
| `10201_comm_broadcast` | `voice\10201\comm_broadcast` | – | keine |

Folgerung: Der störende Klang kommt **allein aus den Audiodateien**, kein Engine-Effekt verstärkt ihn. Die Mod muss `<effects>` jeweils **neu anlegen** (`<add sel=".../sound[@id=…]">`), nicht ersetzen.

**Kein DLC patcht diese IDs.** Alle sieben `extensions/ego_dlc_*/ext_03.cat` enthalten eine `libraries/sound_library.xml` als `<diff>`; keine berührt `10201_`. → **Keine Abhängigkeit auf `ego_dlc_boron` nötig.**

## 3. Wo die Audiodateien liegen

- Ausschließlich in den **Basis-Katalogen 01–09**. Der Boron-DLC enthält **keine** `voice-l0xx/`-Dateien.
- Umfang Page 10201: Englisch (l044) 1 752 Zeilen, Deutsch (l049) 2 326 Zeilen – je Kontext `normal`, `comm`, `comm_npc`, `comm_broadcast` eine eigene Datei, dazu `lipsync/*.xpm`.
- Dateinamen = speak-ID (z. B. `302360401.ogg`), nicht die Zeilennummer innerhalb der Page.

## 4. Effekt-Schema der Engine (`libraries/sound_library.xsd`, `08.cat`)

`<effects>` ist `xs:all` (jedes Kind höchstens einmal, Reihenfolge egal):

| Element | Attribute | Anmerkung |
|---|---|---|
| `doppler` | `factor` | – |
| `fade` | `in`, `out` | Sekunden |
| `filter` | `mode` = lowpass / bandpass / highpass / notch; `frequency` [0, 1]; `oneoverq` [0, 1.5]; `distance` | Spiel nutzt `lowpass frequency` 0.05–0.5 für gedämpfte Sounds |
| `reverb` | `room` (Preset), `roomsize` [1, 100] ft, `drymix` [0, 100] %, `density` [0, 100] % | Presets u. a. `padded cell`, `carpeted hallway`, `sewer pipe`, `underwater` |
| `pitch` | `start`, `end`, `steps` | Beispiel im Spiel: `<pitch start="0.8" end="1.0" steps="1"/>` |

**Nicht vorhanden:** Equalizer, Pitch-Shifter in Halbtönen, Kompressor.

`pitch` ist mit hoher Wahrscheinlichkeit ein **Resampling-Faktor** (OpenAL `AL_PITCH`): 0.891 = −2 Halbtöne und 12 % langsamer, 0.841 = −3 Halbtöne und 19 % langsamer. Die Semantik von `start`/`end`/`steps` (vermutlich Zufallswert zwischen start und end in `steps` Stufen) ist nicht dokumentiert → wir setzen `start = end`.

Die Skala von `filter frequency` (0..1) ist nicht dokumentiert; vermutlich normiert auf die halbe Abtastrate (0.25 ≈ 5,5 kHz). **Nur per Gehör bestimmbar.**

### Entscheidungsmatrix angewendet

Befund = „Nur Resampling-Pitch + Lowpass/Reverb" → **Plan A eingeschränkt**: EN −2 Halbtöne, DE −3 Halbtöne (Obergrenze wegen Tempoverlust), Wärme über Lowpass. Lipsync verschiebt sich um den Tempofaktor.

## 5. Diff- und content.xml-Syntax (verifiziert)

- `libraries/diff.xsd`: Wurzel `<diff>`, Operationen `<add sel="…" [pos="before|after|prepend"] [if="…"] [silent]>`, `<replace sel="…">`, `<remove sel="…"/>`; `sel` ist eingeschränktes XPath (`/soundlibrary/sound[@id='10201_normal']` ist gültig).
- `content.xml` (Vorbild `extensions/ego_dlc_boron/content.xml`): `<content id name description author version date enabled save>` mit Kindern `<text language="49" name="…" description="…"/>`.

## 6. Nutzerumgebung

- Extension-Tabelle heißt hier **`content-MSI-PRODP20Z.xml`** (rechnerspezifisch, X4 9.00), nicht `content.xml`. Alle 19 Workshop-Einträge stehen auf `enabled="false"`. Kein `extensions/`-Ordner im Nutzerverzeichnis → Mods gehören nach `<Spielordner>\extensions\`.
- Spielstände vorhanden: `save_001`, `save_002`, zwei Autosaves.

## 7. Offene Punkte für den Spieltest (Phase 3)

- [ ] Wirkt `<pitch>` überhaupt auf Sprach-Sounds (Betty-Test)?
- [ ] Bedeutung von `steps`; klingt `start=end` stabil?
- [ ] Hörbare Wirkung der `lowpass`-Skala: 0.25 / 0.35 zu dumpf oder zu schwach?
- [ ] Tempoverlust bei −3 Halbtönen akzeptabel? Sonst 0.891 (−2) oder 0.87.
- [ ] Wirkt `<effects>` auch auf `comm`-Fenster (alle IDs sind `is3d="1"`, also vermutlich ja).
