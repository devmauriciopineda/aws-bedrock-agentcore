# Plan de estudio: AWS Bedrock AgentCore

Este plan está dirigido a desarrolladores backend con experiencia en Python,
inteligencia artificial, LLM, RAG y agentes, especialmente LangGraph y
CrewAI, así como conocimientos prácticos de AWS. El objetivo es aprender a
utilizar Amazon Bedrock AgentCore sin repetir fundamentos que ya forman parte
de ese perfil. La formación se centra en sus componentes, SDK, APIs,
integración y operación.

**Duración:** 6 capítulos  
**Dedicación:** 20 horas  
**Total:** 20 horas  
**Enfoque:** desarrollo backend, agentes de IA, integración de herramientas,
memoria, seguridad, observabilidad, evaluación y puesta en producción.

---

## Capítulo 1: Arquitectura y fundamentos de AgentCore

**Duración:** 2 horas

**Objetivo:** Comprender la arquitectura de AgentCore, las responsabilidades de
sus componentes y cómo encajan con una aplicación Python y un framework de
agentes existente.

**Temario:**
- Arquitectura general de Amazon Bedrock AgentCore.
- Responsabilidades y casos de uso de Runtime, Gateway, Memory, Identity,
  Policy, Observability y Evaluations.
- Capacidades adicionales: Browser y Code Interpreter.
- Diferencias entre AgentCore Runtime y AgentCore Harness.
- SDK de Python, CLI y APIs de AWS.
- Plano de control frente a plano de ejecución.
- Preparación del entorno: región, credenciales, permisos mínimos, instalación
  del SDK y CLI, y acceso al modelo de Bedrock.

---

## Capítulo 2: AgentCore Runtime y despliegue de agentes

**Duración:** 4 horas

**Objetivo:** Adaptar un agente Python existente y desplegarlo en AgentCore
Runtime, comprendiendo su contrato de ejecución, sesiones y opciones de
invocación.

**Temario:**
- Arquitectura y modelo de ejecución de Runtime.
- Ciclo de vida de una invocación.
- Contrato de entrada y salida del agente.
- Identificadores de sesión y aislamiento entre sesiones.
- Endpoints, versiones e invocaciones síncronas, asíncronas y streaming.
- Uso de `BedrockAgentCoreApp` y del decorador `@app.entrypoint`.
- Manejo de payloads, respuestas estructuradas y errores.
- Adaptación e integración de un agente LangGraph.
- Creación y configuración del proyecto mediante AgentCore CLI.
- Preparación de contenedores, publicación de imágenes en ECR y despliegue.
- Invocación desde un cliente Python mediante Boto3.
- Actualización de versiones y administración de endpoints.
- Concurrencia, estado entre invocaciones, streaming y límites operativos.

---

## Capítulo 3: AgentCore Gateway e integración de herramientas

**Duración:** 4 horas

**Objetivo:** Exponer herramientas mediante AgentCore Gateway y consumirlas
desde un agente, utilizando MCP para desacoplar las herramientas de la lógica
de orquestación.

**Temario:**
- Arquitectura de Gateway y relación con Model Context Protocol (MCP).
- Diferencias entre herramientas locales y remotas.
- Targets, endpoints, descubrimiento de herramientas y esquemas de entrada y
  salida.
- Exposición de APIs REST, funciones Lambda y servidores MCP existentes.
- Configuración de targets, autenticación y autorización.
- Descubrimiento e invocación de herramientas desde Python.
- Conversión de herramientas MCP para su consumo desde LangGraph.
- Manejo de resultados y errores de herramientas.
- Diseño de herramientas compartidas entre agentes.
- Separación por dominios funcionales, control de permisos y versionamiento.

---

## Capítulo 4: AgentCore Memory y gestión de contexto

**Duración:** 3 horas

**Objetivo:** Implementar memoria conversacional y persistente con AgentCore
Memory e integrarla con un agente LangGraph.

**Temario:**
- Arquitectura de AgentCore Memory.
- Recursos de memoria e identificadores Memory ID, Actor ID y Session ID.
- Eventos, conversaciones y namespaces.
- Diferencias entre memoria de corto y largo plazo.
- Estrategias de memoria disponibles.
- Registro y recuperación de eventos conversacionales.
- Asociación de memoria con usuarios y sesiones.
- Resúmenes, preferencias y memorias semánticas.
- Recuperación de información relevante entre sesiones.
- Integración de Memory con LangGraph.
- Incorporación de memorias recuperadas al contexto del agente y persistencia de
  nuevos eventos.
- Aislamiento de memoria entre usuarios.

---

## Capítulo 5: Seguridad, observabilidad y evaluación

**Duración:** 4 horas

**Objetivo:** Aplicar controles de acceso y autorización, instrumentar las
ejecuciones y evaluar el comportamiento del agente mediante las capacidades de
AgentCore.

**Temario:**
- AgentCore Identity: identidad del agente, autenticación inbound y outbound,
  OAuth, API keys y credenciales.
- Diferencias entre la identidad del cliente y las credenciales utilizadas por
  el agente.
- AgentCore Policy: políticas de acceso a herramientas, autorización de
  acciones y controles deterministas.
- Aplicación de políticas en Gateway y restricciones sobre operaciones
  sensibles.
- AgentCore Observability: integración con CloudWatch y OpenTelemetry.
- Distributed tracing, trazas, spans, métricas y logs.
- Seguimiento de sesiones, latencia y errores.
- Diagnóstico de problemas en orquestación, inferencia, memoria y
  herramientas.
- AgentCore Evaluations: evaluación bajo demanda y online.
- Métricas de calidad, uso de herramientas y resultados.
- Instrumentación y ejecución de evaluaciones sobre interacciones del agente.

---

## Capítulo 6: Proyecto integrador y puesta en producción

**Duración:** 3 horas

**Objetivo:** Integrar los componentes estudiados en una aplicación funcional y
revisar los aspectos esenciales para operarla en un entorno productivo.

**Temario:**
- Diseño de una arquitectura de referencia con backend Python, Runtime,
  Gateway, Memory, Identity, Policy, Amazon Bedrock y observabilidad.
- Integración de LangGraph como framework de orquestación.
- Conexión de herramientas remotas mediante Gateway y MCP.
- Persistencia y recuperación de memoria entre sesiones.
- Configuración de autenticación y autorización.
- Instrumentación de trazas y métricas.
- Ejecución de evaluaciones del agente.
- Versionamiento y actualización de agentes y endpoints.
- Manejo de errores y reintentos.
- Optimización de latencia y concurrencia.
- Análisis de consumo y costes.
- Limpieza de recursos de prueba.
