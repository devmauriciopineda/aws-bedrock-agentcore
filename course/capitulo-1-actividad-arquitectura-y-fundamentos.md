# Actividad: mapa arquitectónico de AgentCore

## Propósito

Aplicar los conceptos del capítulo para analizar una solución de agente,
separar responsabilidades y detectar decisiones de seguridad y operación
antes de implementar.

## Caso de aplicación

Una empresa quiere construir un asistente interno para consultar políticas de
viajes. El asistente tendrá una aplicación Python con LangGraph, consultará
una API interna de políticas y podrá conservar preferencias conversacionales
del usuario. La solución debe ejecutarse en AWS, usar un modelo de Amazon
Bedrock y permitir que el equipo de operaciones diagnostique errores y latencia.

El caso es hipotético y no presupone que la API, las credenciales o los
recursos de AWS ya existan.

## Entregable

Crea un documento Markdown llamado
`mapa-arquitectonico-agentcore.md` dentro de
`course/entregas/capitulo-1/`.

El documento debe contener:

1. Un diagrama textual o Mermaid de la solución.
2. Una tabla que relacione cada necesidad con un componente de AgentCore.
3. Un apartado de identidades, permisos y separación entre plano de control y
   plano de ejecución.
4. Una lista de supuestos, riesgos y decisiones pendientes.
5. Una lista de verificaciones para preparar el entorno.

## Pasos

1. Describe en cinco líneas o menos qué hará el asistente y qué parte
   corresponde a LangGraph.
2. Dibuja el flujo desde la solicitud del usuario hasta la respuesta,
   incluyendo el modelo, la herramienta de políticas y la memoria.
3. Asigna responsabilidades a Runtime, Gateway, Memory, Identity, Policy,
   Observability y Evaluations.
4. Decide si Browser y Code Interpreter son necesarios para este caso. Justifica
   la decisión; no los habilites solo porque están disponibles.
5. Separa las operaciones de administración de recursos de las operaciones de
   ejecución del agente.
6. Propón dos identidades: una para administrar o preparar recursos y otra para
   ejecutar el agente. Indica qué tipo de acciones necesitaría cada una, sin
   inventar nombres concretos de permisos si no puedes verificarlos.
7. Define al menos tres señales de observabilidad: una métrica, un evento de
   log y una traza o span.
8. Propón dos criterios de evaluación del agente, por ejemplo exactitud de la
   respuesta y uso correcto de la herramienta.
9. Lista los datos que deben confirmarse antes de comenzar: región, acceso al
   modelo, configuración del SDK, configuración de la CLI y credenciales.
10. Identifica al menos un supuesto y un límite que deban validarse con el
    equipo responsable de la API interna.

## Criterios de aceptación

- El documento explica el papel de los siete componentes principales del
  capítulo: Runtime, Gateway, Memory, Identity, Policy, Observability y
  Evaluations.
- El flujo distingue la lógica de LangGraph de las capacidades administradas
  de AgentCore.
- El diagrama muestra como mínimo usuario, aplicación Python, Runtime,
  modelo, Gateway, herramienta de políticas y Memory.
- La tabla diferencia explícitamente plano de control y plano de ejecución.
- Se proponen identidades separadas para administración y ejecución.
- Se mencionan mínimo privilegio, región, credenciales y acceso al modelo.
- La propuesta incluye una métrica, un log, una traza o span y dos criterios de
  evaluación.
- Browser y Code Interpreter tienen una decisión justificada.
- Cada riesgo o decisión pendiente tiene una explicación breve.
- El entregable es Markdown, se puede leer sin archivos adicionales y no
  contiene secretos, claves ni credenciales reales.

## Resultado esperado

El resultado es un mapa inicial que permite explicar la arquitectura a otro
miembro del equipo y detectar qué debe definirse antes de desplegar. No se
espera todavía un agente funcional ni una configuración completa de AWS.

## Preguntas abiertas y límites

- ¿La API interna requiere autenticación del usuario, del agente o de ambos?
- ¿Qué información puede conservarse en Memory y durante cuánto tiempo?
- ¿Qué operaciones de la API son de solo lectura y cuáles podrían modificar
  datos?
- ¿Qué latencia máxima acepta el usuario para una respuesta?
- ¿Qué datos deben excluirse de logs y trazas?
- ¿Qué conjunto de interacciones se utilizará para evaluar el agente?

Queda fuera de esta actividad crear recursos reales, desplegar contenedores,
configurar un endpoint productivo, implementar la API interna y seleccionar
políticas concretas de producción. Esas tareas se abordarán cuando el plan
prepare sus respectivos conceptos.
