"""Genera el informe técnico PDF entregable desde el contenido validado del proyecto."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUTPUT = Path(__file__).parent / "reports" / "Informe_Tecnico_Automatizacion_Inventario.pdf"


def paragraph(text: str, style):
    return Paragraph(text.replace("\n", "<br/>"), style)


def build_pdf() -> None:
    styles = getSampleStyleSheet()
    title = styles["Title"]
    title.alignment = TA_CENTER
    body = styles["BodyText"]
    body.leading = 15
    heading = styles["Heading2"]
    document = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=1.8 * cm, leftMargin=1.8 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm)
    flow = [
        Spacer(1, 4 * cm), paragraph("DEVOPS: FUNDAMENTOS", title), Spacer(1, 0.5 * cm),
        paragraph("Informe técnico: Automatización segura de inventario de red", styles["Heading1"]), Spacer(1, 1 * cm),
        paragraph("Bloque: [COMPLETAR]<br/>Integrantes: Cindy Yannet Alcalá Arata; Ramón Francisco León Tavara; Miguel Ángel Celin Cochachi Puente de la Vega; José Fernando Rodríguez Guizado<br/>Fecha de entrega: [COMPLETAR]<br/>Repositorio Git: [COMPLETAR URL HTTPS]", body),
        PageBreak(), paragraph("Introducción", heading),
        paragraph("La solución consulta inventarios mediante REST sobre HTTPS o procesa archivos de laboratorio. Valida los datos y genera salidas JSON y CSV reutilizables, reduciendo errores manuales y mejorando la trazabilidad.", body),
        paragraph("Desarrollo", heading),
        paragraph("Flujo: entrada por archivo o API HTTPS → autenticación opcional desde variable de entorno → análisis JSON/CSV/XML/YAML → validación de campos, IP, estado y duplicados → reportes estructurados. El cliente usa GET, Accept: application/json, timeout y reintentos progresivos ante fallas transitorias.", body),
        paragraph("Decisiones técnicas", heading),
        Table([
            ["Decisión", "Justificación e impacto"],
            ["HTTPS obligatorio", "Protege la información y las credenciales en tránsito."],
            ["Token en variable de entorno", "Evita secretos en código, logs o Git y permite rotación."],
            ["Módulos y pruebas", "Mejoran mantenimiento, reutilización y confiabilidad."],
            ["Validación por registro", "Conserva datos válidos e informa inconsistencias sin detener el proceso."],
            ["Permisos 750/640", "Aplica mínimo privilegio al proyecto y datos de inventario."],
        ], colWidths=[5.2 * cm, 11.1 * cm], repeatRows=1, style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12355B")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"), ("PADDING", (0, 0), (-1, -1), 6),
        ])),
        PageBreak(), paragraph("Linux, Git y buenas prácticas", heading),
        paragraph("En DEVASC VM se administran usuario, grupo y permisos con useradd, groupadd, usermod, mkdir, chmod y chown. Git se organiza con ramas feature/inventory-api y docs/technical-report, commits descriptivos, pruebas antes de cada commit y fusiones revisadas a main. El código incorpora tipado, docstrings, funciones acotadas, manejo de excepciones y .gitignore para secretos y artefactos locales.", body),
        paragraph("Diagnóstico REST API", heading),
        Table([
            ["Respuesta", "Diagnóstico y solución"],
            ["400", "Validar parámetros, tipos y payload con el contrato del servicio."],
            ["401", "Revisar o renovar token y verificar la variable de entorno."],
            ["403 / 429", "Revisar scope o rate limit; respetar Retry-After y aplicar backoff."],
            ["404", "Confirmar endpoint, método y versión de la API."],
            ["5xx / timeout", "Reintentar con backoff, inspeccionar logs y escalar si persiste."],
        ], colWidths=[3.1 * cm, 13.2 * cm], repeatRows=1, style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#12355B")), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("PADDING", (0, 0), (-1, -1), 6),
        ])),
        paragraph("Evidencias", heading),
        paragraph("Insertar capturas reales de DEVASC VM: usuario/grupo/permisos, ejecución de JSON, CSV, XML y YAML, pruebas unitarias, historial y ramas Git, solicitud HTTPS autorizada y un diagnóstico de error. No incluir tokens ni datos sensibles.", body),
        paragraph("Conclusiones", heading),
        paragraph("La automatización entrega inventarios validados y trazables. HTTPS, secretos externos, permisos mínimos, validación y reintentos fortalecen seguridad y confiabilidad. La arquitectura modular y las pruebas habilitan su evolución hacia controladores de red reales, OAuth 2.0, CI/CD y auditoría centralizada.", body),
    ]
    document.build(flow)


if __name__ == "__main__":
    build_pdf()
