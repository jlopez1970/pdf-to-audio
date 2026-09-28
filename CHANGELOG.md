# Historial de cambios

Todas las versiones siguen [Versionado Semántico](https://semver.org/lang/es/): `MAYOR.MENOR.PARCHE`.

## [1.0.0] - 2026-09-28
### Agregado
- Extracción de texto de PDF con pdfplumber.
- Limpieza automática: encabezados/pies repetidos, números de página, palabras con guion y saltos de línea.
- Narración con voces neuronales de Microsoft (edge-tts), con selección de voz y velocidad.
- División del audiolibro en partes por número de páginas y opción `--merge` para un solo MP3.
- Rango de páginas (`--start`, `--end`), `--save-text`, `--list-voices` y `--version`.
- Script de pre-instalación `install.sh` y atajo `audiobook.sh`.
