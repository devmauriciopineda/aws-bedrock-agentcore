# Guía AWS: capítulo 1

## Bloque 1: Proteger la cuenta raíz

1. Inicia sesión en la consola de AWS con la cuenta raíz.
2. Abre **IAM > Dashboard > Security recommendations**.
3. Activa MFA para la cuenta raíz.

## Bloque 2: Crear y proteger la identidad administrativa

4. Abre **IAM > Users > Create user**.
5. Introduce `<admin-alias>` como nombre del usuario administrativo de estudio.
6. Activa el acceso a la consola de AWS para este usuario.
7. Define una contraseña inicial y marca la opción para que el usuario la
   cambie al iniciar sesión por primera vez.
8. No actives la creación de access keys para este usuario.
9. En permisos, crea el grupo `agentcore-study-admins`.
10. Asocia temporalmente la política administrada `AdministratorAccess` al
    grupo para poder crear los recursos del laboratorio.
11. Crea el usuario y guarda únicamente el enlace de inicio de sesión, el
    nombre de usuario y el nombre del grupo.
12. Cierra la sesión de la cuenta raíz.
13. Abre el enlace de inicio de sesión de IAM con `<admin-alias>`.
14. Cambia la contraseña cuando AWS lo solicite.
15. En **IAM > Users > <admin-alias> > Security credentials**, selecciona
    **Assign MFA device** y configura MFA.
16. Cierra sesión y vuelve a entrar con `<admin-alias>` usando MFA.

## Bloque 3: Fijar región y configurar el acceso local

17. Selecciona una sola región compatible con Amazon Bedrock AgentCore y
    anota su código como `<aws-region>`.
18. En la consola, abre el selector de región y fija `<aws-region>`.
19. Instala AWS CLI si no está instalada, en versión 2.32.0 o superior; la
    pestaña **Console credentials** del Toolkit también puede instalarla.
20. En **IAM > User groups > agentcore-study-admins > Permissions**, asocia
    la política administrada `SignInLocalDevelopmentAccess` al grupo.
    Habilita el canje de la sesión de consola por credenciales temporales;
    no crees access keys de la cuenta raíz ni del usuario administrativo.
21. Abre **AWS: Add a New Connection** en VS Code, elige **Console
    credentials**, introduce `<profile-name>` como nombre de perfil y
    `<aws-region>` como región, y completa el inicio de sesión en el
    navegador con `<admin-alias>` y MFA. El Toolkit crea el perfil local
    `<profile-name>`, lo activa y lo comparte con la AWS CLI. No elijas
    **IAM credentials**. La sesión dura hasta 12 horas y caduca también para
    la CLI; repite este inicio de sesión cuando ocurra.
22. Ejecuta:

    ```powershell
    aws sts get-caller-identity --profile <profile-name>
    ```

23. Confirma que el `Account` corresponde a la cuenta de estudio.
24. Ejecuta:

    ```powershell
    aws configure get region --profile <profile-name>
    ```

25. Confirma que la región devuelta es `<aws-region>`.

## Bloque 4: Configurar control de costes

26. Abre **Billing and Cost Management > Budgets**.
27. Selecciona **Create budget**.
28. Elige un presupuesto de coste mensual.
29. Asigna el nombre `agentcore-study-budget`.
30. Define un importe mensual bajo y compatible con tu cuenta.
31. Configura una alerta de coste cuando se alcance el porcentaje elegido.
32. Añade un destinatario de alerta.
33. Revisa la configuración y crea el presupuesto.
34. Abre **Billing and Cost Management > Cost Explorer**.
35. Activa Cost Explorer si la consola lo solicita.
36. Guarda una captura del coste actual sin datos personales.

## Bloque 5: Habilitar y comprobar el modelo de Bedrock

37. Abre **Amazon Bedrock > Model access** en `<aws-region>`.
38. Localiza `<model-id>`.
39. Si la consola muestra una acción de habilitación o solicitud de acceso,
    ejecútala para `<model-id>`.
40. Espera el estado habilitado o aprobado antes de continuar.
41. Abre **Amazon Bedrock > Providers or Models** y confirma que el modelo
    está disponible en `<aws-region>`.
42. Ejecuta una prueba mínima desde la consola con texto sintético.
43. No pegues secretos, datos personales ni información de clientes en la
    prueba.

## Bloque 6: Crear permisos y rol de ejecución

44. Abre **IAM > Policies > Create policy**.
45. Selecciona el servicio Amazon Bedrock.
46. Selecciona únicamente las acciones de invocación requeridas por el
    laboratorio, como `InvokeModel` y, si se usará, streaming.
47. Restringe el recurso al ARN del modelo `<model-id>` cuando la consola lo
    permita.
48. Nombra la política `agentcore-study-bedrock-invoke`.
49. Añade las etiquetas `Project=agentcore-study`,
    `Environment=learning` y `Owner=<alias>`.
50. Revisa el resumen de permisos.
51. Crea la política.
52. Abre **IAM > Roles > Create role**.
53. Selecciona el tipo de entidad o servicio que la pantalla de creación de
    AgentCore Runtime indique para asumir el rol.
54. No adivines el principal de confianza: copia únicamente el principal
    mostrado por la documentación o el asistente vigente de AgentCore.
55. Adjunta `agentcore-study-bedrock-invoke`.
56. Nombra el rol `agentcore-study-execution`.
57. Añade las etiquetas `Project=agentcore-study`,
    `Environment=learning`, `Owner=<alias>` y
    `DeleteAfter=<yyyy-mm-dd>`.
58. Revisa la política de confianza y los permisos.
59. Crea el rol.
60. Abre el rol recién creado y guarda solo su nombre y ARN en el inventario.
61. No guardes credenciales ni tokens.

    ## Bloque 7: Revisar cuotas y disponibilidad de AgentCore

62. Abre **Service Quotas** en `<aws-region>`.
63. Consulta las cuotas de Amazon Bedrock y AgentCore relacionadas con el
    laboratorio.
64. Registra las cuotas relevantes en el inventario.
65. No solicites aumentos de cuota para este ejercicio.
66. Abre **Amazon Bedrock AgentCore** en `<aws-region>`.
67. Comprueba que Runtime, Gateway y Memory aparecen disponibles para la
    región.
68. No crees todavía Runtime, Gateway ni Memory en este capítulo.
69. Confirma que Browser y Code Interpreter permanecen deshabilitados.

    ## Bloque 8: Crear inventario y validar el entorno

70. Crea localmente el archivo de inventario
    `course/entregas/capitulo-1/mapa-arquitectonico-agentcore.md`.
71. Completa región, cuenta, perfil, presupuesto, modelo, política y rol.
72. Añade las etiquetas y la fecha `DeleteAfter`.
73. Ejecuta:

    ```powershell
    aws resourcegroupstaggingapi get-resources `
      --region <aws-region> `
      --resources-per-page 100 `
      --profile <profile-name>
    ```

74. Revisa que no existan recursos de laboratorio inesperados.
75. Abre **Billing > Budgets** y confirma que `agentcore-study-budget` está
    activo.
76. Abre **Cost Explorer** y confirma el coste actual.
77. Guarda la evidencia sin incluir datos sensibles.

    ## Bloque 9: Limpiar recursos y verificar el cierre

78. Si el rol de ejecución no se reutilizará en el capítulo 2, abre **IAM >
    Roles**, selecciona `agentcore-study-execution` y elimínalo.
79. Antes de eliminarlo, elimina las políticas inline y desasocia las
    políticas administradas exclusivas del rol.
80. Si la política `agentcore-study-bedrock-invoke` no se reutilizará, abre
    **IAM > Policies**, selecciona la política y elimínala.
81. Elimina `agentcore-study-budget` solo cuando ya no existan recursos del
    laboratorio.
82. Cierra las sesiones temporales que ya no se utilicen: **Sign out** del
    perfil `<profile-name>` en VS Code o, en la terminal,
    `aws logout --profile <profile-name>`.
83. Mantén MFA de la cuenta raíz y de la identidad administrativa.
84. Vuelve a ejecutar:

    ```powershell
    aws sts get-caller-identity --profile <profile-name>
    ```

85. Confirma que la cuenta y región siguen siendo las esperadas.
