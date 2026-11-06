"""Modelos y validaciones del dominio de inventario."""

from dataclasses import asdict, dataclass
from ipaddress import ip_address
from typing import Any


@dataclass(frozen=True)
class Device:
    """Representa un activo de red validado."""

    name: str
    ip_address: str
    role: str
    status: str
    location: str

    @classmethod
    def from_mapping(cls, raw_device: dict[str, Any]) -> "Device":
        required_fields = ("name", "ip_address", "role", "status", "location")
        missing_fields = [field for field in required_fields if not str(raw_device.get(field, "")).strip()]
        if missing_fields:
            raise ValueError(f"Campos obligatorios ausentes: {', '.join(missing_fields)}")

        address = str(raw_device["ip_address"]).strip()
        try:
            ip_address(address)
        except ValueError as error:
            raise ValueError(f"Dirección IP inválida: {address}") from error

        status = str(raw_device["status"]).strip().lower()
        if status not in {"active", "inactive", "maintenance"}:
            raise ValueError("El estado debe ser active, inactive o maintenance")

        return cls(
            name=str(raw_device["name"]).strip(),
            ip_address=address,
            role=str(raw_device["role"]).strip(),
            status=status,
            location=str(raw_device["location"]).strip(),
        )

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class InventoryResult:
    """Resultado normalizado que conserva registros válidos y observaciones."""

    devices: list[Device]
    errors: list[str]

    def summary(self) -> dict[str, int]:
        return {
            "total_devices": len(self.devices),
            "active_devices": sum(device.status == "active" for device in self.devices),
            "invalid_records": len(self.errors),
        }
