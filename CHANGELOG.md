# Historial de cambios

Todas las versiones siguen [Versionado Semántico](https://semver.org/lang/es/): `MAYOR.MENOR.PARCHE`.

## [1.3.0] - 2026-09-28
### Mejorado
- Puntuación: los guiones de diálogo (—) se convierten en pausas, los títulos cortos ("CANTO I", "Capítulo 3") reciben punto para que la voz haga pausa, y se corrigen espacios faltantes o sobrantes alrededor de la puntuación.
- Puntos suspensivos ("...") se normalizan a "…".
- Las llamadas de nota al pie pegadas a las palabras ("Ulises12") ya no se leen en voz alta.
- Los fragmentos para la voz se cortan correctamente después de comillas de cierre (») y puntos suspensivos.
- Se reconocen números de página en español ("Página 5 de 300").

## [1.2.0] - 2026-09-28
### Agregado
- Se omiten automáticamente las páginas de índice (tabla de contenido e índice alfabético). El script muestra qué páginas omitió.
- Opción `--keep-index` para incluirlas si se desea.

## [1.1.0] - 2026-09-28
### Corregido
- Pronunciación: la voz ahora se elige automáticamente según el idioma del libro (español → `es-MX-DaliaNeural`, inglés → `en-US-AndrewNeural`). Antes, un libro en español se leía con voz en inglés.
- Ligaduras tipográficas (ﬁ, ﬂ) se convierten a letras normales para que las palabras se pronuncien bien.

## [1.0.0] - 2026-09-28
### Agregado
- Extracción de texto de PDF con pdfplumber.
- Limpieza automática: encabezados/pies repetidos, números de página, palabras con guion y saltos de línea.
- Narración con voces neuronales de Microsoft (edge-tts), con selección de voz y velocidad.
- División del audiolibro en partes por número de páginas y opción `--merge` para un solo MP3.
- Rango de páginas (`--start`, `--end`), `--save-text`, `--list-voices` y `--version`.
- Script de pre-instalación `install.sh` y atajo `audiobook.sh`.
