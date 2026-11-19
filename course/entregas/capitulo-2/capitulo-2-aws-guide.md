# Guía AWS: capítulo 2

## Bloque 1: Preparar herramientas y variables

1. Abre PowerShell en la raíz del repositorio.
2. Define los valores del laboratorio:

   ```powershell
   $env:AWS_PROFILE="<profile-name>"
   $env:AWS_REGION="<aws-region>"
   $env:ECR_REPOSITORY="agentcore-study-agent"
   $env:IMAGE_TAG="v1"
   ```

3. Comprueba la identidad y región:

   ```powershell
   aws sts get-caller-identity --profile $env:AWS_PROFILE
   aws configure get region --profile $env:AWS_PROFILE
   ```

4. Comprueba que Docker está iniciado:

   ```powershell
   docker version
   ```

5. Instala el CLI de AgentCore según la documentación vigente y comprueba:

   ```powershell
   agentcore --help
   ```

6. Crea y activa un entorno Python local en `.venv`:

   ```powershell
   py -3.13 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   python -m pip install -r app\requirements-dev.txt
   ```

## Bloque 2: Probar el agente local

7. Activa `.venv` desde la raíz y ejecuta las pruebas:

   ```powershell
   python -m pytest -q
   ```

8. Comprueba que no hay credenciales en el código:

   ```powershell
   Select-String -Path app\* -Pattern "AKIA|aws_secret_access_key|aws_access_key_id" -Recurse
   ```

## Bloque 3: Crear y etiquetar el repositorio ECR

11. Crea el repositorio privado:

    ```powershell
    aws ecr create-repository `
      --repository-name $env:ECR_REPOSITORY `
      --region $env:AWS_REGION `
      --image-scanning-configuration scanOnPush=true `
      --tags Key=Project,Value=agentcore-study Key=Environment,Value=learning Key=Owner,Value=<alias> Key=DeleteAfter,Value=<yyyy-mm-dd> `
      --profile $env:AWS_PROFILE
    ```

12. Guarda el valor `repositoryUri` en
    `course\entregas\capitulo-2\runbook-despliegue-runtime.md`.
13. Obtén el identificador de cuenta:

    ```powershell
    $env:AWS_ACCOUNT_ID = (aws sts get-caller-identity `
      --query Account --output text --profile $env:AWS_PROFILE)
    ```

14. Inicia sesión en ECR:

    ```powershell
    aws ecr get-login-password `
      --region $env:AWS_REGION `
      --profile $env:AWS_PROFILE |
      docker login `
      --username AWS `
      --password-stdin "$env:AWS_ACCOUNT_ID.dkr.ecr.$env:AWS_REGION.amazonaws.com"
    ```

## Bloque 4: Construir y publicar la imagen

15. Construye la imagen desde el directorio del agente:

    ```powershell
    docker build `
      --file app\Dockerfile `
      --tag "$env:ECR_REPOSITORY`:$env:IMAGE_TAG" `
      app
    ```

16. Etiqueta la imagen con la URI de ECR:

    ```powershell
    $env:ECR_URI = "$env:AWS_ACCOUNT_ID.dkr.ecr.$env:AWS_REGION.amazonaws.com/$env:ECR_REPOSITORY"
    docker tag "$env:ECR_REPOSITORY`:$env:IMAGE_TAG" "$env:ECR_URI`:$env:IMAGE_TAG"
    ```

17. Publica una única imagen:

    ```powershell
    docker push "$env:ECR_URI`:$env:IMAGE_TAG"
    ```

18. Obtén y registra el digest:

    ```powershell
    aws ecr describe-images `
      --repository-name $env:ECR_REPOSITORY `
      --image-ids imageTag=$env:IMAGE_TAG `
      --region $env:AWS_REGION `
      --profile $env:AWS_PROFILE `
      --query "imageDetails[0].imageDigest" `
      --output text
    ```

19. Confirma que la imagen no contiene archivos de credenciales revisando
    `.dockerignore` y el contenido de la imagen.

## Bloque 5: Crear el Runtime

20. Ejecuta el asistente de creación de AgentCore CLI:

    ```powershell
    agentcore create --name agentcore-study-agent --defaults
    ```

21. Si el asistente solicita región, selecciona `<aws-region>`.
22. Configura el Runtime con:
    - imagen: `<ecr-repository-uri>:v1`;
    - rol: `agentcore-study-execution`;
    - endpoint de prueba: `agentcore-study-test`;
    - etiquetas del capítulo 1;
    - versión inicial: `v1`.
23. Si el CLI no admite la imagen existente en el flujo elegido, abre
    **Amazon Bedrock > AgentCore > Runtime > Create runtime** y usa el mismo
    URI, rol, región y etiquetas.
24. Ejecuta el despliegue:

    ```powershell
    agentcore deploy
    ```

25. Guarda en el runbook el ARN o identificador del Runtime, endpoint,
    versión, región y fecha de creación.
26. Espera el estado `Ready` o equivalente antes de invocar.

## Bloque 6: Invocar y registrar resultados

27. Desde el entorno virtual, instala Boto3 si aún no está instalado:

    ```powershell
    python -m pip install -r app\requirements-dev.txt
    ```

28. Ejecuta una invocación válida:

    ```powershell
    python app\client.py `
      --runtime-arn "<runtime-arn>" `
      --region $env:AWS_REGION `
      --profile $env:AWS_PROFILE `
      --input "¿Cuál es el horario sintético de soporte?"
    ```

29. Comprueba `status=completed`, `output` y `session_id`.
30. Ejecuta una invocación con `input` vacío y registra el error explícito.
31. Ejecuta dos invocaciones con sesiones distintas y confirma que cada
    respuesta conserva su propio `session_id`.
32. Ejecuta una llamada con un timeout controlado desde un entorno de prueba;
    registra el tipo de error sin repetir llamadas automáticamente.
33. Guarda únicamente resultados sintéticos, identificadores y estados en el
    runbook. No guardes tokens, credenciales ni respuestas sensibles.

## Bloque 7: Publicar la segunda versión y revertir

34. Cambia solo el texto de respuesta del agente y conserva el contrato.
35. Define el segundo tag:

    ```powershell
    $env:IMAGE_TAG="v2"
    ```

36. Construye, etiqueta y publica la imagen como en el bloque 4.
37. Despliega la nueva versión con el mismo Runtime y un endpoint de
    validación separado, o con el mecanismo de versionado mostrado por el
    CLI.
38. Invoca `v2`, registra su identificador y valida el contrato.
39. Restablece el endpoint de prueba a `v1` mediante **Update endpoint** o el
    comando equivalente mostrado por `agentcore --help`.
40. Invoca de nuevo y registra que la respuesta corresponde a `v1`.
41. No dejes ambos endpoints activos al terminar la validación.

## Bloque 8: Inventario y limpieza

42. Completa todos los campos de
    `course\entregas\capitulo-2\runbook-despliegue-runtime.md`.
43. Lista las imágenes publicadas:

    ```powershell
    aws ecr describe-images `
      --repository-name $env:ECR_REPOSITORY `
      --region $env:AWS_REGION `
      --profile $env:AWS_PROFILE
    ```

44. Deshabilita o elimina el endpoint y la versión de prueba desde AgentCore
    CLI o la consola.
45. Elimina el Runtime cuando no lo reutilice el capítulo 3.
46. Elimina el repositorio ECR y sus imágenes:

    ```powershell
    aws ecr delete-repository `
      --repository-name $env:ECR_REPOSITORY `
      --region $env:AWS_REGION `
      --force `
      --profile $env:AWS_PROFILE
    ```

47. Elimina el rol y las políticas creados exclusivamente para el Runtime
    después de retirar sus asociaciones.
48. Confirma en AgentCore, ECR, IAM y Billing que no quedan recursos del
    ejercicio.
49. Cierra la sesión temporal del perfil y conserva MFA.
