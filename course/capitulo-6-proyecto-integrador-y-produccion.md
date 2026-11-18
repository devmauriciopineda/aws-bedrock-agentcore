# Capítulo 6: Proyecto integrador y puesta en producción

## Propósito

Al finalizar este capítulo podrás diseñar una aplicación de referencia que
combine backend Python, LangGraph, Amazon Bedrock y las capacidades de
AgentCore estudiadas. También podrás definir un recorrido de operación que
incluya herramientas remotas, memoria, identidad, políticas,
observabilidad, evaluación, versionamiento, manejo de fallos, latencia,
concurrencia, costes y limpieza de recursos.

## 1. De componentes a sistema

Los capítulos anteriores estudiaron responsabilidades separadas. Un sistema
operable debe conectarlas mediante contratos claros:

```text
Cliente
  -> autenticación inbound
  -> Backend Python / LangGraph
      -> AgentCore Runtime
      -> Amazon Bedrock
      -> AgentCore Memory
      -> AgentCore Gateway -> MCP / REST / Lambda
      -> AgentCore Identity y Policy
      -> Observabilidad y Evaluations
```

El diagrama es una arquitectura lógica, no una lista de componentes que deban
habilitarse todos a la vez. Cada flecha debe tener una identidad, un contrato,
un timeout, una señal de observabilidad y un comportamiento ante error.

El backend Python contiene la lógica de aplicación y adapta el estado de
LangGraph al contrato de Runtime. Runtime ejecuta el agente; Bedrock aporta
inferencia; Gateway conecta herramientas; Memory conserva información
seleccionada; Identity y Policy controlan acceso; Observability explica el
comportamiento; Evaluations mide calidad y operación.

## 2. Arquitectura de referencia

Una arquitectura de referencia debe documentar como mínimo:

- entrada del usuario y autenticación;
- endpoint y versión de Runtime;
- punto de entrada del backend Python;
- estado y nodos de LangGraph;
- modelo y configuración de inferencia;
- herramientas remotas y targets de Gateway;
- Memory ID, Actor ID, Session ID y namespaces;
- identidades inbound y outbound;
- políticas permitidas y denegadas;
- logs, métricas y trazas;
- conjunto y modalidad de evaluaciones;
- límites, timeouts, reintentos y rollback.

Una **arquitectura de referencia** es un diseño reutilizable que muestra
relaciones y decisiones, pero no sustituye la configuración específica de una
cuenta, región, organización o requisito de cumplimiento.

## 3. Flujo completo de una solicitud

Un flujo normal puede seguir esta secuencia:

1. El cliente se autentica y envía una solicitud con sesión y contexto
   permitido.
2. Runtime recibe la invocación y asocia versión y correlación.
3. El entrypoint valida el payload y crea el estado inicial de LangGraph.
4. El agente recupera memoria relevante dentro del ámbito del actor.
5. LangGraph decide si necesita inferencia, una herramienta o una respuesta.
6. Identity y Policy autorizan cada llamada a un modelo o herramienta.
7. Gateway invoca el target remoto y devuelve un resultado normalizado.
8. El grafo produce una respuesta y clasifica errores o resultados parciales.
9. Memory registra eventos o actualiza recuerdos según la política.
10. Runtime devuelve la respuesta y Observability conserva señales mínimas.
11. Evaluations analiza la interacción según el modo configurado.

El flujo puede degradarse. Por ejemplo, si Memory no responde, la aplicación
puede continuar sin recuerdos para una consulta de bajo riesgo, pero impedir
una acción que necesite contexto confiable. La decisión debe estar
documentada, no quedar implícita en un catch genérico.

## 4. Integración de LangGraph

LangGraph coordina el estado y las transiciones del agente. En la solución
integrada, separa:

- **Estado de transporte:** payload recibido y respuesta externa.
- **Estado de sesión:** contexto de la conversación actual.
- **Estado del grafo:** nodos, mensajes y resultados de la invocación.
- **Memoria recuperada:** recuerdos identificados por fuente y ámbito.
- **Resultados de herramientas:** datos remotos y errores clasificados.

Un nodo no debe decidir por sí solo si una acción está autorizada. Puede
proponer una llamada; Identity, Policy, Gateway y el backend deben aplicar
controles. De igual manera, la memoria recuperada debe tratarse como dato
contextual y no como una orden que sobreescriba las instrucciones del sistema.

## 5. Herramientas remotas con Gateway y MCP

Gateway permite que el grafo consuma herramientas sin codificar URLs,
credenciales o detalles de implementación. MCP ofrece un contrato común para
descubrimiento y uso de herramientas.

Para cada herramienta documenta:

1. propósito y dominio;
2. esquema de entrada y salida;
3. target y backend;
4. identidad outbound;
5. regla de autorización;
6. timeout e idempotencia;
7. errores y reintentos;
8. versión y propietario.

Las herramientas de lectura suelen admitir reintentos limitados; una
operación con efectos secundarios necesita idempotencia y autorización
adicional. La selección del modelo no debe ser la única barrera frente a
acciones sensibles.

## 6. Memoria entre sesiones

La memoria debe recuperar solo información necesaria para la solicitud y el
actor correctos. Antes de leer, valida Memory ID, Actor ID, Session ID y
namespace. Antes de escribir, clasifica el evento, elimina secretos y decide
si merece persistir.

Un patrón de integración es:

```text
payload -> validar identidad y sesión
        -> recuperar memoria permitida
        -> ejecutar LangGraph
        -> filtrar respuesta
        -> registrar evento
        -> actualizar memoria seleccionada
```

La aplicación debe poder diferenciar ausencia de memoria, memoria obsoleta,
memoria contradictoria y fallo de servicio. No conviertas una recuperación
semánticamente parecida en un hecho confirmado sin validación.

## 7. Identidad, autorización y políticas

La solución debe separar:

- identidad del cliente que inicia la solicitud;
- identidad del workload que ejecuta el agente;
- identidad outbound que accede a cada target;
- permisos de administración del plano de control;
- permisos de ejecución del plano de ejecución.

Policy debe expresar qué herramientas puede utilizar cada identidad y en qué
condiciones. Los backends deben volver a validar autorización. Una denegación
debe ser segura, observable y no reintentarse como si fuera un timeout.

Para poner una solución en producción, revisa:

- rotación y expiración de credenciales;
- permisos mínimos;
- separación de entornos;
- protección de datos en logs y Memory;
- acceso del equipo a evidencias;
- procedimiento de revocación.

## 8. Observabilidad y evaluación integradas

Cada invocación debe conservar correlación, versión, sesión pseudonimizada y
resultado clasificado. Instrumenta spans para Runtime, inferencia, Memory,
Gateway y backend. Usa métricas agregadas para volumen, latencia, errores,
timeouts, uso de herramientas y coste.

CloudWatch y OpenTelemetry pueden formar parte de la arquitectura de señales,
pero la instrumentación debe responder preguntas operativas y minimizar
datos. No registres credenciales ni contenido completo por defecto.

Las evaluaciones deben ejecutarse sobre interacciones representativas y
versiones identificables:

- bajo demanda antes de promover un cambio;
- online con muestreo, privacidad y alertas durante la operación.

Mide calidad de respuesta, uso correcto de herramientas, cumplimiento de
políticas, errores y latencia. Un promedio global puede ocultar fallos en una
herramienta o en un dominio concreto; segmenta por versión y tipo de caso.

## 9. Versionamiento y actualización

Versiona al menos:

- código del backend;
- imagen de contenedor;
- contrato de entrada y salida;
- configuración del agente;
- herramientas y esquemas;
- prompts o plantillas relevantes;
- conjunto de evaluación;
- endpoint o referencia de despliegue.

Un **cambio compatible** conserva el contrato y el significado de las
operaciones. Un **cambio incompatible** modifica campos obligatorios,
semántica, permisos o formato de resultado. Los cambios incompatibles deben
publicarse como una nueva versión o acompañarse de una migración explícita.

Un recorrido seguro es:

1. construir una imagen identificable;
2. ejecutar pruebas de contrato y seguridad;
3. ejecutar evaluaciones bajo demanda;
4. desplegar a un entorno o endpoint de prueba;
5. realizar una invocación controlada;
6. comparar métricas con la versión anterior;
7. promover gradualmente;
8. conservar una ruta de rollback.

Rollback significa volver a una versión conocida, no simplemente reconstruir
el código actual. Conserva la imagen, configuración y evaluación asociadas a
esa versión.

## 10. Errores, reintentos y degradación

Clasifica fallos por frontera:

- validación de entrada;
- autenticación o autorización;
- inferencia;
- memoria;
- herramienta o backend;
- timeout;
- límite de cuota o concurrencia;
- serialización;
- evaluación u observabilidad.

Reintenta solo fallos transitorios y operaciones idempotentes. Usa límites,
backoff y un máximo de intentos. Un reintento no debe duplicar una operación
con efecto secundario.

La **degradación controlada** es una respuesta definida cuando una dependencia
no está disponible. Ejemplos: responder sin memoria para una consulta
informativa, omitir una herramienta opcional o devolver una respuesta
explícita de indisponibilidad. No es degradación ocultar un error como una
respuesta correcta.

## 11. Latencia y concurrencia

La latencia total depende de serialización, modelo, memoria, herramientas y
red. Mide cada componente antes de optimizar. Algunas acciones:

- limitar el contexto enviado al modelo;
- recuperar solo memoria relevante;
- reducir llamadas innecesarias a herramientas;
- establecer timeouts por dependencia;
- paralelizar operaciones independientes con límites;
- reutilizar conexiones cuando sea seguro;
- escoger modalidad síncrona, asíncrona o streaming según el caso.

La **concurrencia** es la cantidad de solicitudes activas simultáneamente.
Aumentarla sin controlar dependencias puede elevar errores y coste. Define
límites, backpressure, colas o respuestas de saturación, y prueba sesiones
aisladas bajo carga representativa.

## 12. Consumo y costes

El coste de una solución incluye inferencia, ejecución, almacenamiento de
memoria, llamadas de herramientas, observabilidad, evaluaciones y
transferencia o infraestructura asociada. El coste real depende de región,
modelo, volumen, configuración y uso.

Para analizar consumo:

1. identifica unidades medibles por invocación;
2. estima volumen normal y picos;
3. separa coste fijo y variable;
4. etiqueta recursos y versiones;
5. mide tokens, latencia, llamadas y evaluaciones;
6. define presupuestos y alertas;
7. revisa el coste de trazas y evaluaciones online.

No optimices coste eliminando señales necesarias o controles de seguridad.
Primero elimina llamadas innecesarias, contexto irrelevante y retención
excesiva, y valida que la calidad no se degrade.

## 13. Limpieza de recursos de prueba

Los entornos de aprendizaje pueden dejar imágenes, endpoints, logs, memoria y
otros recursos activos. La limpieza debe ser parte del runbook:

1. inventariar recursos creados por entorno y propietario;
2. identificar dependencias;
3. conservar evidencia necesaria;
4. deshabilitar tráfico;
5. eliminar endpoints y despliegues de prueba;
6. retirar imágenes y datos temporales según retención;
7. confirmar que no quedan credenciales o reglas temporales;
8. verificar costes después de la limpieza.

No borres recursos compartidos o productivos por coincidencia de nombre.
Requiere etiquetas, alcance explícito y confirmación de los responsables.

## Checklist de puesta en producción

Antes de promover la solución, verifica:

- contrato de Runtime documentado y probado;
- sesiones y Memory aisladas;
- herramientas catalogadas y versionadas;
- identidades y políticas de mínimo privilegio;
- secretos fuera de código e imágenes;
- logs, métricas y trazas sin exposición innecesaria;
- evaluaciones bajo demanda aprobadas;
- evaluación online y alertas definidas;
- timeouts, reintentos y degradación documentados;
- pruebas de concurrencia y límites realizadas;
- coste estimado y presupuesto revisados;
- rollback probado o demostrado;
- limpieza de recursos de prueba completada.

## Cierre

Una solución AgentCore lista para operar no se define por la cantidad de
componentes habilitados, sino por la claridad de sus fronteras, controles y
evidencias. El proyecto integrador debe demostrar que el agente puede
ejecutarse, usar herramientas, recuperar memoria, respetar identidades,
producir señales, superar evaluaciones y volver a una versión segura cuando
algo falle.

Con este capítulo concluye el recorrido base. Las siguientes mejoras pueden
especializar el proyecto en un dominio, endurecer cumplimiento, ampliar
evaluaciones o automatizar el ciclo de entrega, pero deben partir de los
contratos y límites definidos aquí.
