# Guía del laboratorio

Alcance: esta carpeta y sus descendientes.

- Lee `docs/contrato.md` para conocer el comportamiento esperado.
- Consulta `README.md` para los ejercicios y `docs/bitacora.md` para decisiones.
- Mantén Python 3.11+ sin dependencias externas.
- Verifica con `python -m unittest discover -s tests -v` desde esta carpeta.
- Comprueba la CLI con `python validator.py examples/episodio.json`.
- Para cambiar comportamiento, actualiza el contrato y las pruebas pertinentes.
- Conserva la validación pura separada de la lectura de archivos y la salida CLI.
- No modifiques archivos del proyecto padre como parte de este laboratorio.
- Resume cambios y resultados reales de ejecución; declara lo que no verificaste.
