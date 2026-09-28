#!/usr/bin/env bash
# Atajo: ejecuta el script usando el entorno virtual del proyecto.
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ ! -x "$DIR/.venv/bin/python" ]; then
  echo "Primero ejecuta ./install.sh"; exit 1
fi
exec "$DIR/.venv/bin/python" "$DIR/pdf_to_audiobook.py" "$@"
