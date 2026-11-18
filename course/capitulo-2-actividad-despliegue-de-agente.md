# Actividad: adaptar y preparar un agente para Runtime

## Propósito

Construir un artefacto de despliegue reproducible para un agente Python
pequeño, aplicando contrato de entrada y salida, sesiones, manejo de errores,
versionamiento y validación de invocaciones. La actividad puede realizarse
localmente y deja preparada una ruta clara para un despliegue de prueba en
AgentCore Runtime.

## Caso de aplicación

Continúa el caso del capítulo 1: un asistente interno responde preguntas sobre
políticas de viajes. Para concentrar el trabajo en Runtime, el agente de esta
actividad puede usar una respuesta simulada o una función local de consulta.
No es necesario conectar todavía una API real, AgentCore Gateway, Memory ni
políticas avanzadas.

El agente debe aceptar una pregunta, un identificador de sesión y metadata
opcional. Debe devolver una respuesta estructurada, el mismo identificador de
sesión y un estado explícito.

## Entregable

Crea un documento Markdown llamado
`runbook-despliegue-runtime.md` dentro de
`course/entregas/capitulo-2/`.

El documento debe incluir, como mínimo:

1. El contrato de entrada y salida en JSON.
2. La responsabilidad del entrypoint y su relación con el flujo del agente.
3. Una tabla de casos correctos, entradas inválidas y errores operativos.
4. Una estrategia de aislamiento de sesiones.
5. Una estrategia de versionamiento y actualización del endpoint.
6. Un flujo de construcción, publicación en ECR e invocación desde Python.
7. Una matriz de pruebas y sus resultados esperados.
8. Una lista explícita de supuestos, límites y elementos fuera de alcance.

Si el entorno de práctica está configurado, complementa el documento con
evidencia de una invocación local o de prueba. No incluyas credenciales,
tokens ni payloads sensibles.

## Pasos

1. Define un payload de entrada con `input`, `session_id` y un campo opcional
   de metadata. Especifica tipos, obligatoriedad y límites razonables.
2. Define una respuesta para éxito y otra para error. Incluye un estado
   explícito y evita exponer excepciones internas.
3. Describe cómo `BedrockAgentCoreApp` y `@app.entrypoint` conectan Runtime
   con el agente Python.
4. Explica cómo el adaptador convierte el payload en el estado inicial de
   LangGraph, o en la entrada del agente simulado si no utilizas LangGraph.
5. Define qué ocurre si falta `session_id`, si `input` está vacío o si el
   agente supera el timeout.
6. Describe una prueba con dos sesiones distintas y demuestra qué datos no
   deben cruzarse.
7. Especifica una convención de versión para la imagen y para el endpoint.
   Incluye qué condición debe cumplirse antes de promover una versión.
8. Documenta el flujo conceptual de `build -> test -> tag -> push -> deploy ->
   invoke`, indicando qué información debe configurarse en cada etapa.
9. Describe el cliente Boto3: configuración de región e identidad, timeout,
   validación de respuesta, clasificación de errores y política de reintentos.
10. Completa la matriz de pruebas con casos positivos, negativos, concurrencia
    y actualización de versión.

## Matriz mínima de pruebas

Incluye al menos estos casos:

| Caso | Entrada o condición | Resultado esperado |
|---|---|---|
| Solicitud válida | `input` y `session_id` válidos | Respuesta estructurada con estado de éxito |
| Entrada incompleta | Falta `input` o `session_id` | Error de validación explícito |
| Entrada vacía | `input` vacío o solo espacios | Solicitud rechazada sin ejecutar el flujo |
| Sesiones aisladas | Dos sesiones con preguntas diferentes | Cada respuesta conserva su propia sesión |
| Timeout | Ejecución más lenta que el límite acordado | Error clasificable y sin éxito falso |
| Respuesta no serializable | El agente produce un objeto no válido | Error del adaptador, sin respuesta ambigua |
| Nueva versión | Endpoint apunta a una imagen versionada | Promoción solo después de pruebas exitosas |

## Criterios de aceptación

- El entregable contiene contratos JSON de entrada, éxito y error.
- Cada campo del contrato tiene tipo, propósito y regla de validación.
- El flujo distingue payload de transporte, estado interno del agente y
  respuesta externa.
- Se explica cómo se evita compartir estado entre sesiones.
- Se documentan al menos una invocación síncrona y la diferencia frente a
  asíncrona y streaming.
- El procedimiento incluye construcción de contenedor, publicación en ECR,
  configuración de Runtime e invocación con Boto3.
- La estrategia de versionamiento permite identificar y revertir una versión.
- La matriz incluye los siete casos mínimos o equivalentes verificables.
- Los errores no se presentan como respuestas exitosas ni exponen secretos.
- Se explican timeout, concurrencia, límites y reintentos.
- El documento indica qué partes se simulan y qué partes quedarían pendientes
  para un entorno AWS real.

## Resultado esperado

El resultado es un runbook ejecutable por otra persona del equipo: debe poder
entender qué recibe el agente, qué devuelve, cómo se prueba, cómo se empaqueta
y qué debe verificarse antes de promover una versión. Si se dispone de un
entorno AWS autorizado, el runbook también sirve como checklist para una
invocación de prueba.

## Preguntas abiertas y límites

- ¿Qué modalidad requiere el caso real: síncrona, asíncrona o streaming?
- ¿Cuál es el timeout aceptable para el usuario y para cada dependencia?
- ¿Qué datos de sesión deben persistir y cuáles deben descartarse?
- ¿La operación es idempotente si el cliente reintenta?
- ¿Qué cuota de concurrencia y tamaño de payload aplica al entorno elegido?
- ¿Cómo se hará rollback si una nueva versión cambia el contrato?

Queda fuera de esta actividad integrar herramientas remotas mediante Gateway,
persistir memoria con AgentCore Memory, aplicar políticas de autorización
avanzadas y operar un endpoint productivo. También queda fuera incluir
credenciales reales o automatizar una cuenta de AWS sin autorización expresa.
