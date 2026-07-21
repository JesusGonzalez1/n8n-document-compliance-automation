from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

WORKFLOW_DIRECTORY = Path("workflows")

JWT_PATTERN = re.compile(
    r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+"
)

PRIVATE_URL_PATTERNS = (
    "docs.google.com/spreadsheets/d/",
)

FORBIDDEN_TOP_LEVEL_FIELDS = {
    "pinData",
    "versionId",
    "meta",
    "id",
    "tags",
}


def validate_workflow(path: Path) -> list[str]:
    errors: list[str] = []

    try:
        raw = path.read_text(encoding="utf-8")
        workflow: dict[str, Any] = json.loads(raw)
    except (OSError, json.JSONDecodeError) as exc:
        return [f"{path}: JSON inválido: {exc}"]

    if not isinstance(workflow.get("nodes"), list):
        errors.append(f"{path}: no contiene una lista de nodos.")

    if not isinstance(workflow.get("connections"), dict):
        errors.append(f"{path}: no contiene conexiones válidas.")

    if workflow.get("active") is True:
        errors.append(f"{path}: el workflow público debe estar inactivo.")

    for field in FORBIDDEN_TOP_LEVEL_FIELDS:
        if workflow.get(field):
            errors.append(f"{path}: contiene el campo interno '{field}'.")

    if JWT_PATTERN.search(raw):
        errors.append(f"{path}: contiene una cadena con formato JWT.")

    for value in PRIVATE_URL_PATTERNS:
        if value in raw:
            errors.append(f"{path}: contiene una URL o identificador privado.")

    for node in workflow.get("nodes", []):
        node_name = node.get("name", "sin nombre")

        if node.get("credentials"):
            errors.append(
                f"{path}: el nodo '{node_name}' conserva referencias "
                "de credenciales."
            )

        if node.get("webhookId"):
            errors.append(
                f"{path}: el nodo '{node_name}' conserva un webhookId."
            )

    return errors


def main() -> int:
    files = sorted(WORKFLOW_DIRECTORY.glob("*.json"))

    if not files:
        print("No se encontraron workflows JSON.", file=sys.stderr)
        return 1

    errors: list[str] = []

    for file in files:
        errors.extend(validate_workflow(file))

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        return 1

    print(f"Validación completada: {len(files)} workflow(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())