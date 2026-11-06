# Guía de evidencias de laboratorio

Capture cada evidencia en la DEVASC VM. Oculte tokens, API keys, IP públicas sensibles y datos personales ajenos.

| Evidencia | Comando o acción | Qué debe observarse |
| --- | --- | --- |
| Entorno Linux | `whoami; pwd; ls -la` | Usuario, ruta de trabajo y permisos iniciales. |
| Usuarios y grupos | `id; getent group netops` | Pertenencia al grupo de trabajo. |
| Permisos | `stat -c '%A %n' . data/inventory.json` | Directorio `750` y datos `640` (o política equivalente justificada). |
| Ejecución JSON | `python -m inventory_automation --input-file data/inventory.json --output-dir evidence/output --verbose` | Tres registros válidos y un error de IP controlado. |
| Otros formatos | Ejecute el mismo comando para `.csv`, `.xml` y `.yaml`. | Procesamiento de cuatro formatos. |
| Pruebas | `python -m unittest discover -s tests -v` | Todas las pruebas aprobadas. |
| Git | `git log --oneline --graph --all` y `git branch -a` | Ramas, commits descriptivos e historial limpio. |
| REST/HTTPS | Ejecute con un endpoint autorizado y `--verbose`. | URL HTTPS, código/respuesta y resultados; no mostrar token. |
| Diagnóstico | Capture un error controlado 401/404/429/5xx o use las pruebas. | Código, causa, solución aplicada y reintento cuando corresponda. |

Nombre sugerido: `E01_linux_permisos.png`, `E02_json.png`, ..., `E09_api_error.png`. Inserte las capturas reales en el informe antes de la entrega.
