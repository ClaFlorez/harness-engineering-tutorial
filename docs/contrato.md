# Contrato del validador

Estas reglas son didácticas; no son límites de la API de YouTube.

- Entrada: objeto JSON. Otros valores JSON se rechazan.
- `title`: texto de 1 a 100 caracteres después de quitar espacios exteriores.
- `script`: texto de al menos 20 caracteres después de quitar espacios exteriores.
- `tags`: campo opcional. Si aparece, debe ser una lista de hasta cinco textos.
- Cada etiqueta debe contener texto no vacío después de quitar espacios exteriores.
- Se permiten la lista vacía y las etiquetas repetidas. Un valor `null` no es una lista y se rechaza.
- Los espacios se ignoran solo para comprobar las etiquetas: se conserva la entrada original, sin recortar textos ni eliminar duplicados.
- Los campos desconocidos se permiten; los obligatorios ausentes se rechazan.
- La función `validate_episode` devuelve una lista de errores y no modifica la entrada.
- Lista vacía significa entrada válida. Se acumulan los errores de campos.
- La CLI recibe una ruta a un archivo JSON UTF-8, también admite BOM UTF-8.
- La CLI imprime un objeto JSON con `ok` booleano y `errors` lista de textos.
- Código de salida: 0 si es válido, 1 si es inválido o no puede leerse/decodificarse.
- Uso incorrecto de argumentos: argparse imprime ayuda/error y devuelve 2.

No hay acceso a red, generación de contenido ni publicación.
