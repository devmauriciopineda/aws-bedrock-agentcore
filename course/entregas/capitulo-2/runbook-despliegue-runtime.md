# Runbook: despliegue de agente en AgentCore Runtime

**Capítulo:** 2  
**Proyecto:** `agentcore-study`  
**Entorno:** `learning`  
**Propietario:** `<alias>`  
**Región:** `<aws-region>`  
**Perfil AWS:** `<profile-name>`  
**Fecha:** `<yyyy-mm-dd>`

> Completa los campos entre `< >`. Usa únicamente datos sintéticos. No
> incluyas access keys, tokens, secretos, correos ni payloads sensibles.

## 1. Aplicación

Código: [app/](../../../app/)  
Punto de entrada: `app.py:invoke`  
Prueba local: `python -m pytest -q`

La aplicación recibe una solicitud breve y devuelve una respuesta estructurada.
No invoca todavía un modelo, Gateway, Memory ni herramientas remotas; el
objetivo es validar el contrato y el ciclo de despliegue de Runtime.

## 2. Contrato JSON

### Entrada válida

```json
{
  "input": "Consulta sintética",
  "session_id": "session-demo-01"
}
```

`input` y `session_id` son cadenas no vacías. Campos adicionales se ignoran.

### Salida exitosa

```json
{
  "output": "Solicitud recibida: Consulta sintética",
  "session_id": "session-demo-01",
  "status": "completed"
}
```

### Errores

| Caso | Error esperado |
|---|---|
| Payload no es objeto JSON | `payload must be a JSON object` |
| `input` ausente, vacío o no textual | `input must be a non-empty string` |
| `session_id` ausente, vacío o no textual | `session_id must be a non-empty string` |

El cliente no presenta un error de validación como respuesta exitosa.

## 3. Imagen y Runtime

| Campo | Valor |
|---|---|
| Repositorio ECR | `agentcore-study-agent` |
| URI ECR | `<account>.dkr.ecr.<aws-region>.amazonaws.com/agentcore-study-agent` |
| Tag inicial | `v1` |
| Digest inicial | `<sha256:...>` |
| Tag actualizado | `v2` |
| Digest actualizado | `<sha256:...>` |
| Runtime ARN/ID | `<runtime-arn-or-id>` |
| Endpoint de prueba | `agentcore-study-test` |
| Versión activa | `<v1>` |
| Rol de ejecución | `agentcore-study-execution` |
| Fecha de creación | `<yyyy-mm-dd>` |

## 4. Evidencia de invocaciones

No pegues tokens ni respuestas que contengan datos reales.

| Caso | Sesión | Resultado observado | Evidencia |
|---|---|---|---|
| Válida | `<session-a>` | `completed` | `<captura o salida depurada>` |
| `input` ausente | `<session-a>` | error explícito | `<captura o salida depurada>` |
| Entrada vacía | `<session-a>` | error explícito | `<captura o salida depurada>` |
| Dos sesiones aisladas | `<session-a>`, `<session-b>` | IDs no cruzados | `<captura o salida depurada>` |
| Timeout controlado | `<session-timeout>` | error clasificable | `<captura o salida depurada>` |

## 5. Actualización y rollback

1. Se probó localmente el cambio `<descripción breve>` antes de publicarlo.
2. Se publicó `v2` con digest `<sha256:...>`.
3. Se creó o promovió la versión `<version-id>` en `<fecha>`.
4. La invocación de `v2` devolvió `<resultado>`.
5. El endpoint se revirtió a `v1` mediante `<comando o consola>`.
6. La invocación posterior devolvió `<resultado que confirma v1>`.
7. No quedaron endpoints adicionales activos: `<sí/no>`.

## 6. Inventario, coste y etiquetas

| Recurso | Identificador | Estado | Coste observado | Eliminar |
|---|---|---|---|---|
| ECR | `<repository-uri>` | `<active/deleted>` | `<amount>` | Sí |
| Runtime | `<runtime-arn-or-id>` | `<active/deleted>` | `<amount>` | Sí |
| Endpoint | `<endpoint-id>` | `<active/deleted>` | `<amount>` | Sí |
| Rol | `agentcore-study-execution` | `<active/deleted>` | N/A | `<sí/no>` |

Etiquetas: `Project=agentcore-study`, `Environment=learning`,
`Owner=<alias>`, `DeleteAfter=<yyyy-mm-dd>`.

## 7. Limpieza ejecutada

- [ ] Endpoint y versiones de prueba deshabilitados o eliminados.
- [ ] Runtime eliminado o documentado como reutilizado por capítulo 3.
- [ ] Imágenes y repositorio ECR eliminados.
- [ ] Rol y políticas exclusivas retirados después de desasociarlos.
- [ ] No quedan recursos inesperados en la región.
- [ ] Billing y Cost Explorer revisados.
- [ ] Sesión temporal cerrada.

## 8. Resultado

**Estado:** `<pending/complete>`  
**Fecha:** `<yyyy-mm-dd>`  
**Revisado por:** `<alias>`  
**Observaciones:** `<notes>`
