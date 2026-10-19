# 🎧 PDF a Audiolibro

Convierte el texto de cualquier PDF en un audiolibro MP3 con voces neuronales de sonido natural (en español, inglés y muchos otros idiomas).

**Versión actual:** 1.3.0 — ver [CHANGELOG.md](CHANGELOG.md)

---

## 📋 Requisitos

- macOS o Linux (en Windows funciona usando los comandos de Python directamente)
- Python 3.8 o superior
- Conexión a internet (las voces se generan con el servicio de Microsoft Edge)

## ⚙️ Pre-instalación

Desde la carpeta del proyecto, ejecuta una sola vez:

```bash
cd ~/Desktop/scripts/pdf-to-audiobook
./install.sh
```

El script de instalación:

1. Verifica que tengas Python 3.8+.
2. Crea un entorno virtual aislado en `.venv/` (no afecta tu Python del sistema).
3. Instala las dependencias de `requirements.txt` (`pdfplumber` y `edge-tts`).

<details>
<summary>Instalación manual (alternativa)</summary>

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
</details>

## ▶️ Uso

Usa el atajo `audiobook.sh`, que activa el entorno virtual automáticamente:

```bash
./audiobook.sh mi_libro.pdf
```

Esto crea la carpeta `mi_libro_audiobook/` con un MP3 por cada 25 páginas. El script detecta el idioma del libro y elige la voz, y omite automáticamente las páginas de índice.

### Ejemplos

| Qué quieres hacer | Comando |
|---|---|
| Libro en español (México) | `./audiobook.sh libro.pdf --voice es-MX-DaliaNeural` |
| Voz en español (España) | `./audiobook.sh libro.pdf --voice es-ES-AlvaroNeural` |
| Leer más rápido | `./audiobook.sh libro.pdf --rate +15%` |
| Solo páginas 5 a 120 | `./audiobook.sh libro.pdf --start 5 --end 120` |
| Además, un solo MP3 completo | `./audiobook.sh libro.pdf --merge` |
| Partes de 10 páginas | `./audiobook.sh libro.pdf --pages-per-part 10` |
| Guardar el texto limpio para revisarlo | `./audiobook.sh libro.pdf --save-text` |
| Incluir las páginas de índice | `./audiobook.sh libro.pdf --keep-index` |
| Elegir carpeta de salida | `./audiobook.sh libro.pdf -o ~/Music/Audiolibros` |
| Ver voces en español | `./audiobook.sh --list-voices es` |
| Ver la versión | `./audiobook.sh --version` |

### Todas las opciones

| Opción | Descripción | Predeterminado |
|---|---|---|
| `-v`, `--voice` | Voz a usar | Automática según el idioma del libro |
| `-r`, `--rate` | Velocidad (`-10%`, `+20%`) | `+0%` |
| `--start` / `--end` | Rango de páginas | Todo el PDF |
| `--pages-per-part` | Páginas por archivo MP3 | `25` |
| `--merge` | Crea también un MP3 con todo el libro | No |
| `--keep-index` | No omite las páginas de índice | No (se omiten) |
| `--save-text` | Guarda el texto extraído en `.txt` | No |
| `-o`, `--outdir` | Carpeta de salida | `<nombre>_audiobook` |
| `--list-voices [IDIOMA]` | Lista las voces disponibles | — |

## ❓ Problemas comunes

- **Mala pronunciación**: confirma que la voz coincide con el idioma del libro (el script lo detecta solo, pero puedes forzarlo con `--voice`). Usa `--save-text` para revisar si el texto extraído tiene palabras pegadas o cortadas.
- **La voz no respeta la puntuación**: revisa con `--save-text` que las frases terminen en punto. Una velocidad un poco más lenta (`--rate -10%`) también hace más claras las pausas, y otras voces (`es-ES-AlvaroNeural`, `es-MX-JorgeNeural`) pueden entonar mejor.
- **Se lee el índice**: el script omite automáticamente las páginas donde la mayoría de las líneas terminan en un número de página. Si un índice con formato inusual se cuela, usa `--start` para empezar después de él.
- **Se leen portadas, prólogos u otras secciones**: usa `--start`/`--end` para limitar el rango de páginas.
- **"No text found"**: el PDF es un escaneo (imágenes). Aplícale OCR primero, por ejemplo con `brew install ocrmypdf` y luego `ocrmypdf entrada.pdf salida.pdf`.
- **"Primero ejecuta ./install.sh"**: falta el entorno virtual; corre la pre-instalación.
- **`Permission denied` al ejecutar**: da permisos con `chmod +x install.sh audiobook.sh`.

## 🗂️ Control de versiones

El proyecto es un repositorio **Git** y sigue [Versionado Semántico](https://semver.org/lang/es/):

- **MAYOR** (2.0.0): cambios que rompen el uso anterior.
- **MENOR** (1.1.0): funciones nuevas compatibles.
- **PARCHE** (1.0.1): correcciones de errores.

La versión vive en tres lugares que deben coincidir: `VERSION`, la variable `__version__` en `pdf_to_audiobook.py`, y `CHANGELOG.md`.

### Flujo para publicar una nueva versión

```bash
# 1. Haz tus cambios y revisa qué cambió
git status
git diff

# 2. Actualiza VERSION, __version__ y agrega la entrada en CHANGELOG.md

# 3. Guarda los cambios y etiqueta la versión
git add .
git commit -m "Agrega soporte para capítulos"
git tag -a v1.1.0 -m "Versión 1.1.0"

# Ver historial y versiones
git log --oneline
git tag
```

Para volver a una versión anterior: `git checkout v1.0.0` (y `git checkout main` para regresar).

Los audiolibros generados (`*.mp3`, `*_audiobook/`) y el entorno `.venv/` están excluidos en `.gitignore`.

## 📁 Estructura

```
pdf-to-audiobook/
├── pdf_to_audiobook.py   # Script principal
├── audiobook.sh          # Atajo que usa el entorno virtual
├── install.sh            # Pre-instalación
├── requirements.txt      # Dependencias
├── VERSION               # Versión actual
├── CHANGELOG.md          # Historial de cambios
├── README.md             # Este archivo
└── .gitignore
```
