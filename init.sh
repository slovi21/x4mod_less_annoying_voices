#!/usr/bin/env bash
# Baut alle Varianten und prüft sie gegen die echte sound_library.xml des Spiels.
# Aufruf: ./init.sh            (Spielordner aus X4_GAME_DIR oder Standardpfad)
set -euo pipefail                      # -e: bei Fehler abbrechen, -u: undefinierte Variablen sind Fehler, -o pipefail: Fehler in Pipes durchreichen
cd "$(dirname "$0")"                   # in den Repo-Ordner wechseln, egal von wo das Skript gestartet wird
python -I tools/build_mod.py           # -I: isolierter Modus (keine Umgebungsvariablen/Nutzerpakete)
python -I tools/validate_mod.py
