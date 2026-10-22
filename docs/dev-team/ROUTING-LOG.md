# Routing-Protokoll

| Datum | Aufgabe (kurz) | Stufe initial | Stufe final | Eskalations-Trigger | optionale Rollen (Auslöser) | Fehlversuche | Aufwand/Modell-Wechsel | Tokens grob | Bemerkung |
|---|---|---|---|---|---|---|---|---|---|
| 2026-10-22 | Phase 0 (Verifikation am Spiel) + Mod-Gerüst: Generator, Validator, Installer, 3 Varianten | S1 | S1 | – | keine | 0 | – | ~250k | Orchestrator direkt statt `implementierer`: gesamter Kontext (Katalogbefunde) lag hier, Dateien klein; Review ersetzt durch deterministischen Validator gegen die echte Spieldatei. Bash-Heredocs mit großen Dateien scheiterten → Write-Tool. Installer zweimal nachgebessert (OneDrive-ReadOnly-Attribut, siehe LESSONS.md). 4 Lessons eingetragen. |
| 2026-10-22 | Debugging „kein hörbarer Unterschied" (systematic-debugging): Log ausgewertet, Diagnose-Build mit drei unabhängigen Beobachtungen, Sprecheranalyse Set 10201 | S1 | S1 | – | keine | 0 | – | ~120k | Orchestrator direkt; Ergebnis hängt am Hörtest von Slovi. |
