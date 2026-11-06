"""Interfaz de línea de comandos del proyecto."""

import argparse
import logging
import os
import sys
from pathlib import Path

from .client import ApiRequestError, HttpsApiClient
from .parsers import InventoryFormatError, parse_api_payload, parse_file
from .service import validate_inventory, write_results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Procesa inventarios de red desde archivo o API HTTPS.")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input-file", type=Path, help="Archivo JSON, CSV, XML, YAML o YML.")
    source.add_argument("--api-url", help="Endpoint REST HTTPS autorizado.")
    parser.add_argument("--token-env", help="Nombre de la variable de entorno con token/API key.")
    parser.add_argument("--output-dir", type=Path, default=Path("evidence/output"), help="Directorio de informes.")
    parser.add_argument("--verbose", action="store_true", help="Muestra diagnóstico de ejecución.")
    return parser


def main() -> int:
    arguments = build_parser().parse_args()
    logging.basicConfig(level=logging.DEBUG if arguments.verbose else logging.INFO, format="%(levelname)s %(message)s")
    try:
        if arguments.input_file:
            raw_devices = parse_file(arguments.input_file)
        else:
            token = os.getenv(arguments.token_env, "") if arguments.token_env else None
            if arguments.token_env and not token:
                raise ApiRequestError(f"La variable {arguments.token_env} no está definida.")
            payload = HttpsApiClient().get_json(arguments.api_url, token)
            raw_devices = parse_api_payload(payload)
        result = validate_inventory(raw_devices)
        write_results(result, arguments.output_dir)
    except (OSError, InventoryFormatError, ApiRequestError) as error:
        logging.error("Ejecución detenida: %s", error)
        return 2
    summary = result.summary()
    logging.info("Procesados: %s | Activos: %s | Inválidos: %s", summary["total_devices"], summary["active_devices"], summary["invalid_records"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
