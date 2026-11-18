# Capítulo 1: Arquitectura y fundamentos de Amazon Bedrock AgentCore

## Propósito

Al finalizar esta lectura podrás ubicar los componentes de Amazon Bedrock
AgentCore dentro de una arquitectura de agentes, distinguir sus
responsabilidades y preparar un entorno inicial de trabajo con Python, AWS
CLI y los permisos mínimos necesarios. También podrás diferenciar el plano de
control del plano de ejecución y decidir qué capacidades de AgentCore necesita
una solución.

## 1. ¿Qué es Amazon Bedrock AgentCore?

Amazon Bedrock AgentCore es un conjunto de capacidades administradas de AWS
para construir, desplegar, integrar, proteger, observar y evaluar agentes de
inteligencia artificial. Un **agente** es un sistema que interpreta una
solicitud, razona sobre los pasos necesarios y, cuando corresponde, utiliza
herramientas o servicios externos para producir un resultado.

AgentCore no sustituye al framework de orquestación del agente. Una aplicación
puede seguir utilizando LangGraph, CrewAI u otro framework para definir el
flujo de decisión. AgentCore aporta servicios de infraestructura y operación
alrededor de ese flujo: ejecución, herramientas remotas, memoria, identidad,
políticas, observabilidad y evaluación.

Esta separación permite que la lógica del agente permanezca en código Python
mientras las capacidades transversales se gestionan mediante interfaces de AWS.
El beneficio principal no es únicamente ejecutar un modelo, sino establecer
límites, trazabilidad y controles operativos alrededor de un sistema que puede
tomar acciones.

## 2. Componentes y responsabilidades

Los componentes deben entenderse como responsabilidades separadas, aunque una
misma solución pueda usarlos juntos.

### Runtime

**AgentCore Runtime** es la capacidad de ejecución administrada para un agente.
Recibe invocaciones, inicia el código del agente, mantiene el contexto de la
ejecución según el contrato definido por la aplicación y devuelve una
respuesta. Una **invocación** es una solicitud individual para ejecutar el
agente, y una **sesión** es el contexto lógico que permite relacionar varias
interacciones.

Runtime se ocupa de ejecutar el workload; no decide por sí mismo qué
herramientas debe usar el agente ni reemplaza la lógica de orquestación. Es
responsabilidad de la aplicación definir el contrato de entrada y salida,
validar payloads y manejar errores.

### Gateway

**AgentCore Gateway** es una capa para publicar y consumir herramientas de
forma controlada. Una **herramienta** es una operación que el agente puede
solicitar, como consultar un sistema o ejecutar una acción. Gateway puede
presentar herramientas provenientes de APIs REST, funciones Lambda o
servidores compatibles con MCP.

**Model Context Protocol (MCP)** es un protocolo para describir y exponer
herramientas y recursos que un modelo o agente puede descubrir y utilizar.
Gateway ayuda a desacoplar la lógica del agente de la implementación concreta
de cada herramienta. Así, el agente trabaja con un contrato y no necesita
conocer todos los detalles de red, autenticación o backend.

### Memory

**AgentCore Memory** proporciona almacenamiento y recuperación de información
relacionada con las interacciones del agente. La memoria puede servir para
conservar contexto conversacional o información útil entre interacciones,
según la estrategia y el diseño de la aplicación.

Memoria no significa que el modelo recuerde automáticamente todo. La
aplicación debe decidir qué eventos registrar, qué información recuperar y
cuándo incorporarla al contexto. En capítulos posteriores se estudiarán en
detalle los identificadores, namespaces y estrategias de memoria.

### Identity

**AgentCore Identity** concentra mecanismos para gestionar la identidad del
agente y las credenciales que necesita para comunicarse con otros servicios.
La **autenticación** responde a “¿quién es el solicitante?”; la
**autorización** responde a “¿qué puede hacer?”. Esta distinción es importante
porque la identidad del usuario o cliente que invoca al agente no siempre es la
misma identidad que el agente utiliza para acceder a una herramienta.

### Policy

**AgentCore Policy** permite expresar controles sobre las acciones que pueden
realizarse. Una **política** es un conjunto de reglas que permite, restringe o
condiciona operaciones. Las políticas aportan una barrera determinista
alrededor de decisiones que, de otro modo, podrían depender solo del modelo.

Una política no reemplaza la validación en el código ni la seguridad de AWS.
Debe complementar los permisos de IAM, la autenticación y las comprobaciones
de la herramienta.

### Observability

**AgentCore Observability** reúne la información necesaria para entender el
comportamiento del sistema. **Observabilidad** es la capacidad de inferir el
estado interno de una aplicación a partir de sus señales, principalmente
logs, métricas y trazas.

Una **traza** representa una operación completa; un **span** representa una
parte de esa operación, como una llamada al modelo o una herramienta. Las
métricas muestran valores agregados, como latencia o cantidad de errores, y
los logs registran eventos detallados. AgentCore se integra con servicios como
Amazon CloudWatch y con OpenTelemetry, un estándar y conjunto de herramientas
para instrumentar señales de observabilidad.

### Evaluations

**AgentCore Evaluations** permite evaluar el comportamiento de un agente
mediante métricas y criterios definidos para las interacciones. Una
**evaluación** es un proceso que analiza una respuesta o una ejecución para
determinar si cumple condiciones de calidad, seguridad o uso correcto de
herramientas.

Las evaluaciones pueden ejecutarse bajo demanda sobre un conjunto de
interacciones o integrarse al seguimiento continuo de una aplicación. Una
evaluación no demuestra por sí sola que un agente sea seguro o correcto: sus
resultados dependen de las métricas, datos y criterios elegidos.

## 3. Capacidades adicionales

### Browser

La capacidad **Browser** permite que un agente interactúe con contenido web
mediante una sesión de navegación controlada. Esto puede ser útil cuando la
información o la tarea requiere una interfaz web, pero introduce riesgos
adicionales: sitios no confiables, datos sensibles, acciones irreversibles y
contenido que intenta influir en el comportamiento del agente.

El uso de Browser debe limitarse mediante identidad, políticas, validación de
dominios y supervisión. No debe asumirse que una página web es una fuente
confiable solo porque el agente puede leerla.

### Code Interpreter

**Code Interpreter** es una capacidad para ejecutar código en un entorno
controlado con el fin de analizar datos o realizar cálculos. Resulta útil para
operaciones que requieren precisión computacional, pero el código generado
debe tratarse como no confiable. Los permisos, archivos disponibles, tiempo de
ejecución y efectos externos deben estar limitados.

Browser y Code Interpreter amplían lo que un agente puede hacer; no deben
habilitarse por defecto. La decisión debe considerar el riesgo, la necesidad
real y la capacidad de verificar el resultado.

## 4. Runtime y Harness

**AgentCore Runtime** es la infraestructura administrada donde se ejecuta el
agente. **AgentCore Harness** es el conjunto de elementos de integración que
ayuda a adaptar el código del agente a las convenciones de ejecución de
AgentCore, como su punto de entrada, contrato de invocación y ciclo de vida.

La diferencia práctica es de responsabilidad: Runtime ejecuta el workload,
mientras Harness facilita conectarlo a Runtime. El framework de agentes sigue
siendo responsable de la orquestación interna. Confundir estos conceptos puede
llevar a atribuir a Runtime funciones que corresponden al código de la
aplicación o al framework.

## 5. SDK, CLI y APIs de AWS

El **SDK de Python** es un conjunto de librerías que permite interactuar con
servicios de AWS desde código Python. **Boto3** es el SDK de AWS utilizado
habitualmente en Python. Es apropiado para que una aplicación cree clientes,
realice invocaciones y consuma APIs desde código.

La **AWS CLI** es una herramienta de línea de comandos para administrar
recursos y ejecutar operaciones de AWS desde una terminal. Es útil para
configuración, automatización y diagnóstico. Las **APIs de AWS** son las
interfaces programáticas que reciben solicitudes para consultar o modificar
recursos; el SDK y la CLI actúan como clientes de esas APIs.

Conviene distinguir las capas:

1. La aplicación usa el SDK cuando necesita integrar AWS en su lógica.
2. Un operador usa la CLI para tareas manuales, automatización o inspección.
3. Ambos terminan invocando APIs de AWS, sujetas a autenticación,
   autorización, región y límites del servicio.

## 6. Plano de control y plano de ejecución

El **plano de control** administra la configuración y el ciclo de vida de los
recursos. Crear un recurso, configurar una política, registrar una
integración o consultar su estado son operaciones del plano de control.

El **plano de ejecución** procesa el tráfico y las operaciones de negocio.
Invocar un agente, ejecutar su flujo, llamar a una herramienta y devolver una
respuesta pertenecen al plano de ejecución.

La separación tiene consecuencias prácticas. Los permisos para administrar
recursos no deberían concederse automáticamente a la identidad que solo
necesita ejecutar un agente. También ayuda a diagnosticar fallos: un error al
crear o configurar un recurso pertenece a la administración, mientras que un
timeout durante una invocación pertenece a la ejecución.

## 7. Preparación inicial del entorno

Antes de ejecutar una aplicación, valida estos elementos:

1. **Región:** selecciona una región de AWS compatible con los servicios y
   modelos que se utilizarán. La región forma parte de la dirección lógica de
   muchos recursos.
2. **Credenciales:** configura una identidad de desarrollo sin incorporar
   claves directamente al código, repositorio o archivos compartidos.
3. **Permisos mínimos:** concede solo las acciones y recursos necesarios para
   el aprendizaje. El acceso administrativo permanente no es un requisito del
   diseño.
4. **SDK y CLI:** instala versiones compatibles y confirma que la aplicación y
   la terminal utilizan la configuración esperada.
5. **Acceso al modelo de Bedrock:** verifica que la cuenta, región e identidad
   tengan acceso al modelo que se invocará.
6. **Registro de configuración:** documenta región, perfiles, versiones y
   permisos usados, sin registrar secretos.

El principio de **mínimo privilegio** indica que una identidad debe recibir
solo los permisos indispensables para realizar una tarea. Es una medida de
reducción de impacto: si una credencial se expone o una herramienta se
comporta incorrectamente, el alcance del incidente queda limitado.

## Método de análisis para una solución AgentCore

Para analizar una solución nueva, usa esta secuencia:

1. Describe qué hace el agente y qué parte seguirá viviendo en Python.
2. Separa ejecución, herramientas, memoria, identidad, políticas,
   observabilidad y evaluación.
3. Define qué datos entran y salen de cada componente.
4. Identifica quién administra recursos y quién solo ejecuta invocaciones.
5. Enumera permisos, riesgos y límites antes de habilitar capacidades
   adicionales.
6. Comprueba región, credenciales, acceso al modelo y dependencias del SDK.

Este método evita empezar por habilitar todos los componentes. Cada capacidad
debe responder a una necesidad concreta y tener un propietario, un límite y
una forma de observación.

## Cierre

AgentCore debe verse como una plataforma de capacidades complementarias, no
como un único modelo o framework de agentes. Runtime ejecuta, Gateway integra
herramientas, Memory conserva contexto, Identity y Policy controlan el acceso,
Observability explica el comportamiento y Evaluations mide resultados.

En el siguiente capítulo, esta arquitectura se concretará en AgentCore
Runtime: se adaptará un agente Python, se definirá su contrato de ejecución y
se estudiarán sus invocaciones, sesiones y endpoints.
