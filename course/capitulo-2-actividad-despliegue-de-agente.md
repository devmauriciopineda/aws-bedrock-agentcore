# Actividad: desplegar un agente real en AgentCore Runtime

## Propósito

Empaquetar un agente Python pequeño, publicar su imagen en Amazon ECR, crear
un recurso real de AgentCore Runtime e invocarlo desde Python. La actividad
debe producir una versión funcional, con sesiones, contrato, errores y
evidencia de ejecución.

Usa respuestas simuladas o datos sintéticos. No conectes todavía herramientas
remotas ni Memory.

## Prerrequisitos

- Actividad del capítulo 1 completada.
- Región y perfil de estudio definidos.
- Acceso al modelo validado.
- Presupuesto y tags configurados.
- Docker y AWS CLI instalados; no almacenes credenciales en el proyecto.

## Entregable

Actualiza `runbook-despliegue-runtime.md` en
`course/entregas/capitulo-2/`. Incluye:

1. Contrato JSON de entrada, éxito y error.
2. Código o referencia al agente Python y `BedrockAgentCoreApp`.
3. Nombre, URI y tag de la imagen ECR.
4. Identificador, región y versión del Runtime creado.
5. Evidencia de invocaciones válidas, inválidas y aisladas.
6. Procedimiento reproducible de actualización y rollback.
7. Inventario de recursos y costes observados.
8. Pasos exactos de deshabilitación y eliminación.

## Pasos

1. Implementa un agente mínimo que acepte `input`, `session_id` y metadata
   opcional. Devuelve una respuesta estructurada sin secretos.
2. Añade `BedrockAgentCoreApp` y `@app.entrypoint`; prueba localmente el
   contrato y los errores.
3. Construye una imagen con un tag único. Comprueba que no contiene archivos
   de credenciales.
4. Crea un repositorio ECR dedicado al laboratorio y etiquétalo. Conserva la
   URI en el runbook.
5. Publica una única imagen pequeña y registra su digest.
6. Con AgentCore CLI o la consola vigente, crea un Runtime de prueba usando
   la imagen y el rol de ejecución del capítulo 1. Usa la región única.
7. Configura el endpoint con la versión inicial y documenta cada parámetro.
8. Invoca el endpoint con Boto3: éxito, payload inválido, dos sesiones y un
   timeout controlado. No ejecutes pruebas de carga.
9. Actualiza el agente con un cambio visible, publica un segundo tag y crea o
   promueve una nueva versión solo después de probarla.
10. Prueba rollback a la primera versión.

## Pruebas mínimas

| Caso | Resultado esperado |
|---|---|
| Solicitud válida | Respuesta estructurada y sesión correcta |
| Campo obligatorio ausente | Error de validación explícito |
| Entrada vacía | Rechazo sin éxito falso |
| Dos sesiones | No se cruzan estados |
| Timeout | Error clasificable |
| Nueva imagen | Versión identificable |
| Rollback | Vuelve a una versión conocida |

## Criterios de aceptación

- Existe una imagen en ECR y un Runtime real invocable.
- El contrato, identidad, región, URI y versión están documentados.
- El endpoint responde a una invocación válida.
- Se prueban errores y aislamiento de sesiones.
- El cliente usa timeout y no registra credenciales.
- El rollback se demuestra o se documenta con evidencia verificable.
- No se ejecutan pruebas de carga ni se dejan múltiples endpoints activos.

## Limpieza obligatoria

Ejecuta la limpieza al terminar la sesión, salvo que el capítulo 3 dependa
explícitamente de este Runtime:

1. Deshabilita o elimina el endpoint y la versión de prueba desde AgentCore
   CLI/consola; consulta `help` o la documentación vigente para el comando
   exacto y registra el identificador afectado.
2. Elimina el Runtime cuando ya no sea necesario.
3. Elimina el repositorio ECR y sus imágenes con el comando o consola
   equivalente a `delete-repository --force`.
4. Elimina roles o políticas creados exclusivamente para Runtime, después de
   retirar sus asociaciones.
5. Confirma en la consola que no quedan endpoints, imágenes ni recursos
   asociados y registra el coste.

No uses borrados recursivos ni comandos con comodines. Conserva el recurso
solo si el siguiente capítulo lo reutiliza y deja constancia de ello.

## Resultado esperado

Un agente mínimo desplegado realmente en Runtime, invocable y versionado, con
un procedimiento seguro para apagarlo y eliminarlo.
