# Capítulo 2: AgentCore Runtime y despliegue de agentes

## Propósito

Al finalizar esta lectura podrás adaptar un agente Python existente al
contrato de AgentCore Runtime, distinguir una invocación de una sesión y
elegir una modalidad de respuesta adecuada. También podrás describir el
recorrido desde el código fuente hasta un endpoint versionado, incluyendo el
empaquetado del contenedor, la publicación de la imagen y la invocación desde
un cliente Python.

## 1. Responsabilidad de AgentCore Runtime

AgentCore Runtime es la capacidad de ejecución administrada de AgentCore. Su
responsabilidad es recibir una solicitud, iniciar o reutilizar el contexto de
ejecución correspondiente, entregar el payload al punto de entrada del agente
y devolver el resultado al cliente.

El **workload** es la carga de trabajo que se ejecuta: en este caso, el código
Python del agente y sus dependencias. Runtime proporciona el entorno y el
contrato de ejecución, pero no define por sí mismo la estrategia de
orquestación. LangGraph, CrewAI o el código de aplicación siguen siendo
responsables de decidir cómo se procesan los estados y pasos internos del
agente.

Una arquitectura mínima contiene:

1. Un cliente que envía una solicitud.
2. Un endpoint de Runtime que recibe la invocación.
3. Un punto de entrada que traduce el payload al formato de la aplicación.
4. El agente Python, que ejecuta la lógica de negocio.
5. Una respuesta serializable que vuelve al cliente.

Esta separación permite probar el agente localmente y después cambiar su forma
de ejecución sin reescribir toda la lógica. Para lograrlo, el punto de entrada
debe ser pequeño, explícito y estable.

## 2. Ciclo de vida de una invocación

Una **invocación** es una solicitud individual para ejecutar el agente. Su
ciclo de vida puede analizarse así:

1. El cliente construye un payload válido y proporciona el identificador de
   sesión cuando la interacción lo requiere.
2. Runtime autentica y enruta la solicitud al endpoint correspondiente.
3. El adaptador de la aplicación valida la entrada y la entrega al agente.
4. El agente ejecuta su flujo, consulta el modelo y procesa sus pasos
   internos.
5. El punto de entrada transforma el resultado en una respuesta serializable.
6. Runtime transmite o devuelve la respuesta y registra el resultado
   operativo.

El ciclo puede terminar correctamente, con un error controlado de la
aplicación, con un fallo de infraestructura o por un límite de tiempo. El
cliente debe poder distinguir estas situaciones. Una respuesta con forma de
éxito que oculta un error dificulta el diagnóstico y puede inducir al usuario a
tomar decisiones basadas en información incompleta.

## 3. Contrato de entrada y salida

El **contrato de entrada** define la forma y significado del payload que el
agente acepta. El **contrato de salida** define la forma y significado de la
respuesta que produce. Ambos deben documentar tipos, campos obligatorios,
campos opcionales, errores y límites de tamaño.

Un contrato conceptual podría recibir:

```json
{
  "input": "Resume esta política de viajes",
  "session_id": "sesion-demo-01",
  "metadata": {
    "locale": "es-MX"
  }
}
```

Y devolver:

```json
{
  "output": "La política establece...",
  "session_id": "sesion-demo-01",
  "status": "completed"
}
```

Los nombres anteriores son ilustrativos; el equipo debe fijar el contrato real
que utilizará la aplicación. La regla importante es que el adaptador no
confunda el payload de transporte con el estado interno de LangGraph. El
primero pertenece a la interfaz del endpoint; el segundo pertenece al flujo
del agente.

Un contrato confiable debe:

- validar la presencia y el tipo de los campos obligatorios;
- rechazar entradas inválidas con un error explícito;
- evitar devolver secretos, trazas internas o mensajes de excepción al usuario;
- conservar un identificador de correlación o sesión cuando sea necesario;
- producir respuestas serializables y estables;
- definir qué ocurre cuando el agente no puede completar la solicitud.

## 4. Sesiones y aislamiento

Una **sesión** es el contexto lógico que agrupa varias invocaciones
relacionadas. El **identificador de sesión** permite que la aplicación
reconozca que dos solicitudes forman parte de una misma conversación o flujo.
No debe confundirse con la identidad del usuario, con una instancia de
contenedor ni con una conversación almacenada en Memory.

El **aislamiento entre sesiones** significa que el estado de una sesión no debe
aparecer accidentalmente en otra. Para preservarlo:

- valida y propaga el identificador de sesión de forma consistente;
- no uses variables globales para guardar estado de usuario;
- separa las claves de caché y los registros por sesión;
- evita reutilizar objetos mutables entre solicitudes;
- define qué estado es temporal y qué estado debe persistirse;
- prueba dos sesiones concurrentes con datos diferentes.

La ausencia de un identificador no debe resolverse inventando una sesión
compartida. La aplicación debe definir si crea una sesión nueva, rechaza la
solicitud o trabaja de forma completamente independiente.

## 5. Endpoints, versiones e invocación

Un **endpoint** es un destino identificable al que un cliente envía
invocaciones. Una **versión** es una representación identificable del agente o
de su configuración en un momento determinado. Versionar permite comparar,
probar y actualizar sin cambiar silenciosamente el comportamiento que consume
un cliente.

Una práctica segura separa:

1. La versión que se prueba.
2. La versión que se publica para validación.
3. La versión que recibe tráfico productivo.

La administración de endpoints debe incluir una estrategia de actualización y
reversión. Antes de promover una versión, valida contrato, errores, latencia,
aislamiento y consumo. No actualices el destino productivo solo porque la
imagen fue construida correctamente: una imagen disponible no demuestra que
el agente se comporte correctamente.

## 6. Modalidades de invocación

### Síncrona

En una invocación **síncrona**, el cliente espera a que el agente termine y
recibe una respuesta final. Es adecuada para solicitudes breves con un límite
de tiempo conocido. Su simplicidad facilita el manejo de errores, pero el
cliente debe tolerar latencia y timeouts.

### Asíncrona

En una invocación **asíncrona**, el cliente no necesita mantener abierta la
conexión hasta que termine el trabajo. El resultado se consulta, entrega o
procesa por otro mecanismo. Es apropiada para tareas largas o que no requieren
respuesta inmediata, pero exige un modelo explícito de estados, reintentos y
correlación.

### Streaming

En **streaming**, el agente entrega partes de la respuesta a medida que están
disponibles. Reduce el tiempo hasta el primer contenido visible y puede
mejorar la experiencia interactiva. También complica el contrato: el cliente
debe procesar eventos parciales, detectar el final, manejar interrupciones y
evitar presentar un resultado incompleto como definitivo.

La modalidad debe elegirse por el comportamiento del caso de uso, no por
preferencia tecnológica. Define primero si el usuario necesita una respuesta
final, progreso observable o resultados parciales.

## 7. Punto de entrada con `BedrockAgentCoreApp`

`BedrockAgentCoreApp` es el componente del SDK que ayuda a declarar la
aplicación compatible con AgentCore Runtime. El decorador `@app.entrypoint`
identifica la función que recibe la invocación y actúa como frontera entre el
protocolo de Runtime y la lógica del agente.

Un punto de entrada bien diseñado hace pocas cosas:

1. Recibe el payload.
2. Valida sus campos.
3. Construye la entrada del agente.
4. Ejecuta el flujo.
5. Convierte el resultado al contrato de salida.

La validación, el manejo de errores y la serialización deben permanecer
explícitos. Evita mezclar en el entrypoint configuración global, lógica de
negocio extensa y estado mutable de usuarios. Esa separación facilita las
pruebas locales y reduce el riesgo de que un cambio en el transporte modifique
el comportamiento del agente.

## 8. Payloads, respuestas y errores

Un **payload** es la representación serializada de los datos que atraviesan la
frontera de invocación. Puede contener texto, parámetros estructurados,
identificadores y metadata. La metadata debe tener un propósito definido; no
debe utilizarse como canal informal para transportar secretos o instrucciones
sin validar.

Los errores deben clasificarse por causa:

- **Entrada inválida:** el cliente no cumple el contrato.
- **Error del agente:** la lógica o una dependencia del agente no pudo
  completar el flujo.
- **Error de integración:** el modelo o un servicio requerido no respondió
  como se esperaba.
- **Error operativo:** timeout, límite de concurrencia o fallo de ejecución.

La respuesta externa debe ser útil para el cliente, pero no revelar secretos ni
detalles internos. Registra el contexto técnico necesario para diagnosticar,
asociándolo con una sesión o correlación, y devuelve un estado que permita
decidir si corresponde reintentar.

## 9. Adaptación de un agente LangGraph

LangGraph modela un flujo de ejecución mediante nodos, aristas y estado. Para
integrarlo con Runtime, el adaptador debe traducir entre el contrato externo y
el estado inicial del grafo:

1. Extrae la entrada válida del payload.
2. Construye un estado inicial mínimo.
3. Inyecta solo la metadata que el grafo necesita.
4. Ejecuta el grafo.
5. Selecciona una salida estable y serializable.
6. Asocia errores y resultados con la sesión correspondiente.

Runtime no debe conocer los detalles de cada nodo. Del mismo modo, el grafo no
debe depender de objetos específicos del transporte si puede trabajar con
tipos de dominio. Esta frontera permite cambiar el endpoint o el cliente sin
reescribir el flujo interno.

## 10. CLI, contenedores y ECR

AgentCore CLI es la interfaz de línea de comandos para crear, configurar y
operar proyectos relacionados con AgentCore. Debe utilizarse como herramienta
repetible: los parámetros, región, perfil y destino deben quedar documentados
o automatizados, no depender de valores recordados por una persona.

Un **contenedor** empaqueta la aplicación y sus dependencias en una unidad
reproducible. El `Dockerfile` describe cómo construir esa imagen. Una **imagen**
es una plantilla inmutable de ejecución; un contenedor es una instancia en
ejecución de esa imagen.

Amazon Elastic Container Registry (ECR) es un registro administrado donde se
almacenan imágenes de contenedor. El flujo conceptual es:

1. Preparar el código, dependencias y configuración no secreta.
2. Construir y probar la imagen localmente.
3. Etiquetar la imagen con una referencia inequívoca.
4. Publicarla en ECR.
5. Configurar Runtime para utilizar esa imagen.
6. Validar una invocación antes de promover la versión.

No deben incluirse claves, tokens ni archivos de credenciales en la imagen.
La configuración específica del entorno debe inyectarse mediante mecanismos
de configuración e identidad apropiados.

## 11. Invocación desde Python con Boto3

Boto3 permite que un cliente Python invoque servicios de AWS mediante sus APIs.
El cliente debe configurar región e identidad de forma segura, construir un
payload conforme al contrato y conservar la información necesaria para
diagnóstico.

Una invocación responsable contempla:

- timeout explícito;
- validación de la respuesta;
- clasificación de errores;
- reintentos solo para fallos transitorios y operaciones idempotentes;
- propagación de sesión o correlación;
- no registrar payloads sensibles sin necesidad.

El cliente no debe asumir que cualquier error es reintentable. Reintentar una
acción que modifica datos puede duplicar efectos si no existe idempotencia.
Para una primera integración, prueba con una operación de consulta y un
payload pequeño antes de añadir concurrencia o streaming.

## 12. Actualización, concurrencia y límites

La **concurrencia** es la cantidad de invocaciones que se procesan al mismo
tiempo. Aumentarla puede mejorar capacidad, pero también eleva consumo,
latencia de dependencias y presión sobre límites externos.

El **estado entre invocaciones** debe clasificarse:

- estado local de una llamada, que puede descartarse al terminar;
- estado conversacional, que requiere asociarse con una sesión;
- estado persistente, que necesita un mecanismo de almacenamiento explícito.

No supongas que una instancia de ejecución permanecerá disponible ni que una
solicitud siguiente llegará al mismo proceso. El código debe funcionar aunque
Runtime cree otra instancia.

Los **límites operativos** incluyen tiempo de ejecución, tamaño de payload,
concurrencia, capacidad de dependencias y cuotas del servicio. Documentarlos
permite diseñar timeouts y respuestas parciales sin convertir un límite
previsible en una falla misteriosa.

## Procedimiento de despliegue

Usa esta secuencia para un primer despliegue:

1. Fija el contrato de entrada, salida y errores.
2. Ejecuta el agente localmente con una entrada representativa.
3. Añade el adaptador de `BedrockAgentCoreApp` y prueba el entrypoint.
4. Prueba sesiones aisladas y errores de validación.
5. Construye la imagen y verifica que no contenga secretos.
6. Publica una referencia versionada en ECR.
7. Configura un endpoint de prueba mediante AgentCore CLI.
8. Invoca el endpoint con un cliente Python.
9. Observa latencia, errores, respuesta y aislamiento.
10. Solo después de validar, actualiza o promueve otra versión.

## Cierre

Runtime convierte un agente Python en una unidad invocable, pero la calidad de
la integración depende del contrato, el aislamiento de sesiones, el manejo de
errores y la estrategia de versionamiento. El empaquetado en contenedor y la
publicación en ECR hacen repetible el despliegue; no sustituyen las pruebas de
comportamiento.

En el siguiente capítulo, Gateway permitirá conectar herramientas remotas y
MCP con el agente. La frontera construida aquí será la base para que esas
herramientas se consuman sin mezclar su implementación con el entrypoint.
