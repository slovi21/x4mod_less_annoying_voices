# Meilensteinplan – X4-Mod „Boso Ta: wärmere Stimme"

Ziel: Boso Tas Stimme (Stimm-Set 10201) klingt in X4 Foundations tiefer und wärmer – zuerst rein über Engine-Effekte, ohne Audiodateien zu ändern. Zwei Varianten: Deutsch (stark), Englisch (mittel).

Übernommen aus dem Handoff-Dokument (Abschnitt 12) vom 2026-10-22.

| Nr. | Meilenstein (Ergebnis) | Abnahmekriterium (von außen prüfbar) | Status |
|---|---|---|---|
| 1 | Effekt-Schema der Engine und Boso Tas Sound-IDs sind dokumentiert | `docs/phase0-befund.md` enthält Page-ID, Sound-ID-Liste und das XSD-belegte Effekt-Schema | **erreicht** (2026-10-22, Beleg: `docs/phase0-befund.md`) |
| 2 | Eine Test-Extension verändert hörbar eine Stimme über `<effects>` | Spielstart ohne „No matching node"; eine Sprecherstimme klingt deutlich tiefer | **erreicht** (2026-10-22, Beleg: Diagnose v5, Slovi: „der Tutor ist extrem langsam und tief"; Log ohne Patchfehler) |
| 3 | Boso Ta klingt in der DE-Variante hörbar tiefer und wärmer, Dialoge bleiben verständlich | Hörprotokoll am Spieler-HQ (Gespräch + Comm-Fenster), Parameter in `config/variants.json` eingefroren | offen |
| 4 | EN-Variante mit mittlerer Einstellung | wie 3, mit englischer Sprachspur | offen |
| 5 | Beide Varianten paketiert mit README; Validator läuft ohne Fehler | `python -I tools/validate_mod.py` meldet 0 Fehler; README beschreibt Installation, Deinstallation, Konflikte | offen |
| 6 | (Optional, nur bei Bedarf) Plan B: Audio-Redirect mit gefilterten Dateien | Gefilterte Dateien werden über `<sample start>`-Umleitung geladen, Lipsync bleibt synchron | zurückgestellt (nur falls Effekte nicht reichen) |

## Änderungsvermerke

- 2026-10-22 – Plan angelegt (Orchestrator, aus Handoff-Dokument). **Vorschlag an Slovi:** Reihenfolge 3 (DE) vor 4 (EN), da die Spielsprache Deutsch ist. Keine inhaltliche Änderung ohne Freigabe.
- 2026-10-22 – Meilenstein 2 umformuliert von „Bettys Stimme" auf „eine Stimme" (Orchestrator, nur Formulierung): Der Nachweis gelang mit dem Flugschul-Tutor, weil das Tutorial in Sekunden lädt. Ziel und Kriterium unverändert.
