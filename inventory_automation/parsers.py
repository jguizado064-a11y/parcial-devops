"""Lectura segura de formatos de inventario admitidos."""

import csv
import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree


class InventoryFormatError(ValueError):
    """Indica un formato o una estructura de inventario no admitida."""


def parse_file(source: Path) -> list[dict[str, Any]]:
    """Devuelve dispositivos desde JSON, CSV, XML o YAML simple."""
    suffix = source.suffix.lower()
    content = source.read_text(encoding="utf-8")
    try:
        if suffix == ".json":
            payload = json.loads(content)
            return _extract_devices(payload)
        if suffix == ".csv":
            return list(csv.DictReader(content.splitlines()))
        if suffix == ".xml":
            return _parse_xml(content)
        if suffix in {".yaml", ".yml"}:
            return _parse_simple_yaml(content)
    except (json.JSONDecodeError, csv.Error, ElementTree.ParseError) as error:
        raise InventoryFormatError(f"No se pudo analizar {source.name}: {error}") from error
    raise InventoryFormatError("Formato no admitido. Use JSON, CSV, XML, YAML o YML.")


def parse_api_payload(payload: Any) -> list[dict[str, Any]]:
    """Acepta una lista de dispositivos o un objeto con la clave devices."""
    return _extract_devices(payload)


def _extract_devices(payload: Any) -> list[dict[str, Any]]:
    devices = payload.get("devices") if isinstance(payload, dict) else payload
    if not isinstance(devices, list) or not all(isinstance(item, dict) for item in devices):
        raise InventoryFormatError("La respuesta debe ser una lista o un objeto con la lista 'devices'.")
    return devices


def _parse_xml(content: str) -> list[dict[str, Any]]:
    root = ElementTree.fromstring(content)
    return [
        {child.tag: (child.text or "").strip() for child in device}
        for device in root.findall("device")
    ]


def _parse_simple_yaml(content: str) -> list[dict[str, Any]]:
    """Analiza el YAML restringido usado en las muestras, sin ejecutar código."""
    devices: list[dict[str, Any]] = []
    current: dict[str, str] | None = None
    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#") or line == "devices:":
            continue
        if line.startswith("- "):
            if current is not None:
                devices.append(current)
            current = {}
            line = line[2:].strip()
        if ":" not in line or current is None:
            raise InventoryFormatError(f"YAML no admitido en la línea {line_number}.")
        key, value = line.split(":", maxsplit=1)
        current[key.strip()] = value.strip().strip("\"'")
    if current is not None:
        devices.append(current)
    if not devices:
        raise InventoryFormatError("El archivo YAML no contiene dispositivos.")
    return devices
