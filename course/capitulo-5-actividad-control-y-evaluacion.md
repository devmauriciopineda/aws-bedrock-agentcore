# Actividad: operar el agente con controles reales

## Propósito

Aplicar en AWS controles de identidad, autorización, observabilidad y
evaluación sobre el Runtime, Gateway y Memory creados en capítulos anteriores.
El trabajo usa tráfico sintético, una muestra pequeña y recursos de bajo
consumo.

## Prerrequisitos

- Runtime, Gateway y Memory de aprendizaje activos y etiquetados.
- Rol de ejecución separado del perfil administrativo.
- Presupuesto y región única.
- Datos sintéticos y ningún secreto en logs o evaluaciones.

## Entregable

Actualiza `paquete-control-observabilidad-evaluacion.md` en
`course/entregas/capitulo-5/`. Incluye:

1. Recursos reales de Identity, Policy, CloudWatch/OpenTelemetry y
   Evaluations creados o configurados.
2. Matriz de identidades inbound/outbound y permisos.
3. Evidencia de una solicitud permitida y una denegada.
4. Logs, métricas, trazas y dashboard o consulta mínima.
5. Evaluación pequeña bajo demanda y, si está disponible, online con muestreo
   mínimo.
6. Inventario, coste y procedimiento de desactivación/eliminación.

## Pasos

1. Crea o configura una identidad de ejecución de aprendizaje con permisos
   solo para Runtime, el modelo, Gateway, Memory y observabilidad usados.
2. Configura una política que permita lecturas y bloquee cualquier operación
   de escritura o herramienta no incluida en el catálogo.
3. Invoca el agente con datos sintéticos y verifica una autorización exitosa.
4. Intenta una operación denegada y confirma que no llega al backend.
5. Habilita las señales mínimas en CloudWatch y OpenTelemetry: una métrica de
   invocaciones, logs clasificados y trazas de Runtime/modelo/Memory/Gateway.
6. Configura una consulta o dashboard mínimo con latencia, errores y versión.
   Evita alarmas de alta frecuencia o retención innecesaria.
7. Crea un conjunto pequeño de interacciones sintéticas y ejecuta una
   evaluación bajo demanda. Registra versión, métricas y resultado.
8. Si la capacidad online está disponible y tiene coste aceptable, configúrala
   con muestreo mínimo; si no, documenta la razón y conserva la prueba bajo
   demanda.
9. Provoca únicamente fallos controlados: payload inválido, denegación y
   timeout local. No generes carga ni errores repetitivos.

## Criterios de aceptación

- Una solicitud permitida y una denegada producen evidencia diferenciable.
- Las identidades inbound y outbound están separadas.
- Los logs no contienen credenciales ni datos personales.
- Existe una métrica y una traza consultables.
- La evaluación bajo demanda analiza una muestra pequeña y versionada.
- La evaluación online, si se habilita, tiene muestreo y límites de coste.
- Los umbrales de alerta y retención son mínimos y están documentados.
- Se conoce el coste observado y el origen de cada señal.

## Limpieza obligatoria

1. Deshabilita evaluaciones online y alarmas antes de eliminar sus fuentes.
2. Elimina dashboards, alarmas, grupos de logs y streams creados solo para el
   laboratorio. Usa el nombre exacto, nunca comodines.
3. Desactiva políticas temporales y retira permisos de observabilidad del rol.
4. Elimina configuraciones de evaluación y sus datos sintéticos.
5. Revisa CloudWatch Billing y la consola de cada servicio.

Conserva únicamente las señales que el capítulo 6 reutilizará; documenta el
plazo máximo de conservación y elimina el resto.

## Resultado esperado

El agente real tiene controles verificables de autorización, señales mínimas
de operación y una evaluación reproducible, sin mantener telemetría o
tráfico innecesarios.
