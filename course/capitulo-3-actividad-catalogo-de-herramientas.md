# Actividad: crear herramientas reales con AgentCore Gateway

## Propósito

Crear herramientas de estudio en AWS y conectarlas al Runtime del capítulo 2
mediante AgentCore Gateway. La actividad cubre un target Lambda, un endpoint
HTTP sencillo y un servidor MCP de prueba, usando datos sintéticos y
operaciones de solo lectura.

## Prerrequisitos

- Runtime del capítulo 2 activo o recreable.
- Región y perfil de estudio únicos.
- Presupuesto, tags e inventario actualizados.
- Permisos mínimos para Lambda, API Gateway/endpoint HTTP, ECR si aplica y
  AgentCore Gateway.

## Entregable

Actualiza `catalogo-herramientas-gateway.md` en
`course/entregas/capitulo-3/`. Añade:

1. Recursos reales creados, región, tags e identificadores.
2. Diagrama agente -> Gateway -> target -> backend.
3. Catálogo con contratos de entrada y salida.
4. Evidencia de descubrimiento e invocación de cada herramienta.
5. Identidades, autenticación, autorización y errores.
6. Versiones y pruebas de incompatibilidad.
7. Inventario de recursos y pasos de eliminación.

## Recursos de bajo consumo

Implementa solo:

- una función Lambda pequeña que devuelva datos sintéticos;
- un endpoint HTTP de prueba con una respuesta fija, si la integración
  requerida por Gateway lo necesita;
- un servidor MCP local o mínimo, expuesto únicamente durante la prueba y sin
  datos reales.

No uses NAT Gateway, EC2, RDS, OpenSearch ni cargas continuas. Si una
integración exige un servicio no gratuito o persistente, detente, estima el
coste y confirma que es imprescindible antes de crearlo.

## Pasos

1. Reutiliza el agente y Runtime del capítulo 2.
2. Crea una Lambda de solo lectura para consultar una política sintética.
   Limita memoria, timeout y concurrencia; registra su ARN.
3. Crea el endpoint HTTP mínimo solo si el target REST lo requiere. Usa una
   respuesta fija y desactívalo al finalizar.
4. Levanta un servidor MCP de prueba con una herramienta de cálculo local,
   sin secretos ni efectos secundarios.
5. Configura un target de Gateway para cada backend usando la CLI/consola
   vigente. Documenta autenticación y permisos reales.
6. Publica únicamente las herramientas necesarias para el agente.
7. Descubre el catálogo desde Python, valida argumentos e invoca cada target.
8. Integra los resultados en el nodo de herramientas de LangGraph.
9. Prueba validación, autorización, timeout, resultado vacío y versión
   incompatible.
10. Registra latencia y coste aproximado de cada llamada sin guardar payloads
    sensibles.

## Criterios de aceptación

- Gateway real descubre los targets configurados.
- La Lambda se invoca desde el agente y devuelve el contrato esperado.
- El endpoint HTTP y MCP, si fueron creados, responden y están documentados.
- El agente no conoce secretos ni URLs internas del backend.
- Se bloquea cualquier operación de escritura.
- Los errores se clasifican y los reintentos están limitados.
- Se demuestra al menos una invocación desde Python y una desde LangGraph.
- Se documentan identificadores, tags, región y coste observado.

## Limpieza obligatoria

1. Detén el servidor MCP y elimina su endpoint público o regla temporal.
2. Elimina los targets y el Gateway desde la consola o comando específico de
   AgentCore; elimina solo los identificadores registrados.
3. Elimina la Lambda con el comando equivalente a
   `aws lambda delete-function --function-name <nombre> --region <región>`.
4. Elimina el endpoint HTTP y sus stages o integraciones.
5. Retira roles y políticas exclusivos de las herramientas.
6. Verifica que el Runtime ya no tenga herramientas activas y revisa costes.

No borres el Runtime si el capítulo 4 lo reutilizará; registra explícitamente
qué queda activo y durante cuánto tiempo.

## Resultado esperado

El agente del capítulo 2 utiliza al menos una herramienta real a través de
Gateway, con contratos, permisos mínimos, pruebas y limpieza verificable.
