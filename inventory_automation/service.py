"""Lógica de negocio y generación de resultados reproducibles."""

import csv
import json
import logging
from pathlib import Path
from typing import Any

from .models import Device, InventoryResult

LOGGER = logging.getLogger(__name__)


def validate_inventory(raw_devices: list[dict[str, Any]]) -> InventoryResult:
    """Convierte registros válidos y conserva los errores por registro."""
    devices: list[Device] = []
    errors: list[str] = []
    seen_ips: set[str] = set()
    for record_number, raw_device in enumerate(raw_devices, start=1):
        try:
            device = Device.from_mapping(raw_device)
            if device.ip_address in seen_ips:
                raise ValueError(f"IP duplicada: {device.ip_address}")
            seen_ips.add(device.ip_address)
            devices.append(device)
        except ValueError as error:
            message = f"Registro {record_number}: {error}"
            LOGGER.warning(message)
            errors.append(message)
    return InventoryResult(devices=devices, errors=errors)


def write_results(result: InventoryResult, output_dir: Path) -> None:
    """Escribe resultados JSON y CSV, creando el directorio con permisos del usuario."""
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = {"summary": result.summary(), "devices": [device.to_dict() for device in result.devices], "errors": result.errors}
    (output_dir / "inventory_report.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    with (output_dir / "inventory_report.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["name", "ip_address", "role", "status", "location"])
        writer.writeheader()
        writer.writerows(device.to_dict() for device in result.devices)
