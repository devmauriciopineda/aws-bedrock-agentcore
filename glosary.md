# Glosario de Inteligencia Artificial y AWS Bedrock AgentCore

Definiciones de los principales conceptos utilizados en el plan de estudio y
en los materiales de los capítulos 1 a 6.

## Inteligencia artificial y agentes

### Agente

Sistema de software que interpreta una solicitud, decide qué pasos necesita
seguir y puede utilizar modelos, herramientas o servicios externos para
producir un resultado.

### Inteligencia artificial (IA)

Campo de la computación que desarrolla sistemas capaces de realizar tareas que
normalmente requieren capacidades asociadas con la inteligencia humana, como
percepción, razonamiento, aprendizaje o generación de contenido.

### Modelo de lenguaje grande (LLM)

Modelo de inteligencia artificial entrenado con grandes volúmenes de texto
para comprender y generar lenguaje natural. Puede responder preguntas,
resumir, clasificar, extraer información o decidir cuándo solicitar una
herramienta.

### Modelo fundacional

Modelo de IA entrenado con datos generales y reutilizable como base para
distintas aplicaciones, tareas o dominios.

### Inferencia

Ejecución de un modelo ya entrenado para producir una predicción, respuesta,
clasificación o generación a partir de una entrada.

### Prompt

Instrucción, contexto y datos proporcionados a un modelo para orientar su
respuesta. Un prompt no debe considerarse un control de seguridad suficiente.

### Contexto

Información disponible para el modelo o agente durante una invocación, como
instrucciones, mensajes, resultados de herramientas y recuerdos recuperados.

### Ventana de contexto

Cantidad máxima de información que un modelo puede procesar en una solicitud.
Un contexto demasiado grande puede aumentar coste, latencia y ruido.

### Token

Unidad de texto procesada por un modelo de lenguaje. Una palabra puede
corresponder a uno o varios tokens, según el idioma y la representación usada.

### Embedding

Representación numérica de un texto, imagen u otro objeto que conserva
relaciones semánticas aproximadas y permite comparar contenidos por similitud.

### Generación aumentada por recuperación (RAG)

Patrón que recupera información relevante desde una fuente externa y la añade
al contexto del modelo antes de generar una respuesta.

### Alucinación

Respuesta generada que parece plausible pero contiene información falsa,
inexacta o no respaldada por los datos disponibles.

### Orquestación

Coordinación de pasos, decisiones, estado, herramientas y respuestas que forman
el flujo de un agente.

### Framework de agentes

Biblioteca o plataforma que ayuda a definir el flujo, estado, nodos y llamadas
de herramientas de un agente. LangGraph y CrewAI son ejemplos mencionados en
el plan.

### LangGraph

Framework para modelar flujos de agentes como grafos de nodos, transiciones y
estado. Permite controlar de forma explícita la secuencia de decisiones y
operaciones.

### CrewAI

Framework para coordinar agentes y tareas colaborativas. Se menciona como
conocimiento previo del perfil de los estudiantes.

### Herramienta

Operación que un agente puede solicitar para consultar información o producir
un efecto fuera de su propio proceso, como consultar una API o calcular un
valor.

### Herramienta local

Herramienta implementada dentro del mismo proceso o despliegue que el agente.
Simplifica la invocación, pero comparte dependencias, recursos y superficie de
seguridad.

### Herramienta remota

Herramienta expuesta por un servicio externo, API, función o servidor de
protocolo. Puede reutilizarse entre agentes, pero requiere red, identidad,
autorización y manejo de errores.

### Llamada de herramienta

Solicitud del agente para ejecutar una herramienta con argumentos concretos.
Que el modelo proponga la llamada no implica que la operación esté autorizada.

### Estado

Datos que representan la información disponible durante una ejecución. Puede
pertenecer a una invocación, una sesión, un grafo o una memoria persistente.

### Memoria de corto plazo

Contexto de una conversación o sesión activa, como mensajes recientes y
resultados necesarios para continuar el flujo.

### Memoria de largo plazo

Información seleccionada que puede recuperarse en sesiones futuras, como
preferencias, resúmenes o hechos validados.

## AWS y Amazon Bedrock AgentCore

### Amazon Web Services (AWS)

Plataforma de servicios cloud de Amazon para ejecutar aplicaciones, almacenar
datos, administrar identidades, conectar sistemas y operar infraestructura.

### Región de AWS

Ubicación geográfica aislada donde AWS agrupa recursos y servicios. La región
puede determinar disponibilidad, latencia, residencia de datos y acceso a
modelos.

### Amazon Bedrock

Servicio administrado de AWS que permite utilizar modelos fundacionales y
capacidades de IA generativa mediante APIs, sin administrar directamente la
infraestructura de entrenamiento o inferencia.

### Amazon Bedrock AgentCore

Conjunto de capacidades administradas de AWS para construir, desplegar,
integrar, proteger, observar y evaluar agentes de inteligencia artificial.

### AgentCore Runtime

Capacidad de ejecución administrada para recibir invocaciones, ejecutar el
código del agente y devolver respuestas mediante un endpoint y un contrato
definidos.

### AgentCore Harness

Conjunto de elementos de integración que ayuda a adaptar un agente a las
convenciones de ejecución de Runtime, como su punto de entrada y contrato.

### AgentCore Gateway

Capa de integración que publica y consume herramientas y las conecta con APIs,
funciones Lambda o servidores MCP mediante targets y contratos definidos.

### AgentCore Memory

Capacidad para registrar y recuperar información relacionada con interacciones
del agente, organizada por ámbitos como memoria, actor, sesión y namespace.

### AgentCore Identity

Capacidad para representar la identidad del agente y gestionar la autenticación
o credenciales necesarias para acceder a otros servicios.

### AgentCore Policy

Capacidad para definir reglas deterministas que permiten, deniegan o limitan
el acceso a herramientas y acciones.

### AgentCore Observability

Capacidad y conjunto de integraciones para observar ejecuciones mediante logs,
métricas y trazas, incluyendo integración con CloudWatch y OpenTelemetry.

### AgentCore Evaluations

Capacidad para evaluar interacciones y ejecuciones de agentes mediante
métricas y criterios de calidad, seguridad, uso de herramientas u operación.

### Memory ID

Identificador del recurso o espacio lógico de AgentCore Memory donde se
registran y recuperan eventos.

### Actor ID

Identificador del actor al que pertenece una memoria, normalmente un usuario,
cliente, organización o entidad de negocio.

### Session ID

Identificador de una conversación o flujo concreto de un actor. Permite
separar sesiones y relacionar varias invocaciones.

### Namespace

Espacio lógico para organizar y segmentar tipos de memoria, como preferencias,
resúmenes o hechos de dominio. No constituye por sí solo una frontera de
seguridad.

### Evento de memoria

Hecho registrado durante una interacción, como un mensaje, respuesta,
resultado de herramienta, resumen o preferencia.

### Evaluación bajo demanda

Evaluación ejecutada explícitamente sobre un conjunto de interacciones, por
ejemplo antes de promover una nueva versión.

### Evaluación online

Evaluación realizada durante la operación o sobre una muestra continua del
tráfico para detectar degradación y casos no previstos.

## Integración y protocolos

### Model Context Protocol (MCP)

Protocolo para describir y exponer herramientas y recursos que un cliente
compatible puede descubrir y utilizar.

### Cliente MCP

Aplicación o componente que descubre herramientas MCP y solicita su ejecución.

### Servidor MCP

Servicio que publica herramientas o recursos mediante MCP y procesa las
solicitudes de clientes compatibles.

### Target

Configuración de Gateway que conecta una herramienta publicada con su
implementación real, como una API REST, función Lambda o servidor MCP.

### Endpoint

Destino identificable al que un cliente envía invocaciones o solicitudes. En
Runtime representa una entrada para ejecutar una versión del agente.

### Descubrimiento de herramientas

Proceso por el que un cliente conoce las herramientas disponibles, sus
descripciones, esquemas, restricciones y resultados esperados.

### Esquema de entrada

Descripción estructurada de los campos, tipos, reglas y restricciones que una
herramienta acepta.

### Esquema de salida

Descripción estructurada de los datos que una herramienta devuelve y de la
forma en que el consumidor debe interpretarlos.

### API REST

Interfaz web que expone recursos y operaciones mediante convenciones HTTP,
como métodos, rutas, headers y cuerpos estructurados.

### AWS Lambda

Servicio de AWS que ejecuta funciones sin que el equipo administre
servidores. Puede implementar herramientas acotadas y activadas bajo demanda.

### AWS SDK

Conjunto de bibliotecas que permite utilizar APIs de AWS desde lenguajes de
programación.

### Boto3

SDK de AWS para Python. Permite crear clientes, configurar servicios e invocar
APIs de AWS desde una aplicación.

### AWS CLI

Herramienta de línea de comandos para configurar, consultar y operar servicios
y recursos de AWS.

### Payload

Representación serializada de los datos que atraviesan una frontera de
invocación, como entrada, salida, metadata o argumentos de una herramienta.

### Streaming

Modalidad de respuesta que entrega datos parciales a medida que están
disponibles, en lugar de esperar únicamente el resultado final.

### Invocación síncrona

Invocación en la que el cliente espera la respuesta final antes de continuar.

### Invocación asíncrona

Invocación en la que el cliente no mantiene necesariamente abierta la conexión
hasta que termina el trabajo y procesa el resultado posteriormente.

## Seguridad e identidad

### Autenticación

Proceso de verificar quién es un usuario, servicio o workload.

### Autorización

Proceso de decidir qué acciones, recursos o herramientas puede utilizar una
identidad autenticada.

### Identidad inbound

Identidad asociada con una solicitud que entra al agente o a una frontera de
la aplicación.

### Identidad outbound

Identidad que utiliza el agente para acceder a un modelo, herramienta,
servicio o backend externo.

### Credencial

Secreto o mecanismo criptográfico utilizado para demostrar una identidad, como
un token, API key, certificado o rol.

### OAuth

Marco de autorización delegada que utiliza tokens y scopes para conceder
acceso limitado a un recurso.

### API key

Valor secreto utilizado para identificar o habilitar el acceso a un servicio.
Debe almacenarse, rotarse y limitarse de forma segura.

### Token

Valor emitido por un sistema de identidad para representar una sesión,
identidad, autorización o contenido procesable.

### Scope

Alcance o conjunto de permisos que un token o identidad puede ejercer.

### Mínimo privilegio

Principio según el cual una identidad recibe solo los permisos indispensables
para realizar su tarea.

### Política

Conjunto de reglas que permite, deniega o condiciona operaciones sobre
recursos o herramientas.

### Política determinista

Política cuya decisión se deriva de reglas verificables, no de una decisión
probabilística del modelo.

### Idempotencia

Propiedad de una operación que permite repetirla sin producir efectos
adicionales no deseados.

### Aislamiento

Separación que impide que el estado, memoria, credenciales o resultados de un
usuario, sesión o entorno se mezclen con los de otro.

### Identidad humana

Identidad de una persona que se autentica con contraseña, MFA o un proveedor
de identidad corporativo. Puede aportar factores de autenticación que una
carga de trabajo no tiene.

### Identidad de carga de trabajo

Identidad de un proceso, contenedor, función o agente que no tiene contraseña
ni MFA. Se autentica asumiendo un rol y recibe credenciales temporales del
entorno en el que se ejecuta.

### Credenciales de larga duración

Credenciales cuyo identificador y secreto no caducan y solo dejan de servir
cuando se revocan, como las access keys de un usuario de IAM. Al no estar
ligadas a un factor humano, una filtración conserva acceso hasta que se
detecta y se responde.

### Credenciales temporales

Credenciales formadas por identificador, secreto y token de sesión, con
caducidad explícita y duración máxima. Se obtienen al demostrar identidad y
caducan solas, de modo que el material en reposo es siempre de vida corta.

### Token de sesión

Elemento adicional de una credencial temporal que la vincula a una sesión
concreta y a su caducidad. Su presencia distingue una credencial temporal de
un par identificador/secreto permanente.

### Sesión

Intervalo durante el cual unas credenciales temporales concretas son válidas.
Incluye el inicio por autenticación, la renovación sin nuevo login, la
caducidad y el cierre o la revocación.

### Caducidad

Momento a partir del cual una credencial o sesión deja de ser aceptada. Limita
el daño de una filtración y explica la mayoría de fallos de autenticación
aparentemente repentinos.

### Revocación

Anulación explícita de una credencial, sesión o permiso antes de su caducidad.
Requiere poder identificar qué sesiones o claves existen; con credenciales de
larga duración es la única respuesta posible ante una filtración.

### Access key

Par de identificador y secreto de larga duración asociado a un usuario de IAM
o a la cuenta raíz. AWS no la recomienda para accesos humanos y la prohíbe
para la cuenta raíz.

### Usuario de IAM

Identidad de una cuenta de AWS con credenciales propias, opcionalmente con
acceso a la consola y MFA. Sirve para accesos humanos acotados, pero no escala
a varias cuentas ni a un directorio corporativo.

### Grupo de IAM

Conjunto de usuarios de IAM que comparten políticas. Asignar permisos al grupo
y no a cada usuario permite separar niveles de administración y de ejecución.

### Cuenta raíz

Identidad propietaria de la cuenta de AWS, con permisos totales no
restringibles. Se usa solo para tareas de cuenta, siempre con MFA y sin
credenciales programáticas.

### Principal

Sujeto que realiza una petición a AWS, como un usuario, un rol, un servicio o
una identidad federada. Las políticas de confianza y de recursos se escriben
en términos de principals.

### Rol de IAM

Identidad asumible que no tiene credenciales permanentes. Al asumirse entrega
credenciales temporales con los permisos del rol, y su política de confianza
define quién puede asumirlo.

### Política de confianza

Documento que define qué principals pueden asumir un rol y bajo qué
condiciones. Es la frontera real de seguridad del rol, con independencia de
los permisos que ese rol tenga.

### AWS STS

Servicio que emite credenciales temporales y evalúa las solicitudes de
asunción de roles. Es la pieza común a los roles, a las credenciales de carga
de trabajo y a la federación.

### MFA

Segundo factor que demuestra posesión de un dispositivo además de la
contraseña. Solo protege las operaciones que lo exigen: una access key creada
para un usuario con MFA no aplica ese factor al usarse.

### Federación de identidades

Confianza entre AWS y un proveedor de identidad externo, mediante SAML u
OIDC, para que sus usuarios asuman roles sin duplicar usuarios de IAM.

### Proveedor de identidad (IdP)

Sistema externo que autentica a las personas de una organización y emite
aserciones o tokens en los que AWS puede confiar.

### IAM Identity Center

Servicio de AWS que mantiene un directorio de identidades y asigna permisos
por cuenta mediante permission sets. Es la recomendación de AWS para accesos
humanos, sobre todo con varias cuentas o un IdP corporativo.

### Permission set

Plantilla de permisos de IAM Identity Center que se asigna a personas sobre
cuentas. Su efecto son credenciales temporales por cuenta, no un usuario de
IAM.

### AWS Builder ID

Identidad personal de AWS para herramientas para desarrolladores. No es una
cuenta de AWS ni permite operar recursos de una cuenta.

### IAM Roles Anywhere

Mecanismo que permite a servidores fuera de AWS obtener credenciales
temporales presentando certificados X.509 de una PKI propia. Sustituye las
access keys en infraestructura on-premise.

### Credenciales de consola

Mecanismo local que canjea la sesión de consola de un usuario, con contraseña
y MFA, por credenciales temporales para la CLI y los SDK. Evita crear access
keys y exige un permiso explícito que autorice el canje.

### Caché de sesión

Almacenamiento local, fuera del proyecto, donde la herramienta guarda la
autorización y las credenciales temporales. Caduca sola y su borrado equivale
a cerrar sesión.

### Perfil

Nombre que agrupa región y fuente de credenciales en la configuración
compartida. Un perfil moderno contiene referencias al mecanismo que produce
las credenciales, no secretos.

### Archivos de configuración compartida

Archivos locales, compartidos por la CLI, los SDK y herramientas como el
Toolkit de VS Code, donde se declaran perfiles y fuentes de credenciales.

### Cadena de resolución de credenciales

Orden fijo de fuentes que la CLI y los SDK consultan hasta encontrar
credenciales: invocación, variables de entorno, configuración compartida y
metadatos del entorno. Una fuente olvidada puede imponerse en silencio sobre
el perfil que se cree estar usando.

### Proceso de credenciales externo

Perfil que delega la obtención de credenciales en un programa local. Es un
adaptador para herramientas que no soportan un mecanismo de forma nativa, no
un mecanismo de autenticación propio.

### Rol de carga de trabajo

Rol que un servicio de AWS asigna a un recurso, como una instancia, una tarea,
un pod o una función, para entregar credenciales temporales al proceso sin
distribuir secretos.

## Despliegue y operación cloud

### Backend

Parte de una aplicación que procesa solicitudes, ejecuta lógica, accede a
servicios y produce respuestas para clientes u otros componentes.

### Workload

Carga de trabajo ejecutada por una aplicación, agente, servicio o proceso.

### Contenedor

Unidad aislada y reproducible que empaqueta una aplicación y sus dependencias
para ejecutarlas de forma consistente.

### Imagen de contenedor

Plantilla inmutable a partir de la cual se crean contenedores.

### Dockerfile

Archivo que declara los pasos para construir una imagen de contenedor.

### Amazon ECR

Amazon Elastic Container Registry, servicio administrado de AWS para
almacenar, publicar y distribuir imágenes de contenedor.

### Concurrencia

Cantidad de invocaciones o tareas que se procesan simultáneamente.

### Timeout

Límite de tiempo después del cual una operación se considera incompleta o
fallida.

### Reintento

Ejecución repetida de una operación después de un fallo. Debe limitarse a
errores transitorios y operaciones seguras o idempotentes.

### Backoff

Espera creciente entre reintentos para evitar sobrecargar un servicio que está
fallando o saturado.

### Degradación controlada

Comportamiento definido para continuar con capacidades reducidas cuando una
dependencia no está disponible, sin ocultar el fallo.

### Versionamiento

Identificación de cambios en código, imágenes, contratos, configuraciones,
herramientas, modelos o endpoints para poder comparar y revertir versiones.

### Rollback

Regreso controlado a una versión conocida y validada después de detectar un
problema en una actualización.

### Plano de control

Parte de una plataforma que administra configuración, recursos, permisos y
ciclo de vida.

### Plano de ejecución

Parte de una plataforma que procesa tráfico, invocaciones y operaciones de
negocio.

### Región, entorno y cuenta

Ámbitos que separan ubicación, configuración y recursos de una solución. Una
arquitectura debe distinguir desarrollo, pruebas y producción para evitar
mezclas accidentales.

## Observabilidad y calidad

### Observabilidad

Capacidad de inferir el estado interno de un sistema a partir de sus señales,
principalmente logs, métricas y trazas.

### Log

Registro de un evento con información como timestamp, severidad, componente,
versión y correlación.

### Métrica

Valor numérico agregado que permite observar volumen, latencia, errores, uso,
coste u otra propiedad a lo largo del tiempo.

### Traza

Representación de una operación completa a través de uno o varios servicios.

### Span

Unidad de trabajo dentro de una traza, como una llamada al modelo, Memory,
Gateway o una herramienta.

### Distributed tracing

Seguimiento de una operación distribuida entre varios servicios mediante
trazas, spans y correlación.

### OpenTelemetry

Estándar y conjunto de APIs, SDKs y herramientas para instrumentar y exportar
señales de observabilidad.

### Amazon CloudWatch

Servicio de AWS para recopilar, consultar, visualizar y alertar sobre métricas,
logs y eventos operativos.

### Correlación

Asociación de logs, métricas, spans, sesiones y versiones con una misma
invocación para facilitar el diagnóstico.

### Latencia

Tiempo transcurrido entre el inicio de una solicitud y la disponibilidad de su
respuesta o resultado.

### Evaluación

Proceso que analiza una interacción o ejecución con criterios y métricas para
determinar si cumple un objetivo.

### Métrica de calidad

Medida de propiedades deseadas de una respuesta o flujo, como exactitud,
relevancia, completitud, seguridad o uso correcto de herramientas.

### Regresión

Empeoramiento del comportamiento de una nueva versión respecto de una versión
anterior o de un criterio esperado.

### Muestreo

Selección de una parte de las interacciones para observación o evaluación,
especialmente cuando analizar todo el tráfico sería costoso o invasivo.

### Señal de observabilidad

Dato producido para explicar o medir una ejecución: log, métrica, traza,
evento o resultado de evaluación.
