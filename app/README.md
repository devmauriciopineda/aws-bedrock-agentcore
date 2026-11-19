# Agente mínimo para Bedrock AgentCore

## Descripción

Aplicación Python mínima compatible con Amazon Bedrock AgentCore Runtime.
Valida una solicitud JSON y devuelve una respuesta estructurada asociada a una
sesión. No invoca todavía un modelo de Bedrock ni utiliza Gateway, Memory o
herramientas remotas.

## Funcionalidad

- Recibe `input` y `session_id`.
- Rechaza payloads que no sean objetos JSON.
- Rechaza entradas vacías o campos obligatorios ausentes.
- Devuelve `output`, `session_id` y `status`.
- Expone el punto de entrada mediante `BedrockAgentCoreApp`.
- Incluye un cliente Boto3 para invocar un Runtime desplegado.

## Estructura

```text
app/
├── app.py
├── client.py
├── test_app.py
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
└── .dockerignore
```

## Requisitos

- Python 3.13 para ejecución local.
- AWS CLI y un perfil AWS válido para invocar Runtime.
- Docker, solo para construir la imagen.
- Acceso a un Runtime de Bedrock AgentCore ya desplegado.

Las credenciales AWS no se guardan en esta carpeta. Boto3 utiliza el perfil
indicado mediante `--profile`.

## Instalación

Desde la raíz del repositorio:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r app\requirements-dev.txt
```

Para instalar únicamente las dependencias de ejecución:

```powershell
python -m pip install -r app\requirements.txt
```

## Ejecución local

El proceso de aplicación inicia el servidor compatible con AgentCore:

```powershell
.\.venv\Scripts\python.exe app\app.py
```

Validar el contrato sin AWS:

```powershell
.\.venv\Scripts\python.exe -m pytest -q app\test_app.py
```

## Invocación local

`app.py` inicia el servidor local de AgentCore en
`http://localhost:8080`. Mantén la aplicación ejecutándose en una terminal:

```powershell
.\.venv\Scripts\Activate.ps1
python app\app.py
```

En una segunda terminal, invoca el endpoint con PowerShell:

```powershell
$body = @{
    input = "Consulta sintética"
    session_id = "session-local-01"
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri http://localhost:8080/invocations `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

También puedes usar `curl.exe`:

```powershell
curl.exe -X POST http://localhost:8080/invocations `
  -H "Content-Type: application/json" `
  -d '{\"input\":\"Consulta sintética\",\"session_id\":\"session-local-01\"}'
```

Respuesta esperada:

```json
{
  "output": "Solicitud recibida: Consulta sintética",
  "session_id": "session-local-01",
  "status": "completed"
}
```

Para comprobar la validación de errores:

```powershell
curl.exe -X POST http://localhost:8080/invocations `
  -H "Content-Type: application/json" `
  -d '{\"input\":\"\",\"session_id\":\"session-local-01\"}'
```

## Contrato de entrada

Payload mínimo:

```json
{
  "input": "Consulta sintética",
  "session_id": "session-demo-01"
}
```

Requisitos:

- `input`: cadena no vacía.
- `session_id`: cadena no vacía.

Campos opcionales adicionales se ignoran.

## Respuesta exitosa

```json
{
  "output": "Solicitud recibida: Consulta sintética",
  "session_id": "session-demo-01",
  "status": "completed"
}
```

## Errores de validación

La función devuelve un error `ValueError` con uno de estos mensajes:

| Situación | Mensaje |
|---|---|
| Payload no es objeto JSON | `payload must be a JSON object` |
| `input` ausente, vacío o no textual | `input must be a non-empty string` |
| `session_id` ausente, vacío o no textual | `session_id must be a non-empty string` |

## Invocación de un Runtime desplegado

`client.py` usa Boto3 y no invoca `localhost`. Requiere un Runtime
desplegado, su ARN, una región y un perfil AWS válido:

Con un Runtime desplegado y su ARN:

```powershell
.\.venv\Scripts\python.exe app\client.py `
  --runtime-arn "<runtime-arn>" `
  --region "<aws-region>" `
  --profile "<profile-name>" `
  --input "Consulta sintética"
```

El cliente genera un `session_id` único, envía el payload como
`application/json` y usa un timeout de conexión de 5 segundos y de lectura de
30 segundos. No reintenta automáticamente.

## Docker

Construir la imagen desde la raíz del repositorio:

```powershell
docker build --file app\Dockerfile --tag agentcore-study-agent:v1 app
```

La imagen ejecuta `app.py` y contiene solo las dependencias de runtime. El
archivo `.dockerignore` excluye credenciales, entornos virtuales y artefactos
locales.
