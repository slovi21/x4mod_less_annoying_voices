# Zustands-Snapshot

**Aktueller Meilenstein:** 3 – Boso Ta klingt in der DE-Variante hörbar tiefer und wärmer. (Meilenstein 2 am 2026-10-22 erreicht: Diagnose v5, Tutor „extrem langsam und tief" → `<pitch>` wirkt auf Sprache.)

**Jetzt im Spiel installiert:** `bosota_voice_alien` (Audio-Umleitung, 2 324 bearbeitete DE-Zeilen, 93 MB, Variante `d12_alien`). Hörtest im großen Spielstand offen. Dauer bearbeitet = Original + 61 ms (Filterlatenz, unkritisch).

**Richtungswechsel 2026-10-22 (Slovi):** Boso Ta mit Pitch 0.75 ist „immer noch unangenehm piepsig". Engine-Effekte reichen nicht. Statt KI-Stimmumwandlung (vorgelegt, nicht gewählt) hat Slovi ffmpeg installiert und einen **letzten Versuch mit Audiobearbeitung** gewünscht. Umleitungsmechanik bewiesen (Diagnose v6: Ordner `voice`, kein Sprachsuffix).

**Plan B läuft:** `tools/process_audio.py` (Rubberband tempoerhaltend, zweistufige Lautheitsnormalisierung auf −22 LUFS, Varianten als Filterketten). Hörproben in drei Runden (`build/samples*`): Runde 1 Favorit `deep12big`; Runde 2 Favorit **`d12_alien`** (Oktave tiefer, Formanten mitverschoben, Frequenzverschiebung −70 Hz, Chorus); Whisper/Ringmod rauschen, Underwater hallt zu sehr, Thema aber passend. Runde 3 (alien_soft / alien_deep / alien_tank) zur Entscheidung übergeben. Vollverarbeitung aller 2 324 DE-Zeilen mit `d12_alien` nach `build/audio/d12_alien/` gestartet. Neue Variante `alien` (`bosota_voice_alien`, kind=audio) in `config/variants.json`; Installer kopiert Audio aus `build/audio/`, Audio bleibt außerhalb von Git.

## Erledigt
- Meilenstein 1 erreicht: Phase 0 vollständig am Spiel verifiziert (`docs/phase0-befund.md`).
- Repo-Gerüst steht: `config/variants.json` → `tools/build_mod.py` → `dist/` → `tools/validate_mod.py` → `tools/install_mod.py`.
- Drei Varianten gebaut und validiert (0 Fehler): `bosota_warm_de`, `bosota_warm_en`, `bosota_warm_test`.
- Spieltest 1 mit `bosota_warm_test`: Slovi hört bei Boso Ta keinen Unterschied. Log (`debuglog.txt`) belegt: Extension wurde geladen, unsere `sound_library.xml` gelesen (nur Signatur-Warnung), **kein** „No matching node".
- Diagnose v1 (volume 0.03 auf `10201_normal`, Hall auf `10201_comm`, pitch 0.6 auf Betty): **Boso vor Ort fast stumm → der Diff wird angewendet (bewiesen).** Hall und Betty-Pitch: von Slovi nicht bemerkt (unklar, ob Betty/Funk überhaupt gehört).
- Diagnose v2 (pitch auf `normal`, Tiefpass auf `comm`): Funkweg zu Boso Ta im Spiel nicht auffindbar (Missions-Actor, nicht in der Besatzungsliste des HQ). Kein Ergebnis.
- Diagnose v3 (pitch 0.5–0.6 + Tiefpass 0.08 auf `normal`/`comm`): Rückmeldung uneindeutig. Slovi: Boso im Gespräch mit Managerin Karee „leiser, tiefer, langsamer, aber immer noch sehr unangenehm" (läuft aber über das unveränderte `normal_npc`); direktes „Hallo auch" in Originallautstärke (Lautstärke war in v3 nicht verändert); Tiefpass nicht beurteilbar. **Slovi hat nach eigener Aussage ein schlechtes Gehör** → Tests müssen sich an Dauer/Lautstärke festmachen, nicht an Klangfarbe.
- Diagnose v4 (pitch 0.3–0.35 auf allen `10201_*`): von Slovi nicht getestet, Ladezeiten zu lang.
- Diagnose v5 gebaut, validiert und **installiert**: pitch 0.3–0.35 auf `10201_*` (Boso) **und** `10190_*` (Argon-Tutor der Flugschule). Testbett: Tutorial „Flugschule" statt großem Spielstand, Tutor spricht sofort. Beobachtung über die Dauer.
- Schnelleres Testbett geprüft: einziges Szenario mit Boso Ta als Erzähler ist `x4ep1_gamestart_tutorial2` (`debug="true"`, im normalen Spiel versteckt). Alle sichtbaren Tutorials nutzen `scenario_flightschool` mit dem Argon-Tutor (10190).
- Wichtig für die Zielsetzung: Selbst ein (möglicherweise) stark abgesenkter Boso war für Slovi „immer noch sehr unangenehm" → Hinweis, dass der Sprechstil stört, nicht nur die Tonhöhe (Handoff-Risiko 5). Dann hilft nur Voice Conversion (Option 3), RTX 2070 laut Log vorhanden (RVC lokal möglich).
- Geklärt: Set 10201 ist faktisch Boso Tas eigene Stimme (1 681 Plot- vs. 71 generische Zeilen); einziger weiterer Nutzer ist der Boronen-Fraktionsvertreter.

## Offen
- Spieltest 2 mit dem Diagnose-Build (drei Beobachtungen, siehe Kommentar in der Diff-Datei). Danach Hypothese bestätigen oder verwerfen.
- Hypothese H1: Der Diff wirkt, aber die Engine ignoriert `<pitch>` bei Sprach-Sounds; `lowpass 0.25` war zu mild, um es zu hören.
- Falls H1 bestätigt: Plan B (Audio-Redirect mit per ffmpeg bearbeiteten Dateien) – ffmpeg ist nicht installiert.
- Meilensteine 3–5.

## Getroffene Entscheidungen
- Plan A eingeschränkt (Entscheidungsmatrix): Engine bietet nur Resampling-Pitch + Lowpass + Reverb, keinen EQ. Startwerte DE pitch 0.841 / lowpass 0.25, EN 0.891 / 0.35, kein Reverb.
- Keine Dependency auf `ego_dlc_boron` (kein DLC patcht `10201_*`).
- `<effects>` wird per `<add>` neu angelegt (keine ID hat bereits Effekte); Betty-IDs bekommen Kinder in ihr bestehendes `<effects>`.
- Fertige Extensions liegen committed unter `dist/`; extrahierte Spieldateien nur unter `build/` (ignoriert).
- Kein Agenteneinsatz in dieser Sitzung (Aufgabe S1, Kontext lag vollständig beim Orchestrator; deterministischer Validator statt Review).

## Bekannte Probleme / Risiken
- Stimm-Set 10201 teilt sich Boso Ta nur mit dem Boronen-Fraktionsvertreter (gleicher Sprecher). Eine eigene Page für Boso wäre per MD-Diff möglich, aber die Page steckt im Spielstand (`page="10201"` am NPC) und es gibt keine MD-Aktion zum Ändern → nur per Spielstand-Edit oder Neuerzeugung des Actors.
- Slovis Konsole ist PowerShell 5.1: kein `grep`, kein `&&`. Befehle entsprechend formulieren.
- Pitch = Resampling → −3 Halbtöne = 19 % langsamer, Lipsync verschiebt sich. Falls störend: 0.891 oder 0.87.
- `filter frequency`-Skala und `pitch steps`-Semantik sind nicht dokumentiert; nur Hörtest klärt das.
- Nicht verifiziert: ob `<pitch>` auf Sprach-Sounds überhaupt wirkt (deshalb die Betty-Testvariante).

## Nächster sinnvoller Schritt
Slovi startet X4 mit installiertem Diagnose-Build und meldet die drei Beobachtungen (Betty tief/langsam? Boso vor Ort fast stumm? Boso im Funk mit Hall?). Daraus folgt Plan A (Parameter nachstellen) oder Plan B (Audio-Redirect, ffmpeg installieren).

## Belege
- `python -I tools/validate_mod.py` → „Gesamt: 0 Fehler in 3 Extension(s)" (2026-10-22)
- `docs/phase0-befund.md` Abschnitte 1–5 mit Katalog-/XSD-Belegen
- Noch kein Commit (Erstcommit vorgeschlagen, nicht ausgeführt)
