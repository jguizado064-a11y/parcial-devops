"""Cliente REST mínimo con controles de seguridad para HTTPS."""

import json
import time
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class ApiRequestError(RuntimeError):
    """Error con contexto seguro de una solicitud REST."""


@dataclass(frozen=True)
class HttpsApiClient:
    timeout_seconds: int = 10
    retries: int = 2

    def get_json(self, api_url: str, token: str | None = None) -> Any:
        """Obtiene JSON por HTTPS, sin registrar la credencial."""
        if urlparse(api_url).scheme != "https":
            raise ApiRequestError("La API debe usar HTTPS.")

        headers = {"Accept": "application/json", "User-Agent": "devops-inventory-automation/1.0"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = Request(api_url, headers=headers, method="GET")

        for attempt in range(self.retries + 1):
            try:
                with urlopen(request, timeout=self.timeout_seconds) as response:
                    charset = response.headers.get_content_charset() or "utf-8"
                    return json.loads(response.read().decode(charset))
            except HTTPError as error:
                if 500 <= error.code < 600 and attempt < self.retries:
                    time.sleep(2**attempt)
                    continue
                hint = _http_hint(error.code)
                raise ApiRequestError(f"HTTP {error.code}: {hint}") from error
            except (URLError, TimeoutError, json.JSONDecodeError) as error:
                if attempt < self.retries:
                    time.sleep(2**attempt)
                    continue
                raise ApiRequestError(f"No se pudo completar la solicitud: {error}") from error
        raise ApiRequestError("No se pudo completar la solicitud.")


def _http_hint(status_code: int) -> str:
    hints = {
        400: "revise parámetros y payload.",
        401: "revise el token o la autenticación.",
        403: "revise permisos, alcance del token o límite de tasa.",
        404: "revise método y endpoint.",
        429: "respete Retry-After y aplique espera progresiva.",
        500: "error interno del servicio; reintente y revise logs.",
        502: "gateway no disponible; reintente y revise la conectividad.",
        503: "servicio temporalmente no disponible; reintente más tarde.",
    }
    return hints.get(status_code, "revise la documentación y los logs del servicio.")
