# Meilensteinplan – X4-Mod „Boso Ta: wärmere Stimme"

Ziel: Boso Tas Stimme (Stimm-Set 10201) klingt in X4 Foundations tiefer und wärmer – zuerst rein über Engine-Effekte, ohne Audiodateien zu ändern. Zwei Varianten: Deutsch (stark), Englisch (mittel).

Übernommen aus dem Handoff-Dokument (Abschnitt 12) vom 2026-10-22.

| Nr. | Meilenstein (Ergebnis) | Abnahmekriterium (von außen prüfbar) | Status |
|---|---|---|---|
| 1 | Effekt-Schema der Engine und Boso Tas Sound-IDs sind dokumentiert | `docs/phase0-befund.md` enthält Page-ID, Sound-ID-Liste und das XSD-belegte Effekt-Schema | **erreicht** (2026-10-22, Beleg: `docs/phase0-befund.md`) |
| 2 | Eine Test-Extension verändert hörbar eine Stimme über `<effects>` | Spielstart ohne „No matching node"; eine Sprecherstimme klingt deutlich tiefer | **erreicht** (2026-10-22, Beleg: Diagnose v5, Slovi: „der Tutor ist extrem langsam und tief"; Log ohne Patchfehler) |
| 3 | Boso Ta klingt in der DE-Variante nicht mehr nervig, Dialoge bleiben verständlich | Hörurteil von Slovi am Spieler-HQ (zugewandt, abgewandt, Hintergrundgespräch), Parameter in `config/variants.json` eingefroren | **erreicht** (2026-10-22, Beleg: Slovi „das passt jetzt so", Variante `d12_alien_mid` +9 dB, 2D) |
| 4 | EN-Variante | wie 3, mit englischer Sprachspur | zurückgestellt (Slovi spielt Deutsch; Rezept im README) |
| 5 | Varianten paketiert mit README; Validator läuft ohne Fehler | `python -I tools/validate_mod.py` meldet 0 Fehler; README beschreibt Erzeugung, Installation, Deinstallation | in Arbeit (README und Validator erledigt, Commit offen) |
| 6 | Plan B: Audio-Redirect mit bearbeiteten Dateien | Bearbeitete Dateien werden über `<sample>`-Umleitung geladen, Lipsync bleibt synchron | **erreicht** (2026-10-22, Beleg: Diagnose v6 und installierte Variante `bosota_voice_alien`) |

## Änderungsvermerke

- 2026-10-22 – Plan angelegt (Orchestrator, aus Handoff-Dokument). **Vorschlag an Slovi:** Reihenfolge 3 (DE) vor 4 (EN), da die Spielsprache Deutsch ist. Keine inhaltliche Änderung ohne Freigabe.
- 2026-10-22 – Meilenstein 2 umformuliert von „Bettys Stimme" auf „eine Stimme" (Orchestrator, nur Formulierung): Der Nachweis gelang mit dem Flugschul-Tutor, weil das Tutorial in Sekunden lädt. Ziel und Kriterium unverändert.
- 2026-10-22 – **Zieländerung durch Slovi:** „tiefer und wärmer" per Engine-Effekt reichte nicht („immer noch unangenehm piepsig"); neues Ziel „nicht mehr nervig, verständlich" über bearbeitete Audiodateien (Plan B wurde vom Optional zum Hauptweg). Meilenstein 3 entsprechend umformuliert, 4 zurückgestellt, 6 erreicht.
