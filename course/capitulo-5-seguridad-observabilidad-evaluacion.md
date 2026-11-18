# Capítulo 5: Seguridad, observabilidad y evaluación

## Propósito

Al finalizar esta lectura podrás separar la identidad del cliente de las
credenciales que utiliza un agente, diseñar controles de autorización para
herramientas y analizar una ejecución mediante logs, métricas y trazas.
También podrás definir evaluaciones bajo demanda y online con métricas de
calidad, uso de herramientas y resultados observables.

## 1. Tres preguntas distintas

Una solución de agentes debe responder tres preguntas separadas:

1. **Identidad:** ¿quién solicita o ejecuta la operación?
2. **Autorización:** ¿qué acciones puede realizar esa identidad?
3. **Evidencia:** ¿qué ocurrió y cómo podemos demostrarlo?

AgentCore Identity, AgentCore Policy y AgentCore Observability atienden
principalmente esas tres preguntas. AgentCore Evaluations añade una cuarta:
¿el comportamiento observado cumple los criterios de calidad y seguridad
esperados?

No deben confundirse controles de acceso con observabilidad. Un log que dice
que una acción fue permitida no es la política que la permite. Del mismo modo,
una evaluación que detecta respuestas incorrectas no sustituye la
autorización de una herramienta.

## 2. AgentCore Identity

**AgentCore Identity** reúne capacidades para representar la identidad del
agente y gestionar credenciales necesarias para interactuar con otros
servicios. Una identidad es una representación verificable de un actor o
workload; una credencial es la evidencia que permite autenticarse como esa
identidad.

El diseño debe distinguir dos direcciones:

- **Inbound:** solicitudes que entran al agente o a una frontera de AgentCore.
  La pregunta principal es quién invoca y qué contexto de identidad se
  conserva.
- **Outbound:** llamadas que el agente realiza a modelos, Gateway, APIs,
  funciones u otros servicios. La pregunta principal es con qué identidad y
  credenciales se autoriza esa llamada.

La identidad inbound de un usuario no se convierte automáticamente en una
credencial outbound. Pueden coincidir en casos concretos, pero la decisión
debe ser explícita y justificada por el caso de uso.

## 3. OAuth, API keys y credenciales

**OAuth** es un marco para delegar autorización mediante tokens y alcances
definidos. Un **access token** representa permisos concedidos para un tiempo y
audiencia determinados. La aplicación debe validar emisor, audiencia,
expiración, firma y scopes según el proveedor.

Una **API key** es un valor secreto que identifica o habilita el acceso a un
servicio. Es sencilla de integrar, pero suele ofrecer menos contexto que un
token con identidad y scopes. Debe almacenarse fuera del código, rotarse y
limitarse por servicio, entorno y operación.

Una **credencial** es cualquier secreto o mecanismo utilizado para probar
identidad: token, clave, certificado o rol asumido. No debe registrarse en
logs, payloads, imágenes de contenedor ni repositorios.

La selección depende del flujo:

| Mecanismo | Uso típico | Riesgo principal |
|---|---|---|
| OAuth | Acceso delegado con scopes y expiración | Tokens mal validados o con alcance excesivo |
| API key | Integración sencilla servicio a servicio | Robo y dificultad para atribuir acciones |
| Identidad administrada o rol | Acceso de workload a servicios AWS | Permisos demasiado amplios |
| Certificado | Autenticación basada en identidad criptográfica | Rotación y distribución incorrectas |

No elijas un mecanismo solo por facilidad. Evalúa atribución, rotación,
revocación, expiración y alcance mínimo.

## 4. Cliente frente a agente

El **cliente** es quien inicia la solicitud: una persona, aplicación,
workflow o servicio. El **agente** es el workload que procesa esa solicitud y
puede llamar herramientas o servicios.

Una solicitud puede tener esta cadena:

```text
Cliente autenticado
    -> invoca agente
        -> agente asume o usa identidad de workload
            -> accede a Gateway, modelo o backend
```

La identidad del cliente responde quién pidió una acción; la credencial
outbound responde qué identidad técnica la ejecuta. Registrar ambas, cuando
esté permitido, facilita atribución y diagnóstico.

Nunca asumas que porque el cliente puede preguntar algo, el agente puede
ejecutar cualquier herramienta relacionada. La autorización debe evaluarse en
cada frontera relevante.

## 5. AgentCore Policy y autorización determinista

**AgentCore Policy** permite definir reglas sobre acceso a herramientas y
acciones. Una **política** es un conjunto de condiciones que permite, deniega
o limita una operación. **Determinista** significa que la decisión se deriva
de reglas verificables, no de una decisión probabilística del modelo.

Una política puede considerar identidad, herramienta, operación, recurso,
entorno o atributos de la solicitud. Debe responder con claridad:

- qué se permite;
- a quién;
- bajo qué condiciones;
- qué se deniega;
- qué evidencia se registra;
- qué ocurre si la política no puede evaluarse.

La política debe aplicar mínimo privilegio y denegación segura. Si una
herramienta no está expresamente permitida o falta información necesaria para
decidir, no debe convertirse silenciosamente en una operación permitida.

## 6. Políticas en Gateway y operaciones sensibles

Gateway es una frontera natural para controlar herramientas remotas. Antes de
invocar un target, el sistema puede verificar identidad, herramienta,
argumentos y contexto. La política no reemplaza la autorización del backend:
el target debe aplicar sus propios controles.

Una **operación sensible** puede cambiar datos, transferir dinero, exponer
información privada o producir un efecto difícil de revertir. Para esas
operaciones, considera:

- permisos más específicos;
- validación de argumentos;
- aprobación adicional;
- límites de importe o alcance;
- idempotencia;
- registro de decisión;
- posibilidad de rollback.

El modelo puede proponer una acción sensible, pero la política y la aplicación
deben poder bloquearla. La descripción de una herramienta no es una política.

## 7. Observabilidad con CloudWatch y OpenTelemetry

**AgentCore Observability** proporciona señales para entender ejecuciones y
diagnosticar fallos. Puede integrarse con Amazon CloudWatch y OpenTelemetry.

**Amazon CloudWatch** es un servicio de AWS para recopilar, consultar y
visualizar métricas, logs y eventos operativos. **OpenTelemetry** es un
conjunto de APIs, SDKs y convenciones para instrumentar aplicaciones y
exportar señales de observabilidad.

La instrumentación debe responder preguntas operativas concretas:

- ¿Qué sesión falló?
- ¿Cuánto tardó cada etapa?
- ¿Falló el modelo, la memoria, Gateway o el backend?
- ¿Qué versión del agente procesó la solicitud?
- ¿La respuesta se degradó por timeout o por una política?

Observabilidad no significa registrar todo. Los logs deben minimizar datos
personales, secretos y contenido sensible; las trazas deben conservar contexto
útil sin convertir el sistema de diagnóstico en una copia de la conversación.

## 8. Logs, métricas y trazas

### Logs

Un **log** es un registro de un evento con timestamp, severidad, componente,
versión y correlación. Un buen log explica qué ocurrió sin depender de un
estado local no reproducible.

Incluye campos como resultado, causa clasificada, session ID pseudonimizado y
duración cuando sean necesarios. Excluye tokens, API keys, credenciales y
contenido completo de usuario salvo que exista una justificación y control
explícito.

### Métricas

Una **métrica** es un valor numérico agregado a lo largo del tiempo. Ejemplos:
latencia, tasa de errores, invocaciones, timeouts, llamadas por herramienta o
porcentaje de respuestas incompletas.

Las métricas ayudan a detectar tendencias, pero no explican por sí solas una
ejecución individual. Evita etiquetas de alta cardinalidad, como texto
completo del usuario o identificadores ilimitados.

### Distributed tracing

**Distributed tracing** sigue una operación a través de varios servicios.
Una **traza** representa la operación completa y un **span** representa una
unidad de trabajo, por ejemplo Runtime, una llamada al modelo, Memory,
Gateway o el backend.

Los spans deben mantener una relación padre-hijo y una correlación común.
Una traza útil muestra dónde se consumió el tiempo y en qué punto ocurrió el
error, sin incluir secretos ni payloads innecesarios.

## 9. Sesiones, latencia y errores

Para seguir una sesión, propaga una correlación consistente entre Runtime,
agente, memoria, Gateway y herramientas. No uses un identificador de usuario
en claro como única correlación si expone información personal.

La **latencia** es el tiempo transcurrido entre una solicitud y una respuesta.
Analiza el total y sus componentes: validación, espera del modelo,
recuperación de memoria, herramienta y serialización.

La **tasa de errores** es la proporción de solicitudes fallidas frente al total
de solicitudes. Clasifica los errores por componente y causa: autenticación,
autorización, validación, modelo, memoria, Gateway, backend, timeout o límite
de capacidad.

Un dashboard útil combina:

- volumen de invocaciones;
- latencia mediana y percentiles altos;
- errores por componente;
- timeouts;
- uso y fallos de herramientas;
- distribución por versión;
- sesiones afectadas.

## 10. Diagnóstico de una ejecución

Usa una secuencia basada en evidencia:

1. Localiza la invocación por correlación y versión.
2. Revisa el span raíz y el primer span fallido.
3. Compara duración esperada con timeout y límites.
4. Determina si el fallo ocurrió en orquestación, inferencia, memoria o
   herramienta.
5. Comprueba identidad y decisión de política.
6. Examina el contrato de entrada y salida.
7. Reproduce con payload no sensible y la misma versión.
8. Documenta causa, impacto y acción correctiva.

La **orquestación** es el flujo que coordina nodos, decisiones y herramientas.
La **inferencia** es la generación o transformación realizada por el modelo.
Una respuesta incorrecta no siempre es un fallo del modelo: puede deberse a
memoria irrelevante, herramienta equivocada, política restrictiva o contrato
mal adaptado.

## 11. AgentCore Evaluations

**AgentCore Evaluations** permite analizar interacciones del agente mediante
criterios y métricas definidos. Una **métrica de evaluación** es una medida que
representa una propiedad deseada, como exactitud, relevancia, seguridad,
latencia o uso correcto de herramientas.

Una evaluación debe definir:

- objetivo;
- conjunto de interacciones;
- criterio de éxito;
- método de medición;
- umbral o interpretación;
- versión del agente y del modelo;
- tratamiento de fallos y datos sensibles.

### Evaluación bajo demanda

Una evaluación **bajo demanda** se ejecuta sobre un conjunto seleccionado para
una investigación, cambio o release. Es útil para comparar versiones y
analizar regresiones antes de promoverlas.

### Evaluación online

Una evaluación **online** analiza interacciones durante la operación o a partir
de una muestra continua. Ayuda a detectar degradación y casos no presentes en
los datos de prueba, pero requiere controlar coste, privacidad, muestreo y
latencia.

Una evaluación online no debe bloquear automáticamente una acción crítica sin
una política diseñada para ello. Puede generar alertas, muestras para revisión
o señales de calidad.

## 12. Calidad, herramientas y resultados

Las métricas de un agente deben cubrir más que el texto final:

- **Calidad de respuesta:** exactitud, relevancia, completitud y claridad.
- **Uso de herramientas:** herramienta correcta, argumentos válidos, orden
  adecuado y ausencia de llamadas innecesarias.
- **Resultado operativo:** latencia, errores, finalización, coste y
  cumplimiento de políticas.
- **Seguridad:** ausencia de exposición de secretos, acciones no autorizadas o
  contaminación de memoria.

Un resultado correcto por casualidad no demuestra una política correcta. Evalúa
también casos negativos, entradas ambiguas, herramientas indisponibles,
memoria incorrecta y solicitudes fuera de alcance.

## Instrumentación y evaluación

Aplica este flujo:

1. Define qué comportamiento importa para el caso de uso.
2. Añade correlación, versión y señales mínimas.
3. Instrumenta spans para Runtime, modelo, Memory, Gateway y herramientas.
4. Excluye secretos y minimiza datos sensibles.
5. Construye un conjunto de interacciones representativo.
6. Ejecuta evaluación bajo demanda antes de cambios.
7. Configura evaluación online con muestreo y alertas.
8. Compara resultados por versión y no solo promedios globales.
9. Investiga regresiones con trazas y logs.
10. Convierte hallazgos en cambios de código, política, prompt o datos de
    evaluación.

## Cierre

Identity establece quién actúa, Policy limita qué puede hacer, Observability
explica qué ocurrió y Evaluations mide si el comportamiento cumple el
objetivo. Estos controles deben diseñarse juntos: una política sin evidencia
es difícil de operar, una traza sin protección puede filtrar datos y una
evaluación sin versión no permite comparar resultados.

El siguiente capítulo integrará Runtime, Gateway, Memory, Identity, Policy,
Bedrock y observabilidad en una arquitectura de referencia orientada a
producción.
