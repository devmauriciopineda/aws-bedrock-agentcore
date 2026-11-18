# Actividad: proyecto integrador de AgentCore

## Propósito

Diseñar un paquete de arquitectura y operación para el asistente de políticas
de viajes, integrando los componentes del curso y demostrando que la solución
puede validarse, observarse, actualizarse y limpiarse de forma controlada.

## Caso de aplicación

Construye sobre el caso anterior:

- backend Python con LangGraph;
- ejecución en AgentCore Runtime;
- inferencia mediante Amazon Bedrock;
- herramientas remotas mediante Gateway y MCP;
- memoria conversacional y persistente;
- identidad del cliente e identidad outbound;
- políticas que permiten consultas y bloquean modificaciones;
- observabilidad y evaluaciones.

El entregable es un diseño ejecutable como runbook. Puede usar datos,
respuestas y métricas sintéticas. No requiere desplegar recursos reales ni
incluir credenciales.

## Entregable

Crea un documento Markdown llamado
`proyecto-integrador-agentcore.md` dentro de
`course/entregas/capitulo-6/`.

Debe incluir:

1. Arquitectura de referencia con diagrama.
2. Flujo de una solicitud exitosa y flujos de error.
3. Tabla de componentes, responsabilidades y contratos.
4. Integración de LangGraph, Gateway, MCP y Memory.
5. Matriz de identidades y políticas.
6. Diseño de observabilidad y evaluación.
7. Plan de versionamiento, promoción y rollback.
8. Estrategia de errores, reintentos, latencia y concurrencia.
9. Análisis de consumo y costes con supuestos explícitos.
10. Runbook de limpieza de recursos de prueba.
11. Checklist final de puesta en producción.

## Pasos

1. Define la frontera del sistema y separa cliente, backend Python, Runtime,
   Bedrock, Memory, Gateway, targets, identidades y señales.
2. Dibuja el flujo de una solicitud desde autenticación hasta respuesta,
   indicando dónde se aplican políticas y dónde se registran spans.
3. Relaciona cada componente con una responsabilidad, una entrada, una salida,
   un propietario y un comportamiento ante fallo.
4. Integra conceptualmente LangGraph: entrada, recuperación de memoria,
   decisión de herramienta, resultado remoto y respuesta.
5. Selecciona las herramientas del capítulo 3 y limita el catálogo a las
   operaciones necesarias.
6. Aplica la política de memoria del capítulo 4: Actor ID, Session ID,
   namespaces, retención y aislamiento.
7. Aplica el paquete de control del capítulo 5: identidad inbound/outbound,
   políticas, logs, métricas, trazas y evaluaciones.
8. Define una versión inicial, un cambio compatible y un cambio incompatible.
   Documenta promoción, comparación y rollback.
9. Clasifica fallos y decide cuándo reintentar, degradar, denegar, alertar o
   detener la solicitud.
10. Estima consumo por invocación y por volumen mensual, indicando qué valores
    son supuestos y qué debe medirse.
11. Escribe el procedimiento de limpieza y verifica que no elimine recursos
    compartidos o productivos.
12. Completa el checklist final y marca cada evidencia como pendiente,
    simulada o validada.

## Tabla mínima de integración

Incluye una tabla con columnas equivalentes a:

| Componente | Responsabilidad | Entrada | Salida | Identidad | Observabilidad | Fallo |
|---|---|---|---|---|---|---|
| Runtime | Ejecutar agente | Payload validado | Respuesta | Workload | Traza y latencia | Timeout |
| Bedrock | Inferencia | Contexto permitido | Resultado del modelo | Outbound | Tokens y duración | Error de servicio |
| Gateway | Herramientas | Nombre y argumentos | Resultado normalizado | Outbound | Target y error | Rechazo o timeout |
| Memory | Contexto persistente | Eventos o consulta | Recuerdos | Actor/sesión | Lectura y escritura | Degradación definida |

Añade LangGraph, Identity, Policy, Evaluations y el backend Python.

## Matriz mínima de escenarios

Incluye al menos estos escenarios:

| Escenario | Comportamiento esperado |
|---|---|
| Consulta válida con memoria | Respuesta con contexto del actor correcto |
| Herramienta remota exitosa | Resultado validado e incorporado al grafo |
| Herramienta no autorizada | Denegación observable sin reintento |
| Memory indisponible | Degradación documentada o bloqueo según riesgo |
| Modelo lento | Timeout clasificado y respuesta no engañosa |
| Dos sesiones concurrentes | Estado y memoria aislados |
| Nueva versión compatible | Promoción tras pruebas y evaluación |
| Nueva versión incompatible | Migración, nueva ruta o bloqueo |
| Error transitorio | Reintento limitado si es idempotente |
| Coste por encima del umbral | Alerta y revisión de configuración |

## Análisis mínimo de costes y capacidad

Documenta una fórmula o tabla que incluya:

- invocaciones por periodo;
- tokens o consumo de inferencia estimado;
- llamadas promedio a herramientas;
- lecturas y escrituras de Memory;
- volumen de logs, métricas y trazas;
- frecuencia de evaluaciones online y bajo demanda;
- concurrencia normal y pico;
- supuestos de latencia y timeout;
- alertas o umbrales de presupuesto.

No inventes precios actuales como hechos. Si usas valores de ejemplo,
identifícalos como supuestos y deja la fuente o verificación pendiente.

## Criterios de aceptación

- El diagrama integra backend Python, Runtime, Gateway, Memory, Identity,
  Policy, Amazon Bedrock, LangGraph y observabilidad.
- Se muestran herramientas remotas mediante Gateway y MCP.
- El flujo diferencia identidad del cliente, identidad del agente y
  credenciales outbound.
- La memoria se recupera y persiste con aislamiento por actor y sesión.
- Las políticas permiten operaciones necesarias y bloquean acciones sensibles.
- Existen logs, métricas, trazas y evaluaciones con datos minimizados.
- Runtime, Gateway, Memory, inferencia y herramientas tienen errores
  clasificados.
- Se definen timeouts, reintentos, idempotencia, degradación y concurrencia.
- El versionamiento incluye promoción y rollback.
- El análisis de costes separa hechos, supuestos y mediciones pendientes.
- El runbook de limpieza tiene alcance seguro y verificación posterior.
- Cada punto del checklist tiene evidencia pendiente, simulada o validada.
- El documento no contiene secretos, credenciales ni instrucciones destructivas
  sin alcance explícito.

## Resultado esperado

El resultado es un paquete final que permite a otra persona entender cómo
construir, validar y operar el asistente sin depender de conocimiento tácito.
Debe ser suficientemente concreto para guiar una implementación de prueba y
conservar límites claros para que la promoción a producción requiera
aprobaciones y evidencias reales.

## Preguntas abiertas y límites

- ¿Qué requisitos de disponibilidad y recuperación aplican al caso real?
- ¿Qué modelo, región y límites de servicio deben verificarse?
- ¿Qué operaciones requieren aprobación humana?
- ¿Qué políticas de retención y eliminación aplican a Memory y logs?
- ¿Qué volumen de tráfico y concurrencia debe soportar el primer release?
- ¿Qué métricas determinan que una versión puede promoverse?
- ¿Quién puede ejecutar rollback y limpieza?
- ¿Qué evidencias faltan para considerar la arquitectura lista para producción?

Queda fuera de esta actividad crear recursos reales sin autorización, registrar
credenciales, fijar precios sin fuente actualizada y declarar cumplimiento
productivo o legal sin revisión de los responsables correspondientes.
