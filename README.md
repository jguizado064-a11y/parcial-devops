# Automatización segura de inventario de red

Proyecto práctico para la evaluación parcial de **DevOps: fundamentos**. Consulta un inventario mediante una API REST sobre HTTPS, normaliza datos JSON, CSV, XML y YAML, valida registros y genera resultados en CSV y JSON.

## Integrantes
- Cindy Yannet Alcalá Arata
- Ramón Francisco León Tavara
- Miguel Ángel Celin Cochachi Puente de la Vega
- José Fernando Rodríguez Guizado

## Capacidades

- Solicitudes `GET` por HTTPS, cabecera `Accept`, token opcional desde variable de entorno, tiempo de espera y reintentos.
- Validación del esquema de inventario, manejo explícito de errores 4xx/5xx, errores de red, JSON inválido y archivos mal formados.
- Procesamiento de los formatos JSON, CSV, XML y YAML; salida estructurada y registro de diagnóstico.
- Código modular, tipado, funciones pequeñas, pruebas automatizadas y documentación de decisiones.

## Inicio rápido en DEVASC VM / Linux

```bash
sudo useradd -m -s /bin/bash netops
sudo groupadd netops 2>/dev/null || true
sudo usermod -aG netops "$USER"
mkdir -p ~/devops-inventory && cd ~/devops-inventory
cp -r /ruta/al/proyecto/* .
chmod 750 .
chmod 640 data/*
python3 -m venv .venv
source .venv/bin/activate
python -m unittest discover -s tests -v
python -m inventory_automation --input-file data/inventory.json --output-dir evidence/output
```

Para probar la consulta HTTPS real sin guardar credenciales en el repositorio:

```bash
export INVENTORY_API_TOKEN='reemplaza_con_tu_token'
python -m inventory_automation \
  --api-url 'https://api.github.com/users/octocat/repos' \
  --token-env INVENTORY_API_TOKEN --output-dir evidence/api_output
```

> La API de GitHub se utiliza únicamente como servicio HTTPS público de demostración. Para el escenario de red se debe indicar el endpoint autorizado de la organización. Nunca se debe versionar un token.

## Git y repositorio remoto

```bash
git init
git switch -c feature/inventory-api
git add .
git commit -m "feat: add secure inventory automation"
git switch -c docs/technical-report
git add docs reports README.md
git commit -m "docs: add technical report and evidence guide"
git switch main
git merge --no-ff feature/inventory-api
git merge --no-ff docs/technical-report
git remote add origin https://github.com/USUARIO/devops-inventory-automation.git
git push -u origin main
```

Use commits pequeños y descriptivos; resuelva conflictos revisando `git status`, editando los marcadores de conflicto, ejecutando las pruebas y creando un commit de resolución.

## Evidencias que debe capturar el equipo

Consulte [la guía de evidencias](docs/EVIDENCIAS.md). Las capturas deben ser reales, tomadas en DEVASC VM, e incluir fecha, usuario y resultado del comando sin exponer tokens.

## Estructura

```text
inventory_automation/  Cliente HTTPS, analizadores, modelos y CLI.
data/                  Muestras JSON, CSV, XML y YAML.
tests/                 Pruebas unitarias y de manejo de errores.
docs/                  Informe técnico, decisiones y guía de evidencias.
reports/               Informe técnico PDF listo para entregar.
```
