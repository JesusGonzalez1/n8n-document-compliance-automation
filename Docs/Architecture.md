# Arquitectura

## Entrada

El workflow recibe un identificador empresarial mediante un formulario de n8n.

## Integraciones

- API de consulta de reportes.
- API de descarga de documentos.
- Google Gemini para análisis documental.
- Google Sheets para persistencia de resultados.

## Procesamiento

Los casos se clasifican y las preguntas aplicables se procesan mediante ciclos.
Cada documento se convierte en archivo binario PDF antes de enviarse al modelo.

## Salida

Cada resultado incluye:

- Identificador de pregunta.
- Pregunta evaluada.
- Correspondencia del documento.
- Cumplimiento.
- Observación.
- Estado de revisión manual.
- Fecha de procesamiento.

## Decisiones técnicas

- Procesamiento por lotes para controlar llamadas externas.
- Reintentos en servicios con posibles fallos temporales.
- Separación entre configuración, procesamiento y persistencia.
- Respuesta estructurada para reducir ambigüedad.
- Datos sintéticos en la versión pública.