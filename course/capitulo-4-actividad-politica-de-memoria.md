# Actividad: crear y probar memoria real con AgentCore Memory

## Propósito

Crear un recurso real de AgentCore Memory e integrarlo con el agente de los
capítulos anteriores. La actividad registra eventos sintéticos, recupera
memoria entre sesiones y demuestra aislamiento entre actores, con retención y
limpieza explícitas.

## Prerrequisitos

- Runtime y, preferiblemente, Gateway del capítulo 3.
- Una región y un Memory ID de aprendizaje separados de producción.
- Rol de ejecución con permisos mínimos de lectura/escritura en ese recurso.
- No utilizar datos personales ni secretos.

## Entregable

Actualiza `politica-memoria-agentcore.md` en
`course/entregas/capitulo-4/`. Incluye:

1. Memory ID, región, tags e identificadores de prueba.
2. Actor ID y Session ID sintéticos.
3. Namespaces y estrategias configuradas.
4. Evidencia de escritura y recuperación entre invocaciones.
5. Pruebas de aislamiento y comportamiento ante memoria indisponible.
6. Retención, corrección y eliminación.
7. Inventario y procedimiento de borrado del recurso.

## Pasos

1. Crea un recurso de Memory de aprendizaje mediante la interfaz vigente de
   AgentCore. Usa un nombre que incluya proyecto y entorno; no lo compartas
   con producción.
2. Configura solo las estrategias y namespaces necesarios para el ejercicio:
   preferencias, resumen y hechos sintéticos.
3. Genera dos Actor ID y dos Session ID por actor. No uses correos ni nombres
   reales.
4. Amplía el agente para registrar eventos después de una respuesta y recuperar
   memoria antes de ejecutar LangGraph.
5. Escribe una preferencia sintética para el actor A y verifica que aparece en
   una segunda sesión del mismo actor.
6. Verifica que el actor B no puede recuperar la memoria de A, incluso usando
   un Session ID conocido.
7. Prueba namespace no autorizado, recuerdo obsoleto y Memory temporalmente
   indisponible.
8. Elimina un evento o marca una preferencia como corregida según las
   capacidades disponibles; registra el resultado.
9. Mide número de lecturas, escrituras, latencia y coste aproximado. No
   ejecutes pruebas de volumen.

## Criterios de aceptación

- Existe un recurso Memory real en la región de estudio.
- El agente escribe y recupera un evento sintético entre sesiones.
- Actor ID, Session ID y namespace se validan antes de cada operación.
- El actor B no accede a datos del actor A.
- No se persisten secretos ni datos personales.
- Se documenta el comportamiento ante ausencia, contradicción y caída de
  Memory.
- El coste y la retención están registrados.

## Limpieza obligatoria

1. Elimina los eventos y datos sintéticos mediante la interfaz de Memory,
   cuando la capacidad esté disponible.
2. Deshabilita o elimina estrategias, namespaces o recursos derivados de la
   práctica.
3. Elimina el recurso Memory desde AgentCore CLI/consola, usando el comando
   exacto mostrado por la documentación vigente; confirma el Memory ID antes.
4. Retira permisos de Memory del rol si no se reutilizará.
5. Comprueba que no quedan datos, endpoints ni logs de prueba y registra el
   coste final.

Si el capítulo 6 reutilizará el recurso, conserva únicamente el recurso
etiquetado y elimina todos los datos sintéticos antes de continuar.

## Resultado esperado

El agente conserva una memoria mínima y real entre sesiones, respeta el
aislamiento por actor y tiene un procedimiento documentado para borrar sus
datos y el recurso.
