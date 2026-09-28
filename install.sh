#!/usr/bin/env bash
# Pre-instalación de pdf-to-audiobook: crea un entorno virtual e instala dependencias.
set -e
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
  echo "❌ No se encontró python3. Instálalo desde https://www.python.org o con: brew install python"
  exit 1
fi

PYVER=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)' || {
  echo "❌ Se requiere Python 3.8 o superior (tienes $PYVER)."; exit 1; }
echo "✅ Python $PYVER encontrado"

if [ ! -d ".venv" ]; then
  echo "📦 Creando entorno virtual (.venv)..."
  python3 -m venv .venv
fi

echo "📥 Instalando dependencias..."
.venv/bin/python -m pip install --upgrade pip -q
.venv/bin/python -m pip install -r requirements.txt -q

chmod +x pdf_to_audiobook.py audiobook.sh
echo ""
echo "✅ Instalación completa. Prueba con:"
echo "   ./audiobook.sh --version"
echo "   ./audiobook.sh mi_libro.pdf"
