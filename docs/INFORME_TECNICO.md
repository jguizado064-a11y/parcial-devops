# Informe técnico - Automatización segura de inventario de red

## Portada

- Unidad didáctica: DevOps: fundamentos
- Bloque: **[COMPLETAR]**
- Proyecto: Automatización segura de inventario de red
- Integrantes: **Cindy Yannet Alcalá Arata; Ramón Francisco León Tavara; Miguel Ángel Celin Cochachi Puente de la Vega; José Fernando Rodríguez Guizado**
- Fecha de entrega: **[COMPLETAR]**
- Repositorio Git: **[COMPLETAR URL HTTPS DEL REPOSITORIO]**

## Introducción

La administración manual de inventarios distribuidos causa registros desactualizados, errores de transcripción y dificultades para detectar activos en mantenimiento. Esta solución automatiza la consulta y el análisis de inventario. Consume un servicio REST únicamente por HTTPS o recibe archivos de laboratorio; después valida, normaliza y publica resultados reutilizables en JSON y CSV. El diseño privilegia confidencialidad, disponibilidad, trazabilidad y fácil mantenimiento.

## Desarrollo

### Arquitectura y flujo

1. La CLI recibe un archivo local o una URL HTTPS autorizada.
2. El cliente REST construye `GET`, envía `Accept: application/json`, configura timeout y reintentos progresivos ante fallas transitorias 5xx o de red.
3. Si el servicio exige autenticación, recibe un token Bearer desde una variable de entorno. El secreto no se escribe en código, commits ni logs.
4. Los analizadores convierten JSON, CSV, XML o YAML al mismo modelo de dispositivo.
5. La capa de validación verifica campos obligatorios, IP válida, estado permitido e IP no duplicada. Un registro defectuoso queda reportado sin detener los demás.
6. La salida registra resumen, dispositivos aceptados y errores en `inventory_report.json` y `inventory_report.csv`.

### Decisiones técnicas y justificación

| Decisión | Justificación | Impacto |
| --- | --- | --- |
| Python estándar (`urllib`, `json`, `csv`, `xml`) | Reduce dependencias y facilita su ejecución en DEVASC VM. | Reproducibilidad y menor superficie de actualización. |
| HTTPS obligatorio | Protege datos y credenciales en tránsito frente a interceptación. | Seguridad y cumplimiento del requisito REST seguro. |
| Token por variable de entorno | Separa secretos del código y permite rotación. | Evita filtraciones en Git. |
| Timeout y reintentos exponenciales | Evita procesos bloqueados y reduce presión sobre APIs con fallas temporales. | Disponibilidad y eficiencia. |
| Arquitectura por módulos | Separa cliente, formatos, validación y salida. | Pruebas sencillas, reutilización y escalabilidad. |
| Validación por registro | Conserva información válida y expone inconsistencias. | Robustez operativa y trazabilidad. |
| Permisos mínimos | Directorio de proyecto `750`; archivos de datos `640`. | Menor privilegio y protección de datos. |

### Linux, permisos y operación

La creación de un usuario de servicio (`useradd`), el grupo de trabajo (`groupadd`), la asignación de grupo (`usermod -aG`), el directorio (`mkdir`) y los permisos (`chmod`, `chown`) demuestran una administración autónoma. `chmod 750` protege la ejecución y lectura del directorio; `chmod 640` limita la lectura de inventarios al propietario y grupo. Si el proyecto se comparte, `chown -R usuario:netops ~/devops-inventory` fija propiedad coherente. Estas decisiones aplican mínimo privilegio sin impedir el trabajo del equipo.

### Control de versiones

Se utiliza Git con ramas `feature/inventory-api` y `docs/technical-report`, commits descriptivos y fusiones no lineales a `main`. Antes de cada commit se ejecutan pruebas; antes de publicar se revisa `git diff --check`. Los conflictos se resuelven identificando los marcadores, preservando la intención de ambos cambios, corriendo pruebas y registrando un commit de resolución. El remoto se configura por HTTPS y solo después de crear el repositorio autorizado por el equipo.

### REST API: autenticación, diagnóstico y solución

| Situación | Diagnóstico | Solución fundamentada |
| --- | --- | --- |
| `400 Bad Request` | Parámetro o payload con sintaxis/valor no válido. | Validar esquema, tipos y parámetros contra el contrato de API. |
| `401 Unauthorized` | Token ausente, vencido o inválido. | Verificar variable de entorno, renovar token y no imprimirlo. |
| `403 Forbidden` | Token sin scope, política o rate limit. | Conceder solo scope necesario; revisar `Retry-After` ante límite. |
| `404 Not Found` | Endpoint, versión o método incorrecto. | Confirmar URL, versión y método en documentación. |
| `429 Too Many Requests` | Límite de solicitudes excedido. | Respetar `Retry-After`, aplicar backoff y reducir consultas. |
| `5xx` o timeout | Falla temporal de servidor, gateway o red. | Revisar logs/trazas, reintentar con backoff y escalar si persiste. |
| JSON inválido | Respuesta inesperada/proxy o contrato roto. | Registrar contexto no sensible, validar `Content-Type` y contactar proveedor. |

El proyecto usa `GET` porque consulta recursos. Una API que modifique inventario exigiría `POST`, `PUT/PATCH` o `DELETE`, validación de payload, autorización específica y auditoría. Para servicios empresariales se recomienda OAuth 2.0 con tokens de corta duración; para laboratorios, un Bearer token o API key en variable de entorno. Ningún mecanismo se considera seguro si se transmite por HTTP o se versiona en el repositorio.

### Buenas prácticas aplicadas

- Nombres en inglés consistentes, docstrings, tipado y funciones de responsabilidad única.
- Errores controlados con mensajes accionables, sin revelar secretos.
- Pruebas unitarias para formatos, validaciones, HTTPS y generación de salida.
- `.gitignore` para entornos virtuales, logs, archivos `.env` y reportes generados.
- Resultados deterministas en JSON/CSV para revisión y automatización posterior.

## Evidencias

Inserte aquí las capturas indicadas en `EVIDENCIAS.md`: permisos Linux, ejecuciones de los cuatro formatos, pruebas, ramas/commits, consulta HTTPS y diagnóstico de error. Cada figura debe llevar un pie breve que explique qué requisito demuestra.

Ejemplo de resultado esperado con `data/inventory.json`:

```text
WARNING Registro 4: Dirección IP inválida: 999.1.1.1
INFO Procesados: 3 | Activos: 2 | Inválidos: 1
```

## Conclusiones

1. La automatización reduce el trabajo manual y entrega inventario validado, trazable y reutilizable.
2. HTTPS, tokens externos, permisos mínimos, validación y reintentos aportan seguridad y confiabilidad sin aumentar innecesariamente la complejidad.
3. La modularidad, las pruebas y Git permiten evolucionar el proyecto hacia APIs de controladores de red reales con menor riesgo.
4. La solución queda preparada para escalar con una base de datos, paginación, OAuth 2.0, CI/CD y auditoría centralizada.
