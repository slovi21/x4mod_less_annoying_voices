# X4 Boron Voice Mod – Boso Ta: Recherche und Umsetzungsplan

**Stand:** 2026-10-22
**Zweck:** Vollständiges Handoff aus den Claude-Chat-Sitzungen vom 21./22.10.2026 für die Weiterarbeit in Claude Code. Alles, was recherchiert, entschieden und offen ist, steht hier. Nichts davon ist bisher im Spiel getestet.

**Arbeitsumgebung:** Windows 11, Git Bash. Shell-Befehle sind in diesem Dokument immer mit Erklärung jeder Option versehen – das ist eine feste Vorgabe für alle weiteren Sitzungen. Repos liegen üblicherweise unter `C:\Users\slovi\OneDrive\Documents\#repos\github`.

**Kennzeichnung:** Aussagen ohne Quellenhinweis stammen aus Trainingswissen und sind mit *(TW)* markiert. Mit *(Q)* markierte Aussagen stammen aus den in Abschnitt 11 gelisteten Quellen. Nichts ist bisher selbst verifiziert.

---

## 1. Ziel und Anforderungen

### 1.1 Problem
Die Stimme des Boronen-Beraters **Boso Ta** in X4: Foundations wird als extrem hoch, nervig und unpassend empfunden – auf Deutsch wie auf Englisch. Sie zerstört die Stimmung.

### 1.2 Gewünschtes Ergebnis (Iteration 1 – Auftrag vom 21.10.2026)
Alle Audioausgaben von Boso Ta **tiefer und wärmer** klingen lassen, **ohne die Audiodaten selbst zu ändern** – also rein über Engine-Effekte (`sound_library.xml`).

| Sprache | Anpassung Stimmtiefe und Wärme |
|---|---|
| Englisch (`voice-l044`) | mittel |
| Deutsch (`voice-l049`) | stark |

### 1.3 Spätere Optionen (aus der ersten Recherche)
- Audio-Batch-Filter (Pitch/EQ über ffmpeg) mit Audio-Redirect
- KI-Voice-Conversion (Speech-to-Speech, Timing bleibt erhalten) – fachlich der beste Weg, falls der reine Filter nicht reicht
- Komplett neue Sprachspur per TTS – nicht empfohlen (Lipsync/Timing)

### 1.4 Zwei Korrekturen an der Aufgabenstellung (bereits mit Slovi besprochen)
1. **"EN mittel / DE stark" ist in einer einzigen Mod nicht abbildbar.** `sound_library.xml` ist sprachunabhängig; dieselbe Sound-ID bedient `voice-l044` und `voice-l049`. Lösung: ein Quellprojekt, zwei generierte Extension-Varianten (`bosota_warm_en`, `bosota_warm_de`); es wird genau eine installiert.
2. **"Tiefer" hat zwei technische Bedeutungen:** echter Pitch-Shift (Tempo bleibt) oder Resampling (Stimme wird langsamer). Bei "stark" (ca. −4 Halbtöne) wäre Resampling ~26 % langsamer – Zeitlupeneffekt. Welche Variante die Engine im XML anbietet, klärt Phase 0 des Plans.

---

## 2. Recherche-Erkenntnisse (Faktenbasis)

### 2.1 Archivformat `.cat` / `.dat` (Q: tridkx/x4-voice-mod, X4 9.00)
- `.cat` ist ein **reiner Textindex**, kein Binärformat. Zeilenformat:
  `assets/characters/animations/2.xsm 111354 1208774952 380e1d7ea9d0e38fa17e7e708a01ef28`
  → relativer Pfad, Größe in Bytes, mtime, MD5 des Inhalts.
- `.dat` enthält alle Dateien **in Reihenfolge des Index, lückenlos aneinandergehängt**, ohne Ausrichtung, ohne Kompression. `offset(i) = Summe der Größen 0..i-1`.
- Konsequenz: Man braucht kein XRCatTool; ein kleines Python-Skript (`tools/x4cat.py` im Referenzprojekt) kann list/extract/pack.
- Basis-Kataloge: `01.cat` … `09.cat` im Spielverzeichnis, höhere Nummer überschreibt niedrigere. DLCs/Mods: `extensions/<name>/ext_01.cat` (Überlagerung) bzw. `subst_01.cat` (Ersatz). Alle Pfade sind relativ zur X4.exe; Katalog-Inhalte werden virtuell ins Root gemountet.
- X4.exe scannt `*.cat` und mountet sie einzeln (`CatalogList::AddNewCatalog()`); fehlende `_sig.cat` erzeugt nur eine **Warnung** (`Loading %s %s.cat without a corresponding signature catalog`), keine Ablehnung.
- Signaturdateien (`_sig.cat`) werden von Entpackern ignoriert; Null-Byte-Löscheinträge übersprungen (Q: X4unpacker).

### 2.2 Sprachdateien (Q: tridkx/x4-voice-mod; h2odragon HOWTO)
Pfadschema:
```
voice-l<Sprache>/<page>/<context>/<line>.ogg      ← Audio
voice-l<Sprache>/<page>/lipsync/<line>.xpm        ← Mundbewegungsdaten (EMotion FX)
```

| Feld | Bedeutung | Beispiel |
|---|---|---|
| `l044` / `l049` | Sprachsuffix: **44 = Englisch, 49 = Deutsch**. Nur diese zwei Sprachspuren existieren. Die Engine baut das Suffix zur Laufzeit per `-l%03d` | – |
| `page` | Sprecher bzw. Stimm-Set einer Figur; entspricht `<page id>` in `t/0001-l0XX.xml` | `10002` = Ship Computer – Betty |
| `context` | Abspielanlass: `normal`, `comm`, `comm_npc`, `comm_broadcast`, `station_broadcast` | – |
| `line` | Zeilen-ID, entspricht `<t id>` in der t-Datei | `11201` |

Audioformat: **Ogg Vorbis, Mono, 44 100 Hz, ca. 48 kbps.**
Umfang gesamt: **229 Sprecher-Pages, 37 203 eindeutige Zeilen, 144 499 englische .ogg-Dateien.** Eine komplette Page-Liste liegt im Referenzprojekt unter `docs/voice_pages.csv` (siehe 4.1 – dort Boso Tas Page-ID nachschlagen).

Wichtig: Unter einer Page existieren Verzeichnisse (`comm_npc`, `comm_broadcast`), die in `sound_library.xml` **nicht referenziert** werden. Dieselbe Zeile liegt pro Kontext als eigene Audio-Version (unterschiedliche MD5). Maßgeblich dafür, was geladen wird, ist allein `<sample start>` in der Sound-Library.

Weitere Engine-Fakten:
- X4.exe enthält die Startparameter-Strings `prefersinglefiles` und `voicelanguage`.
- `lang.dat` hält die UI-Sprache (Zahl), `version.dat` die Spielversion (z. B. 900 = 9.00).
- Eine neue Sprachspur (z. B. `voice-l081` + `-voicelanguage 81`) ist möglich, muss aber **komplett** geliefert werden – fehlende Zeilen sind stumm, kein Fallback auf Englisch.

### 2.3 `sound_library.xml` – so findet die Engine das Audio (Q: tridkx)
Datei: `libraries/sound_library.xml`, liegt in `08.cat`. Pro Sprechanlass ein Eintrag:
```xml
<sound id="10002_normal" description="Board computer - Betty" repeat="1" is3d="1" preload="0">
  <sample start="voice\10002\normal"/>   <!-- nur Verzeichnis, kein Dateiname -->
  <effects><reverb room="sewer pipe" .../></effects>
</sound>
```
Abspielvorgang bei `<speak page="10002" line="1" context="normal"/>`:
1. Sound-ID `<page>_<context>` → `10002_normal`
2. `sample start` lesen → `voice\10002\normal`
3. Sprachsuffix anhängen (`voice` → `voice-l044`), Zeile und `.ogg` anhängen
4. Ergebnis: `voice-l044/10002/normal/1.ogg`

Beleg, dass das XML den Pfad bestimmt: `20005_normal` und `20005_comm` zeigen **beide** auf `voice\20005\normal`.
Effekte (`<effects>`) hängen **pro Sound-ID** – das ist der Hebel für Iteration 1.
Welche Effekt-Elemente außer `<reverb>` die Engine im XML akzeptiert, ist **nicht belegt** → Phase 0.

### 2.4 Audio-Backend (Q: Steam-Thread zu Soundproblemen; Rest TW)
- X4 nutzt **OpenAL**: Nutzer ersetzen bei Soundproblemen `openal32.dll` im Spielordner durch `soft_oal.dll` aus OpenAL Soft (Q).
- Der Reverb-Preset-Name `sewer pipe` ist ein Standard-EFX-Preset von OpenAL (`EFX_REVERB_PRESET_SEWERPIPE`) *(TW)*.
- OpenAL EFX kennt *(TW)*: Reverb/EAX-Reverb, Chorus, Distortion, Echo, Flanger, Frequency Shifter, Vocal Morpher, **Pitch Shifter** (tempoerhaltend, coarse −12…+12 Halbtöne, fine −50…+50 Cent), Ring Modulator, Autowah, Compressor, **Equalizer** (4 Bänder) sowie Filter: **Lowpass** (gain, gainhf 0…1), Highpass, Bandpass.
- EFX-Equalizer-Bereiche *(TW)*: Low-Gain 0,126–7,943 (≈ −18…+18 dB), Low-Cutoff 50–800 Hz; Mid1-Center 200–3000 Hz, Mid1-Width 0,01–1; Mid2-Center 1000–8000 Hz; High-Gain wie Low, High-Cutoff 4000–16000 Hz.
- Ob Egosoft diese Effekte im XML **exponiert**, ist offen (siehe 2.3).

### 2.5 Mod-Lademechanik (Q: tridkx, GameStar, Nexus-Kommentare, Egosoft-Forum)
- Mods liegen in `<X4-Ordner>\extensions\<modname>\` **oder** in `Dokumente\Egosoft\X4\<SteamID>\extensions\` (beides funktioniert, je nach System eines sicher).
- Im Hauptmenü unter "Erweiterungen" prüfen, ob die Mod aktiv ist.
- **Enable-Tabelle:** `Dokumente\Egosoft\X4\<id>\content.xml` enthält `<extension id="..." enabled="true"/>`. Nur erkannte Extensions mit `enabled="true"` werden geladen. Beim Debuggen "installiert, aber keine Wirkung" zuerst hier nachsehen.
- **Stille Verwerfung:** Ein unmaskiertes `&` in `content.xml` macht die Datei zu ungültigem XML; X4 verwirft die Extension dann **ohne Meldung**, sie taucht nicht einmal in der Erweiterungsliste auf. Alle Attributtexte XML-escapen (`&amp;`).
- Ladereihenfolge: ohne Abhängigkeit alphabetisch; mit `<dependency>` in `content.xml` wird die Reihenfolge erzwungen. Mods, die dieselben Sound-IDs anfassen, kollidieren.
- `id` in `content.xml` und Ordnername dürfen abweichen (häufig), nur Hinweis.
- Debug: X4 mit `-logfile debuglog.txt` (und `-debug all`) starten. Fehlschlagende Diff-Selektoren erzeugen "No matching node"-Fehler; die betroffenen Patches werden übersprungen (Q: Nexus-Kommentar "Drunken Sounds").
- Referenzprojekt-Hinweise aus dem Nexus-Kommentar: Audio-Pfade im XML ohne Dateiendung angeben; Sound-Einträge in das erwartete Wurzelelement einbetten.

### 2.6 Boso Ta – Annahmen (TW, zu verifizieren)
- Boso Ta ist seit dem Basisspiel vorhanden (Forscher am Spieler-Hauptquartier); Kingdom End (`extensions/ego_dlc_boron/`) ergänzt weitere Zeilen.
- Seine Audio-Dateien liegen daher vermutlich **teils in den Basis-Katalogen (01–09.cat), teils im DLC-Katalog**.
- Seine **Page-ID ist unbekannt** → in `t/0001-l044.xml` nach "Boso" suchen oder `docs/voice_pages.csv` des Referenzprojekts durchsuchen.
- Es ist nicht geklärt, ob der störende Klang teilweise durch einen Engine-Effekt (z. B. ein Reverb-Preset in seinen `<effects>`) entsteht. Falls ja, ist ein Teil des Problems ohne jede Audio-Arbeit lösbar.
- Das DLC patcht vermutlich eigene Einträge in `sound_library.xml` → unsere Mod muss **nach** `ego_dlc_boron` laden.

### 2.7 Präzedenzfälle
| Projekt | Was | Relevanz |
|---|---|---|
| **Split Voice Overhaul** (Nexus 598, C0331, Dez. 2020) | Split-Stimmen tiefer und rauer gefiltert ("mask questionable line readings"); Ordner `voice-l044` ins Spiel-Root, Startoption `-prefersinglefiles` zwingend | Beweis, dass Pitch-Filter-Mods im Spiel funktionieren; Beweis für Route C |
| **tridkx/x4-voice-mod** (GitHub, 2026, X4 9.00) | Chinesische TTS-Ansagen für Betty (page 10002, 504 Zeilen) und Stationsdurchsagen (page 10099, 73 Zeilen); komplette Toolchain; 557 Zeilen TTS in 40 s | Hauptquelle für Format, Mechanik, Route B; Tools wiederverwendbar |
| **Vectorial1024/v1024_poc_voicelines** (X4 5.0) | Community-PoC: Extension-Overlay für Audio wirkt nicht, Root + `-prefersinglefiles` nötig | Bestätigt Route C, widerlegt Route A |
| **starwarsmod_m1** | `subst_01.cat` überschreibt 13 Texturen, `ext_01.cat` 589 Basisdateien inkl. binärer `.xpl` | Zeigt: Extensions überschreiben Basisdateien – **außer Audio**, das eine eigene Dateisuche hat |
| Egosoft selbst | Mit Patch 7.5 wurde Reen (Hatikvah-Plot) mit neuer Stimme versehen (Steam-Diskussion, März 2026) | Egosoft tauscht Stimmen gelegentlich offiziell; Hoffnung, aber kein Plan |

---

## 3. Einbauwege (Q: tridkx, mit eigenen Ergänzungen)

| Route | Prinzip | Voraussetzung | Status |
|---|---|---|---|
| **A – Extension überschreibt Originalpfad** | Dateien unter `voice-l044/<page>/<context>/<line>.ogg` in `ext_01.cat` | – | ❌ **Widerlegt**: Extension geladen, Betty bleibt englisch |
| **B – Sample-Redirect (empfohlen für Audio-Austausch)** | XML-Diff auf `sound_library.xml`: `<sample start>` auf `extensions\<mod>\voice\<page>\<context>` umbiegen, eigene .ogg dort ablegen | XML-Diff + Dateien in der Extension | ✅ **Getestet, funktioniert.** Keine Startparameter, keine Originaldatei geändert, Deinstallation = Ordner löschen |
| **C – Root + Startparameter** | `voice-l044/...` lose ins Spielverzeichnis, Start mit `-prefersinglefiles` | Startparameter | ✅ Bewährt (Split Voice Overhaul). Unsauber: Root verschmutzt, Steam-Updates können überschreiben. Gut für Schnelltests |
| **D – Neuer Katalog** | `10.cat` + `10.dat` ins Root, lädt nach 09 | – | Ungetestet (nach Erfolg von B nicht mehr nötig) |
| **E – Basis-Katalog patchen** | Bytes in `03.dat` direkt ersetzen | – | Notlösung; In-Place nur bei exakt gleicher Dateigröße, sonst 6,1 GB neu schreiben; Skript `patch_base_archive.py` existiert |
| **F – Nur Effekte (Iteration 1)** | XML-Diff auf `<effects>` der Sound-IDs, Audio bleibt unberührt | XML-Diff | **Ungetestet; Gegenstand von Phase 0** |

Fallen (gelten für alle Routen): `&` in `content.xml` (2.5), Enable-Tabelle (2.5), Ladereihenfolge/Abhängigkeit auf `ego_dlc_boron`, "No matching node" bei falschen IDs.

---

## 4. Werkzeuge

### 4.1 Entpacken / Packen
- **X4unpacker** (Nexus 2142, GUI + CLI): berücksichtigt Patch-Überschreibungen und DLCs automatisch, Inhaltsauswahl pro DLC/Extension, `-f/--force` zum Überschreiben, `--threads N`. Beispiele (Q):
  ```
  X4unpackerCLI.exe folder "C:\...\X4 Foundations" ls "*.xml"
  X4unpackerCLI.exe file "C:\...\X4 Foundations\01.cat" x "*.lua" "C:\X4_Unpacked"
  X4unpackerCLI.exe all_folders "C:\...\X4 Foundations" x "*.xml" "C:\X4_Unpacked" --threads 8
  X4unpackerCLI.exe all_folders "C:\...\X4 Foundations" x "assets/units" "C:\X4_Unpacked"
  ```
  Erklärung: erstes Argument = Quelle (`folder` = Spielordner mit allen Basis-Katalogen, `file` = ein einzelner .cat, `all_folders` = Basis + alle DLCs/Extensions); dann der Pfad; `ls` listet nur, `x` extrahiert; dann ein Glob-Muster bzw. Pfadpräfix; dann das Zielverzeichnis. Für uns: `x "libraries/sound_library.xml"`, `x "t/0001-l044.xml"`, `x "voice-l044/<PAGE>"`.
- **XRCatTool** (Egosoft, offiziell, aus X Rebirth): ins X4-Root legen, Batch (Q):
  ```
  XRCatTool.exe -in 01.cat -in 02.cat ... -in 09.cat -out "<Zielordner>\unpacked"
  ```
  `-in` je Katalog (mehrfach), `-out` Zielordner.
- **tridkx/x4-voice-mod** – Python-Toolchain (Python 3 + ffmpeg):
  | Skript | Zweck |
  |---|---|
  | `tools/x4cat.py` | cat/dat: `info` / `list` / `extract` / `pack` |
  | `tools/voice_inventory.py` | Archive scannen, mit t-Dateien kreuzen → Zeilen-Inventar CSV |
  | `tools/voice_mod_builder.py` | Ersetzungsplan (JSON) → Batch-TTS → ogg → Extension + cat/dat |
  | `tools/check_extensions.py` | Extension-Check: content.xml gültig, cat/dat gepaart, Index-Summe = dat-Größe; `--ext <name> --deep` |
  | `tools/patch_base_archive.py` | Route E inkl. Rollback |
  | `tools/build_volc_mod.py` | TTS-Builder (chinesischer Anbieter, für uns irrelevant) |
  | `docs/voice_pages.csv` | **alle 229 Pages** – hier Boso Tas Page-ID finden |

  Repo holen und Page-ID suchen (Git Bash):
  ```bash
  git clone https://github.com/tridkx/x4-voice-mod
  grep -i boso x4-voice-mod/docs/voice_pages.csv
  ```
  `git clone <URL>` lädt das Repository in einen gleichnamigen Unterordner; `grep -i boso <Datei>` sucht zeilenweise nach "boso", `-i` ignoriert Groß-/Kleinschreibung.
- **X4 Customizer** (bvbohnen, GitHub/Egosoft-Forum): Python-Framework, schreibt Änderungen als Diff-Patches in eine Extension, kann cat packen/entpacken und Extensions auf Fehler prüfen – Alternative, wenn wir Diffs automatisiert erzeugen wollen.
- **X4FProjector** (bno1): Datenexport aus cat/dat, nicht audio-relevant.

### 4.2 Audio (nur für Plan B / spätere Iterationen)
- **ffmpeg** (Windows-Build mit `librubberband`, z. B. gyan.dev "full") für Pitch/EQ/Konvertierung.
- **SoX** als Alternative.
- Zielformat stets: Ogg Vorbis, Mono, 44 100 Hz, ~48 kbps (identisch mit Original).

### 4.3 KI-Stimme (nur für spätere Iterationen)
- **ElevenLabs Voice Changer** (früher Speech-to-Speech; API-Endpunkt heißt weiterhin `POST /v1/speech-to-speech/{voice_id}`): behält Emotion, Tempo, Intonation, Atmer und tauscht nur den Sprecher. Ziel: vorgefertigte Stimme, geklonte Stimme oder Library-Stimme. Output-Formate wie `mp3_44100_128`, `mp3_44100_64`; kein Low-Latency-"Flash"-Tier. SDKs: `elevenlabs` (Python), `@elevenlabs/elevenlabs-js`. Preise/Credits: **noch nicht geprüft.**
- **Eledubby** (PyPI): Batch-Tool auf ElevenLabs-Basis, erhält das Timing durch Auffüllen/Kürzen, parallele Segmente.
- **RVC / Applio** *(TW)*: lokale, kostenlose Voice Conversion mit eigener GPU, Batch-Modus; Qualität etwas unter ElevenLabs, kein Upload.
- **Nicht relevant:** HCS Voice Packs (Gamma, Astra, Alix) sind VoiceAttack-Sprachsteuerungen, keine NPC-Stimmen.

---

## 5. Optionen für die Stimme – Bewertung

| Option | Vorteile | Nachteile | Einordnung |
|---|---|---|---|
| **1. Engine-Effekte (Iteration 1)** | Keine Audio-Dateien, kleinste Mod, sofort umschaltbar, patchsicher | Abhängig vom exponierten XML-Schema; Resampling-Pitch macht langsamer; Sprechstil bleibt | **Jetzt umsetzen** |
| **2. Audio-Batch-Filter** (ffmpeg, Route B) | Volle Kontrolle (formant-erhaltender Pitch, EQ), kostenlos, Minuten | Audio-Dateien in der Mod (Größe, Grauzone); Sprechstil bleibt | Plan B, falls Option 1 nicht reicht |
| **3. Voice Conversion** (ElevenLabs/RVC, Route B) | Timing identisch → Lipsync und Dialoglängen intakt; keine Transkripte; eine Pipeline für DE und EN; echte andere Stimme | API-Kosten bzw. GPU; Grauzone bei Verteilung | Fachlich beste Lösung, wenn der Stil das Problem ist |
| **4. Neue TTS-Spur** | Technisch belegt (Referenzprojekt) | Dialogdauer und Lipsync (.xpm) passen nicht mehr; TTS-Dateien 9–22 % größer; pro Zeile angleichen | Nicht empfohlen |

Aufwandsschätzung (Q: tridkx): **ein Charakter = einige Hundert bis 2000 Zeilen → machbar.** Komplettvertonung = ~37 000 × 4 Kontexte ≈ 140 000 Dateien → nur mit Lipsync-Problemen.

---

## 6. Umsetzungsplan Iteration 1 – Engine-Filter ohne Audioänderung

### Phase 0 – Verifikation (Blocker für alles Weitere)
Ziel: Effekt-Schema der Engine ermitteln, Boso Tas Sound-IDs sammeln.

1. Entpacken: `libraries/sound_library.xml` aus `08.cat` **und** aus den Katalogen in `extensions/ego_dlc_boron/`; `t/0001-l044.xml`; optional `t/0001-l049.xml`.
2. Page-ID: `grep -i boso` auf `t/0001-l044.xml` oder `voice_pages.csv` (siehe 4.1).
3. Alle Sound-IDs mit dieser Page sammeln (Basis + DLC-Diff): `<page>_normal`, `<page>_comm`, ggf. weitere. Nur IDs verwenden, die wirklich existieren, sonst "No matching node".
4. Effekt-Inventar:
   ```bash
   grep -oE '<(reverb|pitch|pitchshift|pitchshifter|equalizer|eq|lowpass|highpass|filter|distortion|chorus|echo|compressor|frequencyshifter)[^>]*>' sound_library.xml | sort | uniq -c | sort -rn | head -40
   ```
   `grep` sucht Muster; `-o` gibt nur den Treffer aus; `-E` erlaubt erweiterte reguläre Ausdrücke (`|` = oder, Klammergruppe); das Muster fängt öffnende Tags mit einem der Namen samt Attributen bis `>`; `sort` sortiert; `uniq -c` fasst gleiche Zeilen zusammen und zählt; `sort -rn` sortiert numerisch absteigend; `head -40` zeigt die 40 häufigsten. Ergebnis = inoffizielles Effekt-Schema.
5. Ebenso die Attribute von `<sound>` und `<sample>` sichten (z. B. `pitch`, `pitchmin`/`pitchmax`, `volume`, `gain`), damit auch der Resampling-Weg erkannt wird:
   ```bash
   grep -oE '<sound [^>]*>' sound_library.xml | grep -oE ' [a-z0-9_]+=' | sort | uniq -c | sort -rn
   ```
   Erster `grep` holt alle `<sound ...>`-Tags; zweiter `grep -oE ' [a-z0-9_]+='` extrahiert daraus nur die Attributnamen (Leerzeichen, Name, Gleichheitszeichen); Rest wie oben.
6. Boso Tas vorhandene `<effects>` ansehen: Reverb-Preset? Etwas, das "gurgelig/metallisch" erzeugt?

**Entscheidungsmatrix:**

| Befund in Phase 0 | Konsequenz |
|---|---|
| Pitch-Shifter (Halbtöne) **und** EQ/Lowpass vorhanden | Plan A rein: Timing und Lipsync bleiben exakt |
| Nur Resampling-Pitch + Lowpass/Reverb | Plan A eingeschränkt: EN −1 bis −2 Halbtöne; DE max. −3 (Tempoverlust); Wärme über Lowpass/Reverb-Dämpfung |
| Nur Reverb | Nur "wärmer" möglich (dumpferes Preset), nicht "tiefer" → Vorgabe "ohne Audioänderung" nicht erfüllbar → Plan B (Abschnitt 7) |

### Phase 1 – Mod-Gerüst (unabhängig vom Befund baubar)
```
bosota_warm_<lang>/
  content.xml                      ← id, name, version, Abhängigkeit auf ego_dlc_boron
  libraries/sound_library.xml      ← XML-Diff, kein Vollersatz
```
`content.xml` *(TW, Egosoft-Syntax)*:
```xml
<?xml version="1.0" encoding="utf-8"?>
<content id="bosota_warm_en" name="Boso Ta Warm Voice (EN)" description="Deeper, warmer Boso Ta via engine effects" author="Slovi" version="100" date="2026-10-22" save="0">
  <text language="44" name="Boso Ta Warm Voice (EN)" description="Deeper, warmer Boso Ta via engine effects"/>
  <text language="49" name="Boso Ta – wärmere Stimme (EN)" description="Tiefere, wärmere Stimme per Engine-Effekt"/>
  <dependency id="ego_dlc_boron" optional="true"/>
</content>
```
Alle Attribute XML-sicher (`&amp;` statt `&`). `save="0"` = Spielstand wird nicht als modifiziert markiert *(TW, zu prüfen)*.

Diff-Gerüst *(TW, XPath-basiert)*:
```xml
<?xml version="1.0" encoding="utf-8"?>
<diff>
  <replace sel="//sound[@id='<PAGE>_normal']/effects">
    <effects>
      <!-- Effektkette aus Phase 2 -->
    </effects>
  </replace>
  <!-- je ein Block pro existierender Kontext-ID -->
  <!-- hat ein Eintrag noch kein <effects>: <add sel="//sound[@id='<PAGE>_comm']"><effects>...</effects></add> -->
</diff>
```

### Phase 2 – Effektparameter (Startwerte, nach Gehör nachjustieren)
Attributnamen folgen aus Phase 0; Werte orientieren sich an den EFX-Bereichen (2.4).

| Parameter | EN (mittel) | DE (stark) |
|---|---|---|
| Pitch | −2 Halbtöne (Faktor 0,891) | −4 Halbtöne (0,794); bei Resampling max. −3 (0,841) |
| EQ Tiefen (Low Shelf ~250 Hz) | +3 dB | +5 dB |
| EQ Tiefmitten (200–400 Hz, Wärme) | +2 dB | +3 dB |
| EQ Höhen (High Shelf ~4 kHz) | −4 dB | −7 dB |
| Alternative ohne EQ: Lowpass `gainhf` | 0,6 | 0,4 |
| Reverb | bestehendes Preset prüfen; falls metallisch/gurgelnd: gedämpfteres Preset (z. B. `carpeted hallway`, `padded cell`) oder entfernen | dito |
| Gain-Ausgleich | +1 dB | +2 dB |

Halbton-Faktoren: −1 = 0,944 · −2 = 0,891 · −3 = 0,841 · −4 = 0,794 (Formel 2^(n/12)).
Reihenfolge: erst Pitch, dann EQ – sonst verschiebt der Pitch die EQ-Frequenzen mit.

### Phase 3 – Test und Tuning
1. **Schnelltest-Trick:** Effektkette zuerst auf Bettys `10002_normal` legen – Betty spricht beim ersten Spielstart sofort, Boso Ta erst am HQ. Syntax und Hörbarkeit in 60 Sekunden prüfbar; danach Selektoren auf Boso Tas IDs umstellen.
2. Savegame direkt am Spieler-HQ anlegen (Gespräch mit Boso Ta jederzeit auslösbar).
3. Start mit `-logfile debuglog.txt -debug all`; Log auf "No matching node" und XML-Fehler prüfen.
4. Hörprotokoll: Verständlichkeit, Zischlaute (leiden unter Höhenabsenkung), Dialoglänge vs. Mundbewegung, Comm-Fenster vs. Gespräch vor Ort.
5. Iterieren in 1-dB- bzw. 1-Halbton-Schritten, nur ein Parameter pro Durchlauf.

### Phase 4 – Paketierung
- Build-Skript (Bash oder Python) erzeugt aus einer Parameterdatei beide Varianten (`_en`, `_de`).
- Lose Dateien reichen (Diff-XML funktioniert lose); optional als `ext_01.cat/dat` packen (`x4cat.py pack` oder X4 Customizer).
- README: nur eine Variante installieren; Ladereihenfolge; Deinstallation = Ordner löschen; Konfliktliste (Sound-Overhauls wie zsounds, Deep Thrust/Deep Impact patchen ebenfalls `sound_library.xml`).
- `check_extensions.py --ext bosota_warm_en --deep` als Abschlussprüfung.

---

## 7. Plan B – Audio-Redirect (Route B), falls Phase 0 nicht trägt

### 7.1 Variante Filter (ffmpeg)
1. Boso Tas Audio extrahieren: `voice-l044/<PAGE>/` und `voice-l049/<PAGE>/` (nur die Kontexte, die `sound_library.xml` referenziert).
2. Batch-Filter je Datei, formant-erhaltend *(TW)*:
   ```bash
   ffmpeg -i in.ogg -af "rubberband=pitch=0.891:formant=preserved,lowshelf=f=250:g=3,highshelf=f=4000:g=-4" -ac 1 -ar 44100 -c:a libvorbis -b:a 48k out.ogg
   ```
   `-i in.ogg` Eingabedatei; `-af "..."` Audio-Filterkette, Filter durch Komma getrennt: `rubberband=pitch=0.891` senkt die Tonhöhe um 2 Halbtöne bei gleichem Tempo, `formant=preserved` hält die Formanten (kein "Riesen"-Effekt); `lowshelf=f=250:g=3` hebt alles unter 250 Hz um 3 dB; `highshelf=f=4000:g=-4` senkt alles über 4 kHz um 4 dB; `-ac 1` Mono; `-ar 44100` Abtastrate; `-c:a libvorbis` Vorbis-Encoder; `-b:a 48k` Bitrate; `out.ogg` Ausgabe.
   Vorab prüfen, ob der Build Rubberband enthält: `ffmpeg -filters | grep rubberband` (`-filters` listet alle Filter, `grep` filtert die Zeile heraus).
   Ohne Rubberband *(TW)*: `asetrate=44100*0.891,aresample=44100,atempo=1.1224` – ändert aber die Formanten (dunkler/"größer"); `asetrate` deklariert eine niedrigere Abtastrate (tiefer und langsamer), `aresample` rechnet auf 44 100 Hz zurück, `atempo` beschleunigt um 1/0,891 wieder auf Originaltempo.
3. Loop über alle Dateien (Git Bash):
   ```bash
   find voice-l044/<PAGE> -name '*.ogg' | while read -r f; do out="out/$f"; mkdir -p "$(dirname "$out")"; ffmpeg -loglevel error -i "$f" -af "..." -ac 1 -ar 44100 -c:a libvorbis -b:a 48k "$out"; done
   ```
   `find <Ordner> -name '*.ogg'` listet rekursiv alle .ogg; `| while read -r f` liest zeilenweise in die Variable `f` (`-r` lässt Backslashes unverändert); `out="out/$f"` setzt den Zielpfad; `mkdir -p "$(dirname "$out")"` legt das Zielverzeichnis an (`-p` ohne Fehler, falls vorhanden; `dirname` schneidet den Dateinamen ab); `ffmpeg -loglevel error` unterdrückt alles außer Fehlern; `done` schließt die Schleife.
4. Dateien in `extensions/bosota_warm_<lang>/voice/<PAGE>/<context>/` ablegen; Diff auf `sound_library.xml`:
   ```xml
   <replace sel="//sound[@id='<PAGE>_normal']/sample/@start">extensions\bosota_warm_en\voice\<PAGE>\normal</replace>
   ```
   Beleg aus dem Referenzprojekt: dort wurde `10002_normal` auf `extensions\x4_my_voice\voice\10002\normal` umgebogen – funktioniert.
5. Sprachsuffix beachten: Die Engine hängt vermutlich auch beim Redirect `-l044`/`-l049` an das erste Pfadsegment an (`voice` → `voice-l044`). Im Referenzprojekt hieß das Ziel `voice\...` innerhalb der Extension – zu prüfen, ob der Ordner in der Extension `voice` oder `voice-l044` heißen muss. **Offener Punkt, in Phase 0 von Plan B testen.**

### 7.2 Variante Voice Conversion
Wie 7.1, nur Schritt 2 ersetzt durch ElevenLabs Voice Changer (Eledubby-Batch oder eigenes Skript) bzw. RVC/Applio lokal. Danach ffmpeg-Konvertierung ins Zielformat (Mono, 44 100 Hz, Vorbis ~48 kbps). Ersetzungsplan-Beispiel aus dem Referenzprojekt (JSON):
```json
{
  "id": "x4_my_voice",
  "langs": ["l044"],
  "sound_library_redirect": [
    {"id": "10002_normal", "sample": "extensions\\x4_my_voice\\voice\\10002\\normal"}
  ],
  "targets": [
    {"page": "10002", "contexts": ["normal"], "lines": "all",
     "dest": "voice/10002/{context}/{line}.ogg"}
  ]
}
```
`lines` = `"all"` oder ID-Liste; `dest` mit Platzhaltern `{lang} {page} {context} {line}`.

Vor dem Batch: 5–10 Testzeilen manuell konvertieren und anhören (Web-UI, ohne Code), dann erst die Pipeline bauen.

---

## 8. Kritische Punkte und Risiken (aus beiden Sitzungen)

1. **Größtes Risiko Iteration 1:** Egosoft hat möglicherweise nur Reverb im XML exponiert. Dann ist "tiefer ohne Audioänderung" nicht möglich. Phase 0 kostet eine Stunde – vor jeder weiteren Arbeit.
2. **Resampling-Pitch:** Falls nur das existiert, bedeutet "stark" bei Deutsch Tempoverlust; Obergrenze −3 Halbtöne, Rest über EQ/Reverb.
3. **"Wärmer ≠ einfach Höhen weg":** Zu viel Höhenabsenkung macht Sprache dumpf und unverständlich. Wärme entsteht eher durch moderate Tiefmittenanhebung (200–400 Hz) plus *moderate* Höhenabsenkung → EQ dem reinen Lowpass vorziehen.
4. **Zwei Varianten statt einer** sind unvermeidbar (sprachunabhängige Sound-Library) – zugleich die Chance, EN und DE unabhängig zu tunen.
5. **Sprechstil:** Tempo, Betonung, Gurgeln bleiben bei Filter *und* Voice Conversion erhalten. Falls das der eigentliche Störfaktor ist, löst nur Voice Conversion mit anderem Stimmcharakter oder (mit Lipsync-Nachteilen) TTS das Problem. Deshalb: früh 5–10 Zeilen testen, bevor 1000+ Zeilen verarbeitet werden.
6. **Lipsync:** Alles, was Dateilänge ändert (Resampling, TTS), verschiebt die Mundbewegung aus `lipsync/<line>.xpm`. Tempoerhaltende Verfahren (EFX-Pitch-Shifter, Rubberband, Voice Conversion) nicht.
7. **Quellenlage:** Das Referenzprojekt tridkx/x4-voice-mod hat 0 Stars, ist aber methodisch sauber (MD5-Verifikation, Negativtests) und deckt sich mit dem Nexus-Mod und dem älteren Community-PoC. Eingestuft als belastbar. Spielversion dort: 9.00 – aktuelle Version beim Start prüfen (`version.dat`).
8. **Mod-Konflikte:** Sound-Overhauls patchen dieselbe Datei; Abhängigkeit setzen, damit unser Diff zuletzt greift.

---

## 9. Offene Fragen (vor bzw. in Phase 0 klären)

- [ ] Boso Tas Page-ID (t-Datei oder `voice_pages.csv`)
- [ ] Welche Sound-IDs/Kontexte existieren für diese Page (Basis + DLC-Diff)?
- [ ] Welche Effekt-Elemente und `<sound>`-Attribute akzeptiert das XML (Pitch-Shifter? EQ? Lowpass? nur Reverb?)
- [ ] Hat Boso Ta bereits ein Reverb/Effekt-Preset, das zum störenden Klang beiträgt?
- [ ] Liegen seine Audios im Basis-Katalog, im DLC oder in beiden?
- [ ] Aktuelle X4-Version; hat sich seit 9.00 etwas am Format geändert?
- [ ] Plan B: Muss der Zielordner in der Extension `voice` oder `voice-l044` heißen (Sprachsuffix-Logik beim Redirect)?
- [ ] ElevenLabs: Preis pro Minute Voice Changer, Credits für geschätzte Zeilenmenge (nur falls Option 3)
- [ ] Wirkt `<effects>` auch bei 2D/Comm-Sounds oder nur bei `is3d="1"`?

---

## 10. Rechtliches und Ethik
- Modifizierte Egosoft-Audios **privat** nutzen: unkritisch.
- Öffentlich verteilen (Nexus): Grauzone; der Split Voice Overhaul existiert dort seit 2020 unbeanstandet. Eine reine Effekt-Mod (Iteration 1) enthält keine Egosoft-Assets und ist unproblematisch.
- KI-Stimmen: keine Stimme eines realen Sprechers ohne Einwilligung klonen; Library- oder Stock-Stimmen verwenden.

---

## 11. Quellen

| Quelle | URL | Inhalt |
|---|---|---|
| tridkx/x4-voice-mod | https://github.com/tridkx/x4-voice-mod | Formate, Mechanik, Routen A–E, Toolchain, Fallen |
| Split Voice Overhaul (Nexus 598) | https://www.nexusmods.com/x4foundations/mods/598 | Pitch-Filter-Mod, Route C, `-prefersinglefiles` |
| X4unpacker (Nexus 2142) | https://www.nexusmods.com/x4foundations/mods/2142 | Entpacker GUI/CLI |
| X4 Customizer | https://github.com/bvbohnen/X4_Customizer/ und https://forum.egosoft.com/viewtopic.php?p=4773285 | Diff-/Extension-Framework |
| Egosoft-Forum "Getting Started" | https://forum.egosoft.com/viewtopic.php?p=4768514 | XRCatTool, Extensions-Ordner, `-logfile` |
| h2odragon HOWTO (Egosoft-Wiki) | https://wiki.egosoft.com/X4%20Foundations%20Wiki/Modding%20Support/ScriptingMD/Community%20Guides/h2odragon's%20HOWTO-hackx4f/ | Katalogstruktur, voice-L044/L049, t-Dateien |
| Vectorial1024 PoC | https://github.com/Vectorial1024/v1024_poc_voicelines (laut tridkx) | Route C, Route A widerlegt (X4 5.0) |
| Steam: Soundproblem / openal32.dll | https://steamcommunity.com/app/392160/discussions/0/4772129115120091113 | OpenAL-Backend |
| Steam: Reen neue Stimme 7.5 | https://steamcommunity.com/app/392160/discussions/0/592891171955540387 | Egosoft tauscht Stimmen |
| Nexus "Drunken Sounds" Kommentare | https://www.nexusmods.com/x4foundations/mods/1948?tab=posts | "No matching node", Pfade ohne Endung |
| Nexus "X4 Legacy Music" | https://www.nexusmods.com/x4foundations/mods/56 | Zweiter Extensions-Ort (Dokumente) |
| Steam Workshop Deep Thrust Kommentare | https://steamcommunity.com/sharedfiles/filedetails/comments/3335334169 | Ladereihenfolge/Dependency, Konflikte |
| GameStar Mod-Guide | https://www.gamestar.de/artikel/x4-foundations-beste-mods-download-und-installation,3378800,seite2.html | Installation, Erweiterungen-Menü |
| ElevenLabs Voice Changer (Skill-Doku) | https://mcpservers.org/fr/agent-skills/elevenlabs/voice-changer | API, Verhalten, Formate |
| Eledubby | https://pypi.org/project/eledubby/ | Batch-STS mit Timing-Erhalt |
| X4FProjector | https://github.com/bno1/X4FProjector | Datenexport (Randnotiz) |

Trainingswissen ohne Quelle: Sprach-IDs 44/49 (durch tridkx bestätigt), Boso Ta im Basisspiel, EFX-Effektliste und Parameterbereiche, Egosoft-Diff-/content.xml-Syntax, ffmpeg-Filter, RVC/Applio.

---

## 12. Vorschlag für die Projektsteuerung in Claude Code

**Projektmodus: P1 (Vorschlag)** – mehrere Sitzungen, mehrere Meilensteine, Git-Repo nötig. Dieses Dokument kann in die vier Artefakte aufgeteilt werden: Abschnitt 6 → `docs/superpowers/plans/`, Abschnitt 9 → `docs/projekt/CURRENT_STATE.md` (offen), Meilensteine unten → `docs/projekt/MILESTONES.md`. Die Entscheidung trifft Slovi.

**Meilenstein-Entwurf (Ergebnisse, von außen prüfbar):**
1. Effekt-Schema und Boso Tas Sound-IDs sind dokumentiert – Beleg: Datei `docs/phase0-befund.md` mit grep-Ausgaben und ID-Liste.
2. Eine Test-Extension verändert hörbar Bettys Stimme über `<effects>` – Beleg: Spielstart ohne "No matching node" im Log, hörbarer Unterschied.
3. Boso Ta klingt in EN-Variante hörbar tiefer und wärmer, Dialoge laufen synchron – Beleg: Hörprotokoll, Savegame am HQ.
4. DE-Variante mit stärkerer Einstellung – Beleg: wie 3.
5. Beide Varianten paketiert mit README und `check_extensions.py`-Lauf ohne Fehler.
6. (Optional, nur bei Bedarf) Plan B: Audio-Redirect mit gefilterten oder konvertierten Dateien.

**Erste Session-Checkliste:**
- [ ] Repo anlegen (`git init`), dieses Dokument nach `docs/` legen
- [ ] X4-Version aus `version.dat` notieren, Spielpfad in Umgebungsvariable (`X4_GAME_DIR`), nicht hart im Code
- [ ] `tridkx/x4-voice-mod` klonen, `voice_pages.csv` nach Boso durchsuchen
- [ ] Entpacken: `sound_library.xml` (Basis + DLC), `t/0001-l044.xml`, `t/0001-l049.xml`
- [ ] Phase-0-greps ausführen, Befund dokumentieren, Entscheidungsmatrix anwenden
- [ ] Betty-Schnelltest-Extension bauen und im Spiel prüfen
