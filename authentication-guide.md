# Guía teórica: autenticación en AWS

Documento de referencia conceptual para el plan de estudio de AWS Bedrock
AgentCore. Explica qué es una credencial, qué mecanismos de autenticación
existen hoy en AWS, cómo funcionan por dentro y cuándo tiene sentido cada uno.
No es un tutorial de comandos: los procedimientos concretos están en las guías
de cada capítulo, como
`course/entregas/capitulo-1/capitulo-1-aws-guide.md`.

## 1. Las dos preguntas que resuelve la autenticación

Toda llamada a la API de AWS responde, en el servidor, a dos preguntas
distintas y encadenadas:

- **Autenticación**: ¿quién está llamando? ¿Puede demostrarlo?
- **Autorización**: ¿qué le está permitido hacer a esa identidad?

Son problemas separados y se resuelven con piezas separadas. La autenticación
produce una **credencial**; la autorización la evalúa contra **políticas**. Un
error frecuente consiste en mezclarlas: dar más permisos para "arreglar" un
fallo de credenciales, o usar una credencial más potente para evitar definir
bien los permisos.

Este documento trata sobre todo la primera pregunta.

## 2. Conceptos base

### 2.1 Credencial

Conjunto de datos que una herramienta presenta a AWS para demostrar que actúa
en nombre de una identidad. Para la API de AWS una credencial utilizable se
compone de tres elementos:

- **Identificador** de la credencial (público, viaja en cada petición).
- **Secreto** (privado, se usa para firmar la petición; nunca debe
  transmitirse tal cual).
- **Token de sesión** (solo en credenciales temporales; indica que la
  credencial va asociada a una sesión concreta y con caducidad).

Las peticiones se firman criptográficamente con el secreto. Por eso el secreto
nunca se envía: se usa localmente para calcular una firma que el servidor
puede verificar. De ahí que "filtrar una credencial" signifique, en la
práctica, filtrar el par identificador/secreto.

### 2.2 Credenciales de larga duración

El identificador y el secreto no caducan. Solo dejan de servir cuando alguien
las revoca explícitamente. Las access keys de un usuario de IAM son el ejemplo
clásico.

Sus propiedades implacables:

- No están ligadas a un factor de autenticación humano: no hay MFA asociado.
- No caducan si se filtran; el atacante conserva acceso hasta que se detecte y
  se revoque.
- Suelen copiarse entre máquinas, archivos `.env`, imágenes de contenedor y
  repositorios, multiplicando los lugares donde pueden filtrarse.
- No distinguen "quién" de "qué": todos los usos de una misma access key son
  indistinguibles en los registros.

Por eso AWS desaconseja su creación para personas, y prohíbe las de la cuenta
raíz en cualquier escenario.

### 2.3 Credenciales temporales

Conjunto identificador + secreto + token de sesión, con una hora de caducidad
explícita y una duración máxima. Se obtienen a cambio de demostrar identidad,
no se crean a mano y caducan solas.

Propiedades:

- **Caducidad obligatoria**: de minutos a un máximo de horas, según el
  mecanismo.
- **Vinculadas a una sesión**: AWS sabe para qué identidad y qué rol se
  emitieron; quedan registradas como sesión, no como "usuario genérico".
- **Revocables por vía de la sesión o del rol**, sin tocar secretos.
- **Rotación constante**: la herramienta que las obtiene las renueva antes de
  que expiren, de modo que en disco solo hay material de vida corta.

El objetivo de cualquier diseño de autenticación moderno es que **en reposo
solo exista material de corta duración, y que para obtenerlo haya que pasar
por un control de identidad fuerte**.

### 2.4 Identidad

Sujeto al que AWS le reconoce credenciales y le aplica políticas. Hay dos
familias que conviene no confundir:

- **Identidades humanas** (workforce): personas que se autentican con
  contraseña, MFA o un proveedor de identidad corporativo.
- **Identidades de carga de trabajo** (workload): procesos, contenedores,
  funciones y agentes que no tienen contraseña ni MFA. Se autentican mediante
  roles asumidos dentro de AWS.

Los mecanismos son distintos porque el riesgo es distinto: una persona puede
teclear un segundo factor; un contenedor que arranca mil veces por hora no.

### 2.5 Principal, política y rol

- **Principal**: quien realiza la petición. Puede ser un usuario, un rol, un
  servicio de AWS o una identidad federada.
- **Política**: documento que concede o niega acciones sobre recursos. Las
  políticas de identidad dicen qué puede hacer un principal; las de recurso
  dicen quién puede entrar a ese recurso.
- **Rol**: identidad sin credenciales permanentes. Se **asume** mediante STS;
  a cambio se reciben credenciales temporales de ese rol. Su **política de
  confianza** define quién puede asumirlo.

El rol es la pieza que permite separar "quién eres" de "qué puedes hacer": una
misma persona o servicio puede asumir roles distintos con permisos distintos,
sin crear credenciales nuevas de larga duración.

### 2.6 MFA

Segundo factor que demuestra posesión de un dispositivo. Su valor teórico: una
credencial filtrada, sin el segundo factor, no sirve.

Consecuencia importante: un factor solo protege lo que lo exige. Una access
key creada para un usuario con MFA **no** aplica MFA al usarse. Por eso existen
políticas que condicionan permisos a que la sesión esté autenticada con MFA;
son la forma de trasladar esa garantía a las credenciales temporales.

### 2.7 Sesión

Intervalo durante el cual unas credenciales temporales concretas son válidas.
Una sesión tiene inicio (autenticación), renovación (nuevas credenciales sin
volver a autenticarse, mientras la sesión viva), fin por caducidad y revocación
explícita. Casi todos los problemas de "mi CLI dejó de funcionar" son, en
realidad, sesiones caducadas.

## 3. Mecanismos de autenticación disponibles

### 3.1 Access keys de usuario de IAM

Mecanismo histórico: se crean pares de clave permanente para un usuario y se
distribuyen a las herramientas.

- Ventaja: trivial de configurar, funciona en cualquier entorno.
- Inconvenientes: todos los descritos en 2.2.
- Estado actual: AWS lo mantiene por compatibilidad, no lo recomienda para
  accesos humanos, y lo prohíbe para la cuenta raíz.

Sigue siendo legítimo en casos muy acotados (una integración heredada que no
admite otra cosa), nunca como opción por defecto.

### 3.2 IAM Identity Center (SSO)

Es la recomendación de AWS para identidades humanas.

Funcionamiento:

- AWS mantiene un **directorio de identidades** (propio o federado con un
  proveedor corporativo).
- Los permisos se agrupan en **permission sets**: plantillas de políticas
  asignables.
- El administrador **asigna** a una persona un permission set sobre una o
  varias cuentas.
- La persona inicia sesión una vez contra el portal de Identity Center (con
  MFA) y recibe, por cada cuenta y permiso al que tiene acceso, credenciales
  temporales.

Puntos clave para entenderlo:

- La identidad **no** vive dentro de la cuenta como usuario de IAM: vive en el
  directorio. La cuenta solo recibe el efecto de la asignación.
- Escala a muchas cuentas y muchas personas sin duplicar usuarios.
- Exige habilitar el servicio y definir permission sets: es la opción con más
  preparación inicial.
- Existen variantes de instancia (vinculada a una organización frente a una
  instancia de cuenta única), lo que cambia cuánta infraestructura de identidad
  hay que montar antes de empezar.

Es la respuesta correcta cuando hay una organización, un IdP corporativo o
varias cuentas. En un laboratorio de cuenta única y una sola persona, añade
piezas para obtener el mismo resultado que el mecanismo siguiente.

### 3.3 Credenciales de consola canjeadas por temporales

Mecanismo reciente, pensado para desarrollo local. La idea: reutilizar la
prueba de identidad que ya existe (contraseña de consola + MFA) para obtener
credenciales temporales de línea de comandos.

Funcionamiento:

1. La herramienta abre el navegador y AWS solicita la identidad.
2. La persona introduce usuario y contraseña de consola y completa MFA.
3. AWS devuelve una **autorización**, no un secreto permanente.
4. La herramienta guarda esa autorización en una **caché local** fuera del
   proyecto.
5. Cada vez que se necesita una credencial, se emite una nueva a partir de la
   caché y se renueva periódicamente.
6. Al agotarse la ventana máxima de sesión, hay que volver a autenticarse.

Propiedades:

- No hay secretos permanentes en disco; el material cacheado caduca solo.
- El MFA se exige en cada apertura de sesión, algo imposible con access keys.
- Los permisos siguen siendo los del usuario y sus grupos: cambia la
  autenticación, no la autorización.
- Requiere un permiso explícito que autorice el canje; sin él, el inicio de
  sesión falla aunque la contraseña sea correcta.
- La duración es acotada (horas, no días) y el cierre de sesión borra la caché.

Es la opción más simple y correcta para una cuenta única gestionada por una
persona, sin organización ni IdP.

### 3.4 Proceso de credenciales externo

No es un mecanismo de autenticación en sí, sino un **adaptador**. Permite
declarar en la configuración compartida un perfil que, en lugar de contener
credenciales, indica un programa que las produce al vuelo.

Sirve para integrar herramientas que no implementan un mecanismo nuevo con una
herramienta que sí lo implementa. Su límite conceptual: no crea sesiones
propias ni sustituye la autenticación, solo traduce. Si la sesión de origen
caduca, el adaptador falla igual que fallaría el origen.

Cuando la herramienta ya soporta el mecanismo de forma nativa, el adaptador es
ruido innecesario.

### 3.5 Roles para cargas de trabajo

Aquí no hay persona ni contraseña. El proceso demuestra su identidad a través
del entorno donde se ejecuta:

- **Instancia de EC2**: perfil de instancia; el servicio de metadatos entrega
  credenciales temporales al proceso.
- **Contenedor en ECS**: rol de tarea.
- **Pod en EKS**: identidad de pod vinculada a un rol de IAM.
- **Función Lambda**: rol de ejecución.
- **Proceso fuera de AWS**: se asume un rol explícitamente mediante STS, con
  una política de confianza que limite quién puede hacerlo.

Elementos conceptuales comunes:

- Siempre hay una **política de confianza** en el rol: define qué principal
  (servicio, cuenta, federación) puede asumirlo.
- Las credenciales se entregan por un canal que el proceso ya posee
  (metadatos, variables inyectadas por el orquestador, federación OIDC).
- La duración es corta y la rotación automática.
- Nunca se distribuyen secretos estáticos al contenedor.

Este es el mecanismo que usará un agente desplegado en AgentCore Runtime: el
agente no "tiene" credenciales, las recibe del rol que se le asigna.

### 3.6 Otros mecanismos relevantes

- **IAM Roles Anywhere**: permite que servidores fuera de AWS obtengan
  credenciales temporales presentando certificados X.509 emitidos por una PKI
  propia. Sustituye access keys en infraestructura on-premise.
- **Federación con IdP externo (SAML/OIDC)**: la organización autentica en su
  IdP y AWS confía en esa aserción. Es la base de Identity Center y también
  puede usarse directamente con roles.
- **AWS Builder ID**: identidad personal para servicios concretos de AWS
  (herramientas para desarrolladores). **No** es una cuenta de AWS ni da acceso
  a recursos de una cuenta; no sirve para autenticar la CLI contra tu cuenta.

## 4. Cómo consumen la autenticación las herramientas locales

### 4.1 Cadena de resolución de credenciales

La CLI y los SDK buscan credenciales en un orden fijo de fuentes, y usan la
primera que encuentren. De forma simplificada:

1. Credenciales pasadas explícitamente en la invocación.
2. Variables de entorno.
3. Archivos de configuración compartida (incluye perfiles de sesión y procesos
   externos).
4. Metadatos del entorno de ejecución (instancia, contenedor, pod).

Consecuencia práctica: una variable de entorno olvidada gana silenciosamente
sobre el perfil que crees estar usando. Por eso conviene no mezclar fuentes y
verificar siempre contra qué identidad se está llamando.

### 4.2 Perfiles

Un **perfil** es un nombre que agrupa región, fuente de credenciales y otros
ajustes. La CLI y el Toolkit comparten los mismos archivos de configuración, de
modo que un perfil creado por una herramienta suele ser utilizable por la otra.

Un perfil moderno no contiene secretos: contiene una **referencia** a la sesión
o al mecanismo que los produce. Esa diferencia —referencia frente a secreto—
resume el cambio de modelo de los últimos años.

### 4.3 El Toolkit de VS Code como cliente, no como sistema propio

El Toolkit no tiene un sistema de autenticación paralelo. Se apoya en los
mismos mecanismos y los expone como opciones en su panel de conexión:

| Opción del Toolkit  | Mecanismo subyacente              |
| ------------------- | --------------------------------- |
| Console credentials | Credenciales de consola canjeadas |
| Workforce           | IAM Identity Center / Builder ID  |
| IAM credentials     | Access keys de larga duración     |

Cuando la herramienta soporta de forma nativa el mecanismo elegido, comparte
sesión y perfil con la CLI: iniciar sesión en una autentica a la otra. Cuando
no lo soporta, queda el adaptador de proceso externo como puente.

## 5. Comparativa

| Mecanismo                  | ¿Secreto permanente? | ¿MFA?         | Preparación | Uso típico                     |
| -------------------------- | -------------------- | ------------- | ----------- | ------------------------------ |
| Access keys                | Sí                   | No            | Mínima      | Legado, integraciones acotadas |
| IAM Identity Center        | No                   | Sí (en el IdP)| Alta        | Empresas, varias cuentas       |
| Credenciales de consola    | No                   | Sí            | Baja        | Persona en cuenta única        |
| Proceso externo            | Depende del origen   | Depende       | Baja        | Adaptar herramientas antiguas  |
| Roles de carga de trabajo  | No                   | N/A           | Media       | Servicios y agentes en AWS     |
| Roles Anywhere             | No                   | N/A           | Media       | Infraestructura fuera de AWS   |

## 6. Ciclo de vida de una sesión local

Modelo mental que conviene fijar, independientemente del mecanismo:

1. **Autenticación**: se demuestra identidad (contraseña + MFA, IdP, canal de
   confianza del entorno).
2. **Emisión**: se reciben credenciales temporales con caducidad.
3. **Uso**: cada petición se firma con la credencial vigente.
4. **Renovación**: antes de expirar, se emiten credenciales nuevas a partir de
   la sesión, sin volver a autenticarse.
5. **Caducidad**: agotada la ventana máxima, la renovación deja de funcionar.
6. **Cierre de sesión**: se borra el material local aunque aún no haya
   caducado.

Errores típicos y su lectura correcta:

- "Credenciales expiradas" tras un rato de inactividad → sesión agotada, no
  permisos mal configurados.
- "No autorizado" nada más iniciar sesión → autorización (política), no
  autenticación.
- "No se encuentra la credencial" → cadena de resolución: perfil mal
  seleccionado o variable de entorno que gana.
- Funciona en una herramienta y no en otra → fuentes de credenciales distintas,
  no mecanismo distinto.

## 7. Criterios de decisión

Preguntas en orden, que suelen resolver el caso sin ambigüedad:

1. ¿Es una persona o una carga de trabajo?
   Carga de trabajo → rol recibido del entorno (3.5).
2. Si es persona: ¿hay organización, varias cuentas o IdP corporativo?
   Sí → IAM Identity Center (3.2).
   No → credenciales de consola canjeadas (3.3).
3. ¿La herramienta soporta el mecanismo de forma nativa?
   Sí → úsalo directamente.
   No → adaptador de proceso externo (3.4), consciente de su límite.
4. ¿Queda algún caso donde solo funcione una access key?
   Trátalo como deuda explícita: documenta por qué, limita permisos, rota y
   planifica su retirada.

Regla transversal: separa identidades por nivel de permiso (administración
frente a ejecución) y nunca incluyas una identidad de ejecución en un grupo
administrativo "temporalmente".

## 8. Antipatrones

- Access keys de la cuenta raíz, en cualquier forma.
- Access keys en `.env`, imágenes de contenedor o repositorios.
- Copiar credenciales entre máquinas o compartirlas por chat.
- Usar el perfil `default` para todo, de modo que no se sabe qué identidad
  está activa.
- Ampliar permisos para resolver un fallo de credenciales.
- Meter la identidad de ejecución en el grupo de administración para "probar
  rápido".
- Confundir Builder ID con una cuenta de AWS.
- Interpretar un adaptador de credenciales como un mecanismo de autenticación
  nuevo.

## 9. Glosario rápido

- **Autenticación**: demostrar identidad.
- **Autorización**: decidir qué puede hacer una identidad ya autenticada.
- **Credencial temporal**: identificador, secreto y token de sesión con
  caducidad.
- **Sesión**: intervalo de validez de unas credenciales temporales.
- **Perfil**: nombre que agrupa región y fuente de credenciales en las
  herramientas locales.
- **Rol**: identidad asumible, sin credenciales permanentes, con política de
  confianza.
- **Permission set**: plantilla de permisos de Identity Center asignable a
  personas sobre cuentas.
- **MFA**: segundo factor de autenticación.
- **Caché de sesión**: almacenamiento local de la autorización y de las
  credenciales temporales; caduca y puede borrarse.

## 10. Alcance de este documento

Cubre los mecanismos de autenticación de identidades humanas y de cargas de
trabajo en AWS, con el nivel de detalle necesario para tomar decisiones y
entender fallos. No cubre federación avanzada, diseño de políticas de mínimo
privilegio, cifrado de secretos en aplicaciones ni la operación de Identity
Center a escala organizativa.
