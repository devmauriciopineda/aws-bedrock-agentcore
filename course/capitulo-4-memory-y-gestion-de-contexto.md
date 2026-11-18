# Capítulo 4: AgentCore Memory y gestión de contexto

## Propósito

Al finalizar esta lectura podrás distinguir el estado de una invocación, una
sesión conversacional y una memoria persistente. También podrás organizar
eventos mediante Memory ID, Actor ID, Session ID y namespaces, elegir una
estrategia de memoria y explicar cómo recuperar información relevante e
integrarla con un agente LangGraph sin mezclar datos entre usuarios.

## 1. Contexto, estado y memoria

Un agente necesita contexto para interpretar una solicitud, pero no todo el
contexto debe conservarse. Conviene separar tres niveles:

- **Estado de invocación:** datos necesarios para una llamada individual.
  Puede descartarse al terminar.
- **Estado de sesión:** información que relaciona varias invocaciones de una
  conversación o flujo.
- **Memoria persistente:** información seleccionada para recuperarse en
  interacciones futuras, incluso después de que termine una sesión.

**AgentCore Memory** proporciona capacidades para registrar y recuperar
información de las interacciones del agente. No es una instrucción para guardar
todo lo que el usuario diga. La aplicación debe definir qué eventos registra,
qué información puede transformarse en memoria, durante cuánto tiempo es
válida y en qué situaciones puede recuperarse.

La memoria mejora continuidad, pero añade riesgos: datos obsoletos,
información sensible, contaminación entre usuarios, recuperación irrelevante y
costes de almacenamiento o procesamiento. Diseñar memoria es diseñar también
sus límites.

## 2. Arquitectura conceptual de AgentCore Memory

Una arquitectura de memoria suele contener:

1. Una aplicación que decide qué eventos enviar y cuándo consultar.
2. Un recurso de memoria que define el espacio lógico y su configuración.
3. Identidades que autorizan el registro y la recuperación.
4. Eventos asociados con un actor y una sesión.
5. Estrategias que transforman o estructuran información útil.
6. Una recuperación que devuelve recuerdos candidatos al agente.
7. El agente, que decide cómo incorporar esos recuerdos al contexto actual.

La memoria debe considerarse una dependencia del agente, no una fuente
infalible. El agente debe poder continuar o pedir confirmación cuando no hay
recuerdos, cuando son contradictorios o cuando su antigüedad los vuelve
inseguros.

## 3. Memory ID, Actor ID y Session ID

### Memory ID

**Memory ID** identifica el recurso o espacio de memoria donde se registran y
recuperan eventos. Define el ámbito lógico de una configuración de memoria.
Una aplicación debe elegirlo de forma consistente y no intercambiarlo
accidentalmente entre entornos o dominios.

Separar memoria de desarrollo, pruebas y producción evita que los datos de un
entorno contaminen otro. También puede ser conveniente separar dominios con
requisitos de retención o acceso diferentes.

### Actor ID

**Actor ID** identifica al actor al que pertenece una memoria, normalmente un
usuario, cliente, organización o entidad de negocio. Su significado debe
documentarse: no uses un identificador de sesión como actor si necesitas
conservar información entre sesiones.

El Actor ID debe ser estable dentro del ámbito autorizado, pero no debe
contener datos personales innecesarios. Cuando sea posible, utiliza un
identificador interno o pseudónimo en lugar de un correo o nombre completo.

### Session ID

**Session ID** identifica una conversación o flujo concreto de un actor. Permite
separar eventos de distintas interacciones y reconstruir el contexto de una
sesión.

Un mismo Actor ID puede tener muchas sesiones. El aislamiento requiere validar
que cada Session ID pertenece al actor autenticado y que una solicitud no
puede consultar sesiones de otro actor.

La relación conceptual es:

```text
Memory ID
└── Actor ID
    ├── Session ID A
    └── Session ID B
```

La forma exacta de organizar los recursos depende de la configuración y las
interfaces utilizadas, pero la regla de diseño permanece: memoria, actor y
sesión deben tener responsabilidades distintas.

## 4. Eventos, conversaciones y namespaces

Un **evento** es un hecho registrado durante una interacción, como un mensaje
del usuario, una respuesta del agente, una llamada de herramienta o un
resultado relevante. Un evento debe incluir solo la información necesaria para
su propósito y mantener una asociación clara con actor y sesión.

Una **conversación** es la secuencia relacionada de mensajes y eventos de una
sesión. Registrar la conversación completa puede ser útil para auditoría o
reproducción, pero no implica que todo deba recuperarse como contexto en cada
solicitud.

Un **namespace** es un espacio lógico para organizar, segmentar y consultar
tipos de memoria. Puede separar preferencias, resúmenes, hechos de dominio o
recuerdos de una aplicación. Los namespaces ayudan a controlar recuperación y
retención, pero no deben confundirse con una frontera de seguridad por sí
solos. La autorización y el aislamiento de identidades siguen siendo
necesarios.

Ejemplo conceptual:

```text
preferences      -> idioma y formato preferidos
session-summary  -> resumen de una conversación
domain-facts     -> hechos útiles y validados
```

El nombre del namespace debe indicar propósito y reglas. Evita un namespace
genérico donde se mezclen instrucciones, preferencias, hechos y datos
sensibles sin distinguir su nivel de confianza.

## 5. Memoria de corto y largo plazo

La **memoria de corto plazo** mantiene el contexto de una conversación activa:
mensajes recientes, decisiones provisionales y resultados necesarios para el
siguiente paso. Se asocia normalmente con una sesión y puede perder utilidad
cuando el flujo termina.

La **memoria de largo plazo** conserva información seleccionada para futuras
sesiones: una preferencia estable, un resumen validado o un hecho de dominio
que el usuario espera reutilizar.

La diferencia no es solo cuánto tiempo se conserva un dato:

| Aspecto | Corto plazo | Largo plazo |
|---|---|---|
| Ámbito | Sesión activa | Varias sesiones |
| Contenido | Contexto reciente | Información seleccionada |
| Riesgo | Ventana grande de contexto | Persistencia de datos incorrectos |
| Gestión | Recorte, orden y resumen | Validación, retención y actualización |
| Recuperación | Casi inmediata y contextual | Selectiva y relevante |

No conviertas automáticamente cada mensaje en memoria de largo plazo. La
persistencia debe justificar su utilidad y cumplir las reglas de privacidad del
caso de uso.

## 6. Estrategias de memoria

Una **estrategia de memoria** define cómo se transforma una secuencia de
eventos en información que puede recuperarse. Las estrategias disponibles
dependen de la configuración y versión del servicio, pero conceptualmente
pueden incluir:

- **Registro de eventos:** conserva mensajes o hechos tal como ocurrieron.
- **Resumen:** comprime una conversación para reducir contexto sin conservar
  todos los turnos.
- **Preferencias:** extrae elecciones relativamente estables del usuario.
- **Memoria semántica:** representa hechos o contenidos para recuperarlos por
  significado, no solo por coincidencia literal.

Cada estrategia tiene límites. Un resumen puede omitir una condición
importante; una preferencia puede dejar de ser válida; una memoria semántica
puede recuperar un hecho parecido pero incorrecto. La aplicación debe incluir
fecha, fuente, confianza o versión cuando esa información sea necesaria para
validar el recuerdo.

## 7. Registro de eventos

Registrar un evento significa enviar a Memory una representación de algo que
ocurrió. El momento y la selección son decisiones de aplicación:

1. Identifica el actor y la sesión autenticados.
2. Clasifica el evento: mensaje, respuesta, herramienta, resumen o hecho.
3. Elimina secretos y datos que no deban persistir.
4. Asigna el namespace y metadata necesarios.
5. Registra el evento con una correlación estable.
6. Maneja explícitamente errores de escritura.

La escritura no debe bloquear de forma silenciosa el resultado del agente.
Define si un fallo de memoria impide la respuesta, genera una advertencia o se
reintenta. La decisión depende de si la memoria es esencial para la seguridad o
solo mejora la experiencia.

## 8. Recuperación de información relevante

Recuperar memoria es buscar candidatos útiles para una solicitud actual. El
resultado debe filtrarse por actor, sesión, namespace, vigencia y propósito
antes de incorporarlo al contexto.

Una secuencia segura es:

1. Autenticar al actor actual.
2. Construir una consulta basada en la solicitud y el dominio.
3. Limitar el ámbito de búsqueda al Memory ID y Actor ID correctos.
4. Elegir namespaces permitidos.
5. Recuperar un conjunto acotado de candidatos.
6. Filtrar datos obsoletos, contradictorios o insuficientemente confiables.
7. Etiquetar el contenido como memoria recuperada.
8. Incorporarlo al contexto solo si es relevante.

La recuperación no debe convertirse en una instrucción con autoridad
automática. Un recuerdo puede contener texto generado por el usuario o por un
modelo; debe tratarse como dato, no como una orden que ignore políticas o
controles de la aplicación.

## 9. Resúmenes, preferencias y memorias semánticas

### Resúmenes

Un **resumen** conserva una versión compacta de una conversación. Debe
preservar decisiones, restricciones y hechos necesarios, pero marcar lo que
sea incierto. Actualizarlo repetidamente puede acumular errores; conviene
conservar la fuente o permitir reconstruirlo cuando el caso lo exija.

### Preferencias

Una **preferencia** expresa una elección del usuario, como idioma o formato de
respuesta. No toda afirmación es una preferencia permanente. Antes de guardar
una, define evidencia, alcance y mecanismo de actualización o eliminación.

### Memorias semánticas

Una **memoria semántica** representa contenido recuperable por significado.
Puede encontrar información relacionada aunque las palabras no coincidan
exactamente. Esa flexibilidad exige validar relevancia y evitar que similitud
lingüística se interprete como identidad del hecho.

## 10. Integración con LangGraph

LangGraph mantiene un estado de ejecución propio. AgentCore Memory mantiene
información que puede sobrevivir a una invocación o sesión. El adaptador debe
conectar ambos sin confundirlos:

1. Recibe payload, Actor ID y Session ID validados.
2. Recupera memoria relevante antes de iniciar el grafo.
3. Inserta recuerdos en un campo diferenciado del estado.
4. Ejecuta el grafo, sin permitir que un recuerdo sobreescriba controles del
   sistema.
5. Selecciona la respuesta externa.
6. Registra nuevos eventos y, si corresponde, actualiza memoria de largo plazo.

El estado del grafo puede contener mensajes temporales, resultados de
herramientas y decisiones de la invocación. La memoria recuperada debe estar
identificada por fuente y tipo para que los nodos puedan distinguirla de una
instrucción del sistema o de un dato nuevo del usuario.

Una integración robusta también define qué ocurre si Memory está indisponible:
continuar sin recuerdos, usar solo el contexto de sesión, devolver un error
controlado o impedir una acción sensible. No existe una respuesta universal;
debe elegirse según el riesgo del caso de uso.

## 11. Aislamiento entre usuarios

El **aislamiento de memoria** impide que un usuario consulte o influya en la
memoria de otro. Debe aplicarse en varias capas:

- validar la identidad antes de aceptar Actor ID;
- no permitir que el usuario elija libremente otro Actor ID;
- asociar Session ID con el actor autenticado;
- filtrar cada recuperación por el ámbito autorizado;
- separar entornos y dominios cuando sea necesario;
- no incluir memoria de un usuario en logs accesibles a otro;
- probar accesos cruzados de lectura y escritura;
- definir eliminación, retención y corrección de datos.

El aislamiento no se demuestra con una sola prueba feliz. Debe probarse con
sesiones concurrentes, identificadores manipulados, namespaces no autorizados
y respuestas que contengan información parecida pero perteneciente a otra
persona.

## Método para diseñar memoria

Antes de persistir un dato, responde:

1. ¿Qué problema resuelve conservarlo?
2. ¿Pertenece a la invocación, sesión o largo plazo?
3. ¿A qué actor y namespace pertenece?
4. ¿Qué fuente, vigencia y confianza tiene?
5. ¿Quién puede leerlo, actualizarlo y eliminarlo?
6. ¿Qué ocurre si está ausente, obsoleto o equivocado?
7. ¿Cómo se evita que se convierta en una instrucción no confiable?
8. ¿Qué prueba demuestra el aislamiento?

Después define el flujo de lectura y escritura, la política de retención y los
casos en los que la memoria no debe utilizarse.

## Cierre

AgentCore Memory ayuda a conservar contexto, pero no reemplaza el diseño de
estado ni la validación del agente. Memory ID, Actor ID, Session ID y
namespaces organizan el ámbito; los eventos son la fuente registrada; las
estrategias convierten eventos en recuerdos recuperables.

En el siguiente capítulo se estudiarán Identity, Policy, Observability y
Evaluations. Esos controles completarán la protección, trazabilidad y medición
de los flujos de memoria y de las herramientas.
