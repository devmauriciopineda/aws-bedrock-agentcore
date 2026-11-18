# Capítulo 3: AgentCore Gateway e integración de herramientas

## Propósito

Al finalizar esta lectura podrás explicar cómo AgentCore Gateway desacopla un
agente de las herramientas que utiliza, distinguir herramientas locales de
remotas y describir el papel de Model Context Protocol (MCP). También podrás
analizar targets, endpoints, esquemas, autenticación, errores, permisos y
versiones antes de integrar una herramienta con Python o LangGraph.

## 1. Herramientas en una arquitectura de agentes

Una **herramienta** es una operación que el agente puede solicitar para
obtener información o producir un efecto fuera de su propio proceso. Ejemplos:
consultar una política, buscar un pedido o calcular una cotización. Una
herramienta debe tener un propósito acotado, entradas y salidas definidas y
reglas explícitas sobre errores y autorización.

El modelo puede proponer una llamada, pero la aplicación y la infraestructura
deben decidir si esa llamada es válida y si puede ejecutarse. No se debe
interpretar la selección de una herramienta por parte del modelo como una
autorización.

Una herramienta puede vivir:

- **Localmente**, dentro del mismo proceso del agente. Es simple de invocar y
  probar, pero comparte despliegue, dependencias y superficie de seguridad.
- **Remotamente**, detrás de una API, una función o un servidor de
  herramientas. Puede ser compartida y desplegarse de forma independiente,
  pero necesita red, autenticación, observabilidad, control de errores y
  versionamiento.

La elección depende del acoplamiento, sensibilidad de los datos, frecuencia de
reutilización, latencia y necesidad de separar permisos. Gateway se vuelve
especialmente útil cuando las herramientas remotas deben ofrecer una interfaz
común a varios agentes.

## 2. Arquitectura de AgentCore Gateway

**AgentCore Gateway** es una capa administrada que presenta herramientas a los
agentes y conecta esas herramientas con implementaciones externas. Su función
principal es separar el contrato que consume el agente de los detalles de
cada backend.

En un flujo típico:

1. El agente obtiene el catálogo de herramientas disponibles.
2. Selecciona una herramienta y construye argumentos según su esquema.
3. Envía la solicitud al Gateway.
4. Gateway identifica el target y aplica autenticación, autorización y
   configuración de la integración.
5. El target invoca la API REST, función Lambda o servidor MCP.
6. Gateway normaliza el resultado o el error.
7. El agente recibe el resultado y decide el siguiente paso.

Un **target** es la configuración que conecta una herramienta publicada por
Gateway con su implementación real. Un **endpoint** es un destino identificable
para recibir solicitudes. En conjunto, el Gateway puede actuar como frontera
de integración sin obligar al agente a conocer cada URL, función o protocolo
interno.

Gateway no convierte una herramienta insegura en segura automáticamente. La
implementación debe validar entradas, limitar efectos, proteger datos y
producir respuestas confiables.

## 3. Model Context Protocol (MCP)

**Model Context Protocol (MCP)** es un protocolo para describir y exponer
herramientas y recursos que un cliente compatible puede descubrir y utilizar.
Un **servidor MCP** ofrece capacidades; un **cliente MCP** las descubre y
solicita. En esta relación, el agente o un adaptador puede actuar como cliente,
mientras que Gateway conecta con el servidor o lo presenta mediante un target.

MCP aporta un vocabulario común para:

- identificar herramientas;
- describir nombres y propósitos;
- declarar esquemas de entrada;
- transportar solicitudes y resultados;
- comunicar errores.

El protocolo reduce acoplamiento, pero no elimina la necesidad de diseñar
contratos. Un nombre claro y un esquema preciso ayudan al modelo a elegir una
herramienta; no garantizan que la operación sea correcta o segura.

## 4. Targets, endpoints y descubrimiento

El **descubrimiento de herramientas** es el proceso mediante el cual el cliente
conoce qué herramientas existen, qué hacen y qué argumentos aceptan. El
catálogo descubierto debe incluir al menos nombre, descripción, esquema de
entrada y restricciones relevantes.

La descripción debe ser:

- específica sobre el objetivo de la herramienta;
- clara sobre unidades, formatos y campos obligatorios;
- explícita sobre efectos secundarios;
- libre de instrucciones ambiguas;
- estable entre versiones compatibles.

Los **esquemas de entrada y salida** son contratos estructurados. Un esquema
de entrada debe impedir que una herramienta reciba datos incompletos o de tipo
incorrecto. Un esquema de salida permite al agente distinguir un resultado
válido de un mensaje de error.

El catálogo no debería publicar herramientas que el agente no puede usar.
Exponer demasiadas herramientas aumenta la ambigüedad de selección y la
superficie de permisos. Organizar el catálogo por dominios facilita aplicar
límites y revisar cambios.

## 5. Integración de APIs REST

Una **API REST** expone operaciones mediante recursos HTTP y métodos
estandarizados. Para conectarla a Gateway, se debe definir cómo cada
herramienta se traduce a una operación concreta:

1. Nombre y descripción de la herramienta.
2. Campos de entrada y su transformación a ruta, query, headers o body.
3. Autenticación requerida.
4. Códigos de éxito y error.
5. Forma de la respuesta que se devuelve al agente.
6. Timeouts, reintentos e idempotencia.

La herramienta no debe permitir que el modelo construya libremente una URL o
headers sensibles. El target debe controlar el destino y la transformación.
También debe evitar copiar tokens o datos privados en respuestas, logs o
mensajes para el modelo.

## 6. Integración de funciones Lambda

**AWS Lambda** es un servicio de ejecución de funciones sin administrar
servidores. Una función Lambda puede implementar una herramienta cuando la
operación es acotada, usa servicios de AWS o necesita escalar según demanda.

El contrato de la herramienta debe traducirse a un evento de Lambda y la
respuesta de la función debe traducirse a un resultado estable. La función
debe validar de nuevo sus entradas: la validación del catálogo o del Gateway
no reemplaza la defensa en profundidad del backend.

Considera límites de duración, tamaño de eventos, dependencias, concurrencia y
errores transitorios. Si una operación tiene efectos secundarios, define
idempotencia antes de habilitar reintentos.

## 7. Integración de servidores MCP existentes

Un servidor MCP existente ya implementa un contrato de herramientas compatible
con MCP. Gateway puede conectarlo mediante un target, de manera que el agente
consuma las herramientas sin conocer la ubicación concreta del servidor.

Antes de conectarlo, verifica:

- procedencia y mantenimiento del servidor;
- herramientas que publica y permisos que requieren;
- datos que recibe y devuelve;
- autenticación del canal;
- aislamiento de red;
- comportamiento ante errores y límites;
- compatibilidad de versiones del protocolo y esquemas.

Un servidor MCP de terceros debe tratarse como una dependencia externa. La
compatibilidad técnica no equivale a confianza operacional.

## 8. Autenticación y autorización

La **autenticación** identifica al cliente o servicio que solicita una
operación. La **autorización** decide si esa identidad puede realizarla.
Gateway puede participar en ambas, pero la decisión final debe estar alineada
con las políticas de AWS y con las reglas del backend.

Analiza por separado:

1. Quién invoca Gateway.
2. Qué identidad utiliza Gateway frente al target.
3. Qué identidad observa la API o función de destino.
4. Qué recursos y operaciones puede utilizar cada identidad.

No uses las credenciales del usuario final como credenciales generales del
agente sin una razón clara. Tampoco otorgues a un agente permisos amplios solo
porque necesita una herramienta de lectura.

Un diseño de mínimo privilegio puede separar dominios: un agente que consulta
políticas no necesita permisos para modificar nóminas. Las operaciones
sensibles pueden exigir validación adicional, aprobación humana o políticas
deterministas.

## 9. Descubrimiento e invocación desde Python

Un cliente Python debe tratar el catálogo como datos no confiables que deben
validarse contra las capacidades permitidas de la aplicación. Un flujo básico
es:

1. Obtener o configurar el catálogo de herramientas.
2. Filtrar herramientas permitidas para el agente y el usuario.
3. Validar argumentos según el esquema.
4. Invocar la herramienta mediante el cliente o adaptador correspondiente.
5. Validar el resultado.
6. Convertir el resultado a un tipo que el agente pueda procesar.
7. Registrar la operación sin datos sensibles.

El cliente debe tener timeout, clasificación de errores y una política de
reintentos. Un fallo de validación no debe reintentarse; un timeout puede ser
transitorio, pero solo debe reintentarse si la operación es segura o
idempotente.

El resultado que recibe el agente debe distinguir entre:

- datos obtenidos correctamente;
- ausencia legítima de datos;
- rechazo por autorización;
- error transitorio;
- error permanente del contrato o del backend.

## 10. Adaptación para LangGraph

LangGraph representa el flujo como un grafo con estado. Para consumir
herramientas de Gateway, el adaptador debe convertir la descripción y el
resultado remoto a los tipos que esperan los nodos:

1. Seleccionar las herramientas permitidas para el grafo.
2. Exponer nombres y esquemas compatibles con el nodo que decide la llamada.
3. Validar argumentos antes de enviar la solicitud.
4. Ejecutar la llamada remota desde un nodo o componente de herramientas.
5. Guardar resultado, error y metadata de correlación en el estado.
6. Permitir que el grafo decida si continúa, responde o solicita otra acción.

El grafo no debe incorporar URLs, secretos ni reglas de autenticación
específicas del target. Esa configuración pertenece al adaptador o a la capa
de infraestructura. Así se puede sustituir una implementación local por una
remota sin cambiar el flujo de decisión.

## 11. Resultados, errores y reintentos

Una herramienta remota añade fallos de red, autenticación, cuota, timeout y
versiones incompatibles. Diseña los errores como parte del contrato:

- **Validación:** argumentos ausentes o incorrectos; corregir antes de llamar.
- **Autorización:** identidad sin permiso; no insistir con reintentos.
- **No encontrado:** recurso inexistente; informar o tomar una ruta alternativa.
- **Transitorio:** timeout, saturación o indisponibilidad temporal; reintentar
  con límites y backoff si la operación lo permite.
- **Backend:** error interno del destino; conservar correlación y evitar
  ocultarlo como resultado válido.

El agente debe recibir información suficiente para decidir, no una traza
interna completa. Gateway, cliente y backend deben compartir un identificador
de correlación para diagnosticar el recorrido completo.

## 12. Herramientas compartidas, dominios y versiones

Una herramienta compartida entre agentes debe tener un contrato estable,
propietario identificado y permisos explícitos. Compartir no significa dar a
todos los agentes el mismo acceso.

La separación por **dominios funcionales** agrupa herramientas relacionadas:
viajes, inventario, facturación o soporte. Cada dominio puede tener su
catálogo, identidad y reglas de autorización. Esto reduce el alcance de un
error y facilita la revisión.

El **versionamiento** debe cubrir nombre, esquema y comportamiento. Un cambio
que elimina un campo o modifica el significado de una operación puede romper
agentes aunque la solicitud siga siendo técnicamente válida. Usa versiones
compatibles cuando sea posible, publica cambios incompatibles como una nueva
versión y retira la anterior de forma planificada.

## Método para diseñar una integración

Aplica esta secuencia antes de publicar una herramienta:

1. Define la acción y su efecto observable.
2. Decide si debe ser local o remota.
3. Especifica entrada, salida, errores, timeout e idempotencia.
4. Elige el target y el backend: REST, Lambda o servidor MCP.
5. Define identidades, permisos y datos que pueden cruzar la frontera.
6. Limita el catálogo a las herramientas necesarias.
7. Adapta el contrato a Python y al estado de LangGraph.
8. Prueba éxito, validación, autorización, timeout y versión incompatible.
9. Observa latencia, errores y uso sin registrar secretos.
10. Documenta propietario, versión y plan de retirada.

## Cierre

Gateway y MCP permiten que un agente consuma herramientas remotas mediante
contratos explícitos, pero la abstracción no elimina las responsabilidades de
seguridad, validación y operación. Un buen diseño limita el catálogo, separa
dominios, clasifica errores y versiona cambios.

En el siguiente capítulo se estudiará AgentCore Memory. La distinción entre
resultado de una herramienta, estado de una sesión y memoria persistente será
fundamental para evitar que una respuesta remota se convierta
automáticamente en contexto permanente.
