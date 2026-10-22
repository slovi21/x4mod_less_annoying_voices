# Zustands-Snapshot

**Aktueller Meilenstein:** 3 erreicht (2026-10-22), 5 in Arbeit (Paketierung/README erledigt, Commit offen).

## Erledigt
- Boso Ta spricht im Spiel mit der Variante `d12_alien_mid` (+9 dB): eine Oktave tiefer, Formanten mitverschoben, Frequenzverschiebung −70 Hz, Chorus, Mitten-Fokus, Gespräche 2D ohne Geometrie-Dämpfung. **Slovi: „das passt jetzt so."**
- Pipeline komplett: `x4cat_extract.py` → `process_audio.py` (ffmpeg/Rubberband, zweistufige Lautheitsnormalisierung, `--gain-db`) → `build_mod.py` (Audio-Umleitung + Attribut-Operationen) → `validate_mod.py` (Selektoren, Attribute) → `install_mod.py` (kopiert XML + Audio, entfernt alle `bosota_*`).
- Testvariante (Betty) aus Konfiguration und `dist/` entfernt. README auf den tatsächlichen Weg umgeschrieben.
- Audio (2 324 Dateien) liegt nur unter `build/audio/d12_alien_mid_g9/` und im Spielordner, nicht im Repo.

## Offen
- Commit des Standes (vorgeschlagen, nicht ausgeführt).
- Optional: englische Audio-Variante (gleiches Rezept auf `voice-l044/10201/normal`), nur bei Bedarf.
- Optional: eigenes Radio-Filter für die Funk-Kontexte (derzeit nutzen alle den normalen Satz).

## Getroffene Entscheidungen
- Engine-Effekte (Plan A) verworfen: Pitch ist Resampling, Slovi nahm −3 HT nicht wahr und fand −9 HT weiter unangenehm.
- KI-Stimmumwandlung (ElevenLabs/RVC) nicht gewählt; ffmpeg-Bearbeitung mit Hörproben in Runden war ausreichend.
- `is3d="0"` für `10201_normal`/`10201_normal_npc`: Blickrichtung machte 90 % → 60 % Lautstärke und Unverständlichkeit aus.
- `noocclusion="true"` auf allen Einträgen (Boso hinter Glas).
- Alle Kontexte zeigen auf den bearbeiteten `normal`-Satz.

## Bekannte Probleme / Risiken
- Boronen-Fraktionsvertreter bekommt die Stimme mit (gleicher Sprecher, Set geteilt).
- Hintergrundgespräche von Boso (normal_npc) sind 2D: überall auf der Plattform gleich laut.
- Pegel +9 dB mit Begrenzer: Spitzen bei −0,3 dBTP, Begrenzer greift hörbar wenig, aber messbar.
- Verteilung (Nexus) wäre eine Grauzone, da bearbeitete Egosoft-Audios enthalten wären; Repo enthält sie bewusst nicht.

## Nächster sinnvoller Schritt
Commit. Danach neues Spiel starten und über längere Zeit hören; Feinjustage nur bei Bedarf (Pegel ±3 dB, Mitten-Filter stärker/schwächer).

## Belege
- `python -I tools/validate_mod.py` → 0 Fehler in 3 Extensions (2026-10-22)
- `build/process_d12_alien_mid_g9.log` → 2324 OK, 0 Fehler
- Slovis Hörurteile in dieser Datei und `docs/dev-team/LESSONS.md`
