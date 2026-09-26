"""Validador didáctico, independiente de servicios externos."""

import argparse
import json
from pathlib import Path


def validate_episode(data: object) -> list[str]:
    """Devuelve errores de contrato sin modificar la entrada."""
    if not isinstance(data, dict):
        return ["El episodio debe ser un objeto JSON."]
    errors = []
    title = data.get("title")
    if not isinstance(title, str) or not 1 <= len(title.strip()) <= 100:
        errors.append("title debe contener entre 1 y 100 caracteres útiles.")
    script = data.get("script")
    if not isinstance(script, str) or len(script.strip()) < 20:
        errors.append("script debe contener al menos 20 caracteres útiles.")
    if "tags" in data:
        tags = data["tags"]
        if not isinstance(tags, list):
            errors.append("tags debe ser una lista.")
        else:
            if len(tags) > 5:
                errors.append("tags debe contener como máximo cinco etiquetas.")
            for index, tag in enumerate(tags):
                if not isinstance(tag, str) or not tag.strip():
                    errors.append(f"tags[{index}] debe ser texto no vacío.")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Ruta al episodio JSON")
    args = parser.parse_args()
    try:
        data = json.loads(args.file.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors = [f"No se pudo leer el episodio: {exc}"]
    else:
        errors = validate_episode(data)
    print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
