# Actividad: catálogo seguro de herramientas con Gateway

## Propósito

Diseñar un catálogo de herramientas para el asistente de políticas de viajes,
definir sus contratos y preparar su consumo desde Python y LangGraph mediante
AgentCore Gateway. El ejercicio aplica descubrimiento, targets, autenticación,
autorización, errores, dominios y versionamiento sin exigir un despliegue
productivo.

## Caso de aplicación

Continúa el caso de los capítulos anteriores. El asistente interno necesita:

1. Consultar una política de viajes por país o región.
2. Buscar el estado de una solicitud de viaje.
3. Proponer un cálculo de viáticos sin modificar registros.

La primera capacidad está disponible como API REST, la segunda como función
Lambda y la tercera como servidor MCP existente. Las implementaciones son
hipotéticas: documenta contratos y decisiones sin inventar URLs, nombres de
cuentas, secretos ni permisos concretos no verificados.

## Entregable

Crea un documento Markdown llamado
`catalogo-herramientas-gateway.md` dentro de
`course/entregas/capitulo-3/`.

Debe incluir:

1. Un diagrama del recorrido agente -> Gateway -> target -> backend.
2. Un catálogo con las tres herramientas del caso.
3. Esquemas de entrada y salida para cada herramienta.
4. Target y backend correspondiente.
5. Identidad, autenticación y autorización por dominio.
6. Matriz de errores, reintentos e idempotencia.
7. Adaptación conceptual para consumo desde Python y LangGraph.
8. Estrategia de versionamiento y retirada.
9. Decisión sobre qué herramientas quedan disponibles para este agente.
10. Supuestos, límites y preguntas pendientes.

## Pasos

1. Define nombres y descripciones que permitan descubrir cada herramienta sin
   ambigüedad.
2. Especifica campos obligatorios, tipos, unidades y restricciones de entrada.
3. Define una respuesta exitosa y errores distinguibles para cada operación.
4. Explica cómo se transforma cada backend en un target de Gateway:
   API REST, Lambda y servidor MCP.
5. Distingue la identidad que invoca Gateway de la identidad que usa cada
   target para acceder al backend.
6. Asigna cada herramienta a un dominio funcional y limita el catálogo del
   asistente a las operaciones estrictamente necesarias.
7. Describe cómo el cliente Python descubre o configura las herramientas,
   valida argumentos, invoca y normaliza resultados.
8. Explica cómo un nodo de LangGraph recibiría el resultado o error sin
   incorporar URL, secretos ni detalles del backend.
9. Define qué fallos se reintentan y cuáles se devuelven inmediatamente.
10. Propón una versión inicial y un cambio incompatible; documenta cómo se
    publicarían, probarían y retirarían.

## Estructura mínima del catálogo

Usa una tabla con columnas equivalentes a:

| Campo | Qué debe describir |
|---|---|
| Herramienta | Nombre estable y propósito |
| Dominio | Área funcional responsable |
| Target | Tipo de integración y destino lógico |
| Entrada | Campos, tipos y restricciones |
| Salida | Datos devueltos y formato |
| Efecto | Solo lectura o efecto secundario |
| Identidad | Quién invoca y quién accede al backend |
| Errores | Validación, autorización, transitorio y backend |
| Versión | Versión publicada y compatibilidad |

## Matriz mínima de pruebas

Incluye al menos estos casos:

| Caso | Resultado esperado |
|---|---|
| Descubrimiento del catálogo | Solo aparecen herramientas permitidas |
| Argumento obligatorio ausente | La llamada se rechaza antes del backend |
| Tipo o unidad inválida | Se devuelve error de validación claro |
| Identidad sin permiso | La operación se rechaza sin reintento |
| API REST lenta | Se aplica timeout y solo se reintenta si corresponde |
| Lambda con error transitorio | Se clasifica y limita el reintento |
| Servidor MCP incompatible | Se detecta incompatibilidad, no se oculta |
| Resultado vacío | El agente distingue ausencia de datos de error |
| Herramienta con efecto | Se identifica el riesgo y la autorización adicional |
| Versión incompatible | Se mantiene la versión anterior o se bloquea promoción |

## Criterios de aceptación

- El catálogo cubre las tres herramientas y sus tres tipos de backend.
- Cada herramienta tiene propósito, dominio, entrada, salida y efecto
  explícitos.
- El diagrama muestra Gateway, targets y backends.
- Se distinguen autenticación y autorización.
- Se separan las identidades de invocación y de acceso al backend.
- El catálogo limita herramientas por dominio y mínimo privilegio.
- Se explican descubrimiento e invocación desde Python.
- Se describe la conversión de resultados y errores para LangGraph.
- La matriz contempla validación, autorización, timeout, reintentos,
  incompatibilidad y versionamiento.
- Se documenta al menos un cambio compatible y uno incompatible.
- No se incluyen credenciales, URLs reales ni permisos no verificados como si
  fueran definitivos.
- El documento identifica qué decisiones requieren validación con los dueños de
  cada backend.

## Resultado esperado

El resultado es un catálogo revisable por los equipos de aplicación,
seguridad y backend. Debe permitir responder qué puede hacer cada herramienta,
quién puede invocarla, qué sistema la implementa, cómo falla y cómo cambiará
sin romper agentes existentes.

## Preguntas abiertas y límites

- ¿Qué identidad debe propagarse desde el usuario al backend?
- ¿Qué datos de la API de políticas pueden enviarse al modelo?
- ¿Qué operación del servidor MCP tiene efectos secundarios, si existe alguna?
- ¿Qué herramientas deben requerir aprobación adicional?
- ¿Qué latencia máxima tolera el agente antes de elegir una respuesta
  alternativa?
- ¿Qué versión mínima de cada backend debe soportarse?

Queda fuera de esta actividad desplegar Gateway, crear la función Lambda,
implementar el servidor MCP, configurar secretos reales y construir políticas
productivas. La actividad produce diseño y criterios de validación, no una
integración autorizada en una cuenta real.
