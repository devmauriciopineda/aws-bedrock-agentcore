# Actividad: control, observabilidad y evaluación de un agente

## Propósito

Diseñar un paquete de control operativo para el asistente de políticas de
viajes. El ejercicio aplica identidad inbound y outbound, autorización de
herramientas, instrumentación con logs, métricas y trazas, además de
evaluaciones bajo demanda y online.

## Caso de aplicación

Continúa el caso de los capítulos anteriores. El asistente puede consultar
políticas, revisar el estado de solicitudes y calcular viáticos mediante las
herramientas definidas en el capítulo 3. Memory conserva preferencias y
resúmenes según la política del capítulo 4.

El asistente no debe modificar solicitudes ni aprobar gastos. El diseño debe
distinguir la identidad del empleado que consulta de la identidad técnica del
agente. El ejercicio es conceptual y puede ejecutarse con datos sintéticos.

## Entregable

Crea un documento Markdown llamado
`paquete-control-observabilidad-evaluacion.md` dentro de
`course/entregas/capitulo-5/`.

Debe incluir:

1. Diagrama de identidades inbound y outbound.
2. Matriz de autenticación y autorización.
3. Reglas de AgentCore Policy para herramientas permitidas y denegadas.
4. Diseño de logs, métricas y trazas sin secretos.
5. Flujo de diagnóstico con correlación de sesión y versión.
6. Plan de evaluación bajo demanda.
7. Plan de evaluación online.
8. Métricas de calidad, herramientas y resultados operativos.
9. Matriz de fallos y respuesta esperada.
10. Supuestos, límites y preguntas abiertas.

## Pasos

1. Define qué identidad representa al empleado y cuál representa al workload
   del agente. Explica por qué no son automáticamente la misma credencial.
2. Selecciona un mecanismo conceptual para cada frontera: OAuth, API key,
   identidad administrada, rol u otro. Justifica expiración, rotación y
   alcance.
3. Clasifica las tres herramientas del caso por lectura, cálculo o posible
   efecto secundario.
4. Escribe políticas deterministas que permitan las consultas necesarias y
   denieguen modificaciones o accesos fuera del dominio.
5. Define qué ocurre si falta identidad, el token expiró o una política no
   puede evaluarse.
6. Diseña un log de ejemplo sin credenciales ni contenido sensible, una
   métrica agregada y una traza con spans para Runtime, modelo, Memory y
   Gateway.
7. Define campos de correlación, versión y componente para diagnosticar una
   respuesta lenta o incorrecta.
8. Crea un conjunto sintético de interacciones para evaluación bajo demanda,
   incluyendo casos normales, ambiguos, rechazados y con herramienta
   indisponible.
9. Define una evaluación online: muestreo, métricas, privacidad, alertas y
   acción ante degradación.
10. Relaciona cada fallo con su señal y su respuesta: reintentar, denegar,
    degradar, alertar o revisar manualmente.

## Matrices mínimas

### Identidad y política

| Situación | Identidad | Acción | Decisión esperada | Evidencia |
|---|---|---|---|---|
| Empleado consulta política | Cliente autenticado | Lectura | Permitir | Correlación y resultado |
| Agente consulta API | Identidad outbound | Lectura limitada | Permitir | Target y versión |
| Agente intenta modificar solicitud | Identidad outbound | Escritura | Denegar | Decisión de política |
| Token inbound expirado | No válida | Cualquier operación | Denegar | Error de autenticación |
| Herramienta fuera del dominio | Válida pero sin alcance | Lectura | Denegar | Regla aplicada |

### Observabilidad y evaluación

| Señal o evaluación | Qué mide | Datos permitidos | Acción |
|---|---|---|---|
| Latencia por componente | Tiempo de Runtime, modelo, Memory y Gateway | IDs técnicos y versión | Alertar si supera umbral |
| Tasa de errores | Fallos clasificados | Código y componente | Investigar tendencia |
| Calidad de respuesta | Exactitud y relevancia | Interacción sintética o protegida | Comparar versiones |
| Uso de herramientas | Selección y argumentos válidos | Nombre y resultado clasificado | Revisar regresiones |
| Seguridad | Acciones no autorizadas o filtraciones | Evento minimizado | Bloquear y revisar |

## Matriz mínima de fallos

Incluye al menos estos casos:

| Caso | Respuesta esperada |
|---|---|
| Credencial outbound inválida | No llamar al backend; registrar error clasificado |
| Política deniega herramienta | Devolver rechazo controlado y no reintentar |
| Modelo lento | Registrar spans, aplicar timeout y clasificar resultado |
| Memory indisponible | Aplicar degradación definida en el capítulo 4 |
| Gateway con timeout | Reintentar solo si la operación es segura |
| Respuesta de baja calidad | Marcar evaluación y conservar evidencia mínima |
| Evaluación online degradada | Alertar o muestrear, sin ocultar el problema |
| Log contiene secreto | Corregir instrumentación y tratar como incidente |

## Criterios de aceptación

- Se diferencian identidad inbound, identidad outbound y credenciales.
- OAuth, API keys o identidades administradas se justifican por frontera y
  riesgo; no se incluyen secretos reales.
- Las políticas permiten consultas necesarias y bloquean modificaciones.
- Logs, métricas y trazas tienen propósito, correlación y minimización de
  datos.
- El diseño menciona CloudWatch y OpenTelemetry.
- La traza incluye Runtime, inferencia, Memory y Gateway o herramienta.
- Se explica cómo diagnosticar latencia y errores por componente.
- El plan incluye evaluación bajo demanda y online.
- Las métricas cubren calidad, uso de herramientas y resultados operativos.
- La matriz contempla autenticación, autorización, timeouts, memoria,
  evaluación y filtración de secretos.
- Cada decisión de bloqueo, reintento, degradación o alerta es observable.
- El documento permite revisar una versión del agente sin depender de datos
  personales.

## Resultado esperado

El resultado es un paquete que un equipo puede revisar antes de operar el
agente. Debe dejar claro quién puede hacer qué, qué evidencia se conserva,
cómo se diagnostica una ejecución y cómo se detecta una regresión de calidad
sin convertir la observabilidad en una fuente de exposición de datos.

## Preguntas abiertas y límites

- ¿Qué proveedor emite los tokens inbound y qué scopes son necesarios?
- ¿Qué identidad outbound debe usar cada target?
- ¿Qué operaciones requieren aprobación humana?
- ¿Qué datos pueden aparecer en logs, trazas y conjuntos de evaluación?
- ¿Qué umbrales de latencia, error y calidad activan alertas?
- ¿Qué muestra mínima representa adecuadamente el tráfico online?
- ¿Quién puede consultar la evidencia y durante cuánto tiempo?

Queda fuera de esta actividad crear credenciales, activar políticas en una
cuenta real, configurar dashboards productivos y definir requisitos legales
definitivos. Esos elementos requieren validación con los responsables de
seguridad, plataforma y cumplimiento.
