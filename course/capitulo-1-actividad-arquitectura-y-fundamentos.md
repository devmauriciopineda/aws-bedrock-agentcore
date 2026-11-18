# Actividad: preparar una cuenta AWS personal para AgentCore

## Propósito

Preparar una cuenta personal de AWS con controles de coste, una región de
estudio, acceso al modelo y una identidad de trabajo con mínimo privilegio.
Al terminar, quedará documentada la arquitectura objetivo y el inventario que
se utilizará en los capítulos siguientes.

Esta es una actividad sobre recursos reales. No utilices una cuenta
productiva, datos reales ni credenciales de larga duración.

## Caso de aplicación

Continúa el caso del asistente de políticas de viajes. La solución final
usará Python, LangGraph, AgentCore Runtime, Gateway, Memory, Identity, Policy,
Amazon Bedrock y observabilidad. En este capítulo todavía no se despliega el
agente; se prepara la cuenta y se validan las precondiciones.

## Entregable

Crea `mapa-arquitectonico-agentcore.md` dentro de
`course/entregas/capitulo-1/`. Incluye:

1. Diagrama de la arquitectura final y sus componentes.
2. Región, cuenta y perfil AWS de estudio.
3. Convención de nombres y etiquetas, por ejemplo
   `Project=agentcore-study`, `Environment=learning` y `Owner=<alias>`.
4. Inventario de recursos, responsables y comandos o pantallas usados.
5. Resultado de la validación de acceso al modelo.
6. Identidades de administración y ejecución.
7. Riesgos, límites y decisiones pendientes.

## Preparación segura de la cuenta

1. Activa MFA para la cuenta raíz y no uses la cuenta raíz para laboratorios.
2. Elige una sola región compatible con los servicios del curso y registra la
   decisión. No repartas recursos entre regiones.
3. Usa un perfil o identidad administrativa de estudio con MFA. No guardes
   access keys en el repositorio ni en la imagen del agente.
4. Configura una alerta de presupuesto de AWS con un umbral bajo apropiado
   para tu cuenta. Registra destinatario, umbral y fecha de revisión.
5. Habilita solo el acceso al modelo de Bedrock que el laboratorio necesita,
   siguiendo la consola o documentación vigente de AWS.
6. Comprueba cuotas, disponibilidad regional y requisitos de AgentCore antes
   de crear recursos.
7. Crea una identidad o rol de ejecución separado. Concede únicamente lo
   necesario para invocar el modelo y los recursos que se crearán después.
8. Documenta cada cambio en un inventario; no guardes secretos ni valores de
   tokens.

## Pasos

1. Describe en cinco líneas o menos qué hará el asistente y qué parte
   corresponde a LangGraph.
2. Dibuja el flujo desde el usuario hasta Runtime, Bedrock, Gateway, Memory y
   observabilidad.
3. Distingue plano de control y plano de ejecución.
4. Explica por qué Browser y Code Interpreter quedan deshabilitados en este
   laboratorio.
5. Valida desde la CLI o consola la región, identidad activa y acceso al
   modelo. Guarda solo la salida no sensible.
6. Crea y prueba la alerta de presupuesto. No la confundas con un límite duro:
   supervisa el coste diariamente.
7. Define el rol de ejecución y deja pendientes los permisos específicos de
   Runtime, Gateway y Memory para los capítulos en que se necesiten.
8. Ejecuta una revisión de “qué se creó” y registra recursos, región, tags y
   propietario.

## Criterios de aceptación

- La arquitectura incluye usuario, Python/LangGraph, Runtime, Bedrock,
  Gateway, Memory y observabilidad.
- La cuenta tiene MFA, región única y una alerta de presupuesto configurada.
- El acceso al modelo requerido está validado.
- Administración y ejecución usan identidades separadas.
- Los recursos y documentos usan una convención de tags.
- El inventario no contiene secretos.
- Browser y Code Interpreter no se habilitan sin necesidad.
- Se documenta un procedimiento para revisar coste y recursos cada sesión.

## Limpieza y control de gastos

Al finalizar:

1. Revisa el inventario y confirma que no se creó ningún recurso inesperado.
2. Mantén la alerta de presupuesto si continuarás el curso; elimínala al
   terminar todo el laboratorio desde AWS Billing > Budgets.
3. Si creaste un rol o política exclusivamente para esta actividad, elimina
   primero sus asociaciones y después el rol/política desde IAM.
4. Revoca sesiones o credenciales temporales que no vuelvas a usar.
5. No elimines la identidad administrativa principal ni desactives MFA.

## Resultado esperado

Una cuenta personal preparada y controlada, con acceso mínimo al modelo,
alerta de coste e inventario suficiente para crear el primer Runtime sin
confundir recursos de estudio con recursos productivos.
