# Actividad: política de memoria para un agente conversacional

## Propósito

Diseñar una política de memoria para el asistente de políticas de viajes,
aplicando ámbitos, namespaces, estrategias de corto y largo plazo,
recuperación relevante e integración con LangGraph. El ejercicio debe
demostrar cómo se evita mezclar información entre usuarios y cómo se responde
cuando la memoria está ausente, obsoleta o indisponible.

## Caso de aplicación

Continúa el caso de los capítulos anteriores. El asistente conversa con
empleados sobre políticas de viajes. Puede recordar el idioma preferido, un
formato de respuesta solicitado y un resumen de una conversación anterior. No
debe conservar credenciales, números completos de documentos, secretos ni
información que no sea necesaria para el servicio.

El agente utiliza LangGraph para orquestar el flujo y AgentCore Memory para
registrar eventos y recuperar información entre sesiones. El diseño es
conceptual: no requiere crear un recurso real ni escribir datos personales.

## Entregable

Crea un documento Markdown llamado
`politica-memoria-agentcore.md` dentro de
`course/entregas/capitulo-4/`.

Debe incluir:

1. Un diagrama del flujo de lectura y escritura de memoria.
2. Una tabla que explique Memory ID, Actor ID y Session ID.
3. Un catálogo de namespaces y tipos de información permitidos.
4. Una clasificación de memoria de corto y largo plazo.
5. Estrategias para eventos, resúmenes, preferencias y memoria semántica.
6. Un flujo de integración con el estado de LangGraph.
7. Reglas de aislamiento, retención, corrección y eliminación.
8. Matriz de fallos y comportamiento esperado.
9. Pruebas de aislamiento entre dos usuarios y dos sesiones.
10. Supuestos, límites y preguntas abiertas.

## Pasos

1. Define un Memory ID separado para el entorno de aprendizaje y explica por
   qué no debe mezclarse con producción.
2. Define cómo se generan y validan Actor ID y Session ID. Indica qué parte
   proviene de la identidad autenticada y qué parte identifica la conversación.
3. Diseña al menos tres namespaces: preferencias, resumen de sesión y hechos
   de dominio. Para cada uno, indica contenido permitido y excluido.
4. Decide qué eventos se registran siempre, cuáles se resumen y cuáles no se
   persisten.
5. Define una regla para convertir una afirmación en preferencia o memoria
   semántica, incluyendo fuente, vigencia y posibilidad de corrección.
6. Describe cómo se recuperan recuerdos antes de ejecutar LangGraph y cómo se
   incorporan al estado sin reemplazar instrucciones ni controles.
7. Describe cómo se registran nuevos eventos después de la respuesta.
8. Define el comportamiento si Memory no responde, devuelve un recuerdo
   contradictorio o no encuentra información.
9. Especifica retención, eliminación y corrección para datos obsoletos o
   incorrectos.
10. Diseña pruebas con usuario A y usuario B, cada uno con dos sesiones, y
    prueba identificadores manipulados y namespaces no autorizados.

## Tabla mínima de decisión

Incluye una tabla con columnas equivalentes a:

| Dato | Nivel | Namespace | Fuente | Retención | Puede recuperarse cuando | Riesgo |
|---|---|---|---|---|---|---|
| Preferencia de idioma | Largo plazo | Preferencias | Confirmación del usuario | Definida | Usuario autenticado | Preferencia obsoleta |
| Resumen de conversación | Sesión o largo plazo | Resumen | Conversación | Definida | Mismo actor | Omisión o distorsión |
| Credencial o secreto | No persistir | Ninguno | Entrada del usuario | Cero | Nunca | Exposición |

Puedes añadir otros datos, pero cada fila debe justificar su decisión.

## Matriz mínima de pruebas

Incluye al menos estos casos:

| Caso | Resultado esperado |
|---|---|
| Lectura con actor y sesión válidos | Solo se recupera información autorizada |
| Usuario A consulta memoria de B | Solicitud rechazada o resultado vacío controlado |
| Sesión A1 consulta sesión A2 | Solo ocurre si la política lo permite |
| Namespace no autorizado | No se recuperan sus datos |
| Recuerdo obsoleto | Se marca, filtra o solicita confirmación |
| Recuerdos contradictorios | El agente no elige silenciosamente una versión |
| Memory indisponible | Comportamiento documentado, sin éxito falso |
| Evento con secreto | Se elimina o rechaza antes de persistir |
| Preferencia corregida | La nueva versión tiene prioridad según la regla |
| Recuperación irrelevante | No se incorpora al contexto del agente |

## Criterios de aceptación

- El entregable diferencia estado de invocación, sesión y memoria persistente.
- Memory ID, Actor ID y Session ID tienen significado y validación explícitos.
- Los namespaces separan propósitos y no se usan como única frontera de
  seguridad.
- Se cubren eventos, conversaciones, memoria corta y larga.
- Se explican estrategias para resúmenes, preferencias y memoria semántica.
- El flujo LangGraph distingue memoria recuperada de instrucciones y datos
  actuales.
- Existe una política explícita para ausencia, contradicción, obsolescencia y
  caída de Memory.
- Se incluyen retención, corrección y eliminación.
- Las pruebas incluyen aislamiento de usuarios y sesiones.
- El diseño excluye secretos y datos innecesarios.
- Las reglas permiten que otra persona implemente el flujo sin inventar
  identificadores o ámbitos.

## Resultado esperado

El resultado es una política de memoria revisable por los equipos de
aplicación, seguridad y privacidad. Debe explicar qué se conserva, dónde,
durante cuánto tiempo, quién puede recuperarlo y cómo se evita que un recuerdo
incorrecto afecte al agente.

## Preguntas abiertas y límites

- ¿Qué requisitos de retención y eliminación aplican a las conversaciones?
- ¿Qué datos puede confirmar el usuario como preferencia persistente?
- ¿Qué debe suceder si la memoria es necesaria para autorizar una acción?
- ¿Qué nivel de confianza exige una memoria semántica antes de usarla?
- ¿Cómo se auditarán correcciones y eliminaciones sin exponer el contenido?
- ¿Qué campos deben enmascararse antes de registrar eventos?

Queda fuera de esta actividad seleccionar una estrategia productiva concreta
sin verificar la configuración disponible, crear recursos reales, definir
políticas de identidad del siguiente capítulo y construir un sistema completo
de cumplimiento o retención legal.
