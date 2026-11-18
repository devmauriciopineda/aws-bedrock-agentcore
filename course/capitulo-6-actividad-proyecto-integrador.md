# Actividad: proyecto integrador desplegado en AWS

## Propósito

Consolidar los recursos reales de los capítulos anteriores en una pequeña
aplicación funcional desplegada totalmente en AWS. El resultado debe poder
invocarse, usar una herramienta, recuperar memoria, respetar políticas,
producir señales y evaluarse con tráfico sintético.

El objetivo no es construir un servicio productivo de alta disponibilidad:
es demostrar una ruta completa y de bajo consumo en una cuenta personal.

## Prerrequisitos

- Actividades 1 a 5 completadas o sus recursos recreados.
- Una sola región y un único entorno `learning`.
- Presupuesto revisado y alertas activas.
- Runtime, Gateway, Memory, roles, políticas y observabilidad inventariados.
- Modelo de Bedrock habilitado y acceso probado.

## Entregable

Actualiza `proyecto-integrador-agentcore.md` en
`course/entregas/capitulo-6/`. Incluye:

1. Diagrama de la aplicación desplegada y sus identificadores reales.
2. URL, endpoint o método de invocación y ejemplo sin secretos.
3. Flujo exitoso y flujos de error.
4. Evidencia de herramienta, memoria, autorización y evaluación.
5. Métricas de una prueba pequeña y coste observado.
6. Versionamiento y rollback.
7. Runbook completo de apagado y eliminación.

## Construcción final

1. Revisa todos los recursos y elimina duplicados antes de integrar.
2. Usa el Runtime del capítulo 2 y la herramienta de Gateway del capítulo 3.
3. Conecta Memory del capítulo 4 con Actor ID y Session ID sintéticos.
4. Aplica la política del capítulo 5 y conserva solo logs y métricas mínimas.
5. Ejecuta una invocación válida que recupere memoria y use una herramienta.
6. Ejecuta una invocación denegada y una con dependencia indisponible.
7. Ejecuta la evaluación bajo demanda aprobada; no uses un conjunto grande.
8. Publica una segunda versión, compara una muestra pequeña y demuestra
   rollback o documenta evidencia de que el endpoint vuelve a la anterior.
9. Mide latencia y coste con pocas invocaciones; no realices pruebas de carga.
10. Captura inventario final con región, tags, IDs, propietarios y estado.

## Límites de consumo

- Una región, un entorno y una imagen activa.
- Sin NAT Gateway, EC2, RDS, OpenSearch ni almacenamiento persistente no
  necesario.
- Sin tráfico continuo, bucles de invocación o pruebas de concurrencia masiva.
- Evaluaciones online deshabilitadas o limitadas a una muestra mínima.
- Logs y trazas con retención corta.
- Herramientas sintéticas y operaciones de solo lectura.

Si una capacidad requiere un recurso de pago no previsto, detén la actividad,
consulta el coste actual en AWS y decide si sustituirla por una simulación.

## Criterios de aceptación

- La aplicación responde desde AWS y combina Python/LangGraph, Runtime,
  Bedrock, Gateway, Memory, Identity, Policy y observabilidad.
- Una invocación usa una herramienta real y recupera memoria real.
- Existe evidencia de autorización permitida y denegada.
- Se ejecuta una evaluación versionada.
- Se prueban error, timeout o degradación sin éxito falso.
- Se documenta rollback y no se dejan versiones duplicadas activas.
- Coste, región, tags y recursos están inventariados.
- El runbook permite apagar y eliminar todo el laboratorio de forma segura.

## Limpieza final obligatoria

Realiza la limpieza en este orden y registra cada confirmación:

1. Detén el tráfico y deshabilita endpoints, evaluaciones online y alarmas.
2. Elimina targets, Gateway y endpoints HTTP de prueba.
3. Elimina el Runtime y sus versiones no necesarias.
4. Elimina Memory y sus eventos sintéticos.
5. Elimina Lambda, ECR, imágenes, logs, dashboards y alarmas.
6. Retira roles y políticas creados exclusivamente para el laboratorio.
7. Elimina la alerta de presupuesto solo cuando ya no haya recursos activos;
   conserva MFA y la identidad administrativa.
8. Revisa Billing, Cost Explorer y la consola de cada servicio después de
   esperar la actualización de cargos.
9. Conserva el runbook y la evidencia, pero elimina secretos y datos de
   ejecución del repositorio.

Para cada servicio usa el identificador exacto documentado. No uses
comodines, borrado recursivo ni comandos que puedan afectar otros proyectos.
Si no puedes confirmar el alcance de una eliminación, detente y verifica en la
consola.

## Resultado esperado

Una pequeña aplicación de agente funcional, desplegada completamente en AWS,
demostrable con datos sintéticos y acompañada de un inventario y runbook que
evitan gastos posteriores innecesarios.
