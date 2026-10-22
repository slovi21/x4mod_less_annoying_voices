#!/usr/bin/env bash
# Builds all variants and validates them against the game's real sound_library.xml.
# Usage: ./init.sh   (game folder from X4_GAME_DIR or the default path)
set -euo pipefail                      # -e: stop on error, -u: undefined variables are errors, -o pipefail: propagate errors inside pipes
cd "$(dirname "$0")"                   # change into the repository folder regardless of where the script was started
python -I tools/build_mod.py           # -I: isolated mode (no environment variables, no user site packages)
python -I tools/validate_mod.py
