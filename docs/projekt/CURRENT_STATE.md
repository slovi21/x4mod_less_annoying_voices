# Zustands-Snapshot

**Aktueller Meilenstein:** 2 – Test-Extension verändert hörbar eine Stimme. **Erster Spieltest negativ**, Diagnose läuft.

## Erledigt
- Meilenstein 1 erreicht: Phase 0 vollständig am Spiel verifiziert (`docs/phase0-befund.md`).
- Repo-Gerüst steht: `config/variants.json` → `tools/build_mod.py` → `dist/` → `tools/validate_mod.py` → `tools/install_mod.py`.
- Drei Varianten gebaut und validiert (0 Fehler): `bosota_warm_de`, `bosota_warm_en`, `bosota_warm_test`.
- Spieltest 1 mit `bosota_warm_test`: Slovi hört bei Boso Ta keinen Unterschied. Log (`debuglog.txt`) belegt: Extension wurde geladen, unsere `sound_library.xml` gelesen (nur Signatur-Warnung), **kein** „No matching node".
- Diagnose v1 (volume 0.03 auf `10201_normal`, Hall auf `10201_comm`, pitch 0.6 auf Betty): **Boso vor Ort fast stumm → der Diff wird angewendet (bewiesen).** Hall und Betty-Pitch: von Slovi nicht bemerkt (unklar, ob Betty/Funk überhaupt gehört).
- Diagnose v2 gebaut, validiert und **installiert**: pitch 0.5–0.6 (4 Stufen) auf `10201_normal`, Tiefpass 0.03 auf `10201_comm`. Beide Effekte direkt an Boso Ta, keine Lautstärke-Änderung mehr.
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
