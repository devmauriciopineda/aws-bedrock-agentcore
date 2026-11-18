# Guía AWS: capítulo 1

1. Inicia sesión en la consola de AWS con la cuenta raíz.
2. Abre **IAM > Dashboard > Security recommendations**.
3. Activa MFA para la cuenta raíz.
4. Cierra la sesión raíz.
5. Inicia sesión con la identidad administrativa de estudio.
6. Abre **IAM Identity Center**.
7. Si la organización de estudio no tiene Identity Center, habilítalo en la
   región indicada por AWS.
8. Crea el usuario administrativo de estudio `<admin-alias>`.
9. Activa MFA para `<admin-alias>`.
10. Asigna a `<admin-alias>` únicamente el acceso administrativo necesario
    para el laboratorio.
11. Cierra sesión y vuelve a entrar con `<admin-alias>`.
12. Selecciona una sola región compatible con Amazon Bedrock AgentCore y
    anota su código como `<aws-region>`.
13. En la consola, abre el selector de región y fija `<aws-region>`.
14. Instala AWS CLI si no está instalada.
15. Configura el acceso de la identidad administrativa mediante el mecanismo
    recomendado por AWS; no crees access keys de la cuenta raíz.
16. Configura el perfil local `<profile-name>`.
17. Ejecuta:

    ```powershell
    aws sts get-caller-identity --profile <profile-name>
    ```

18. Confirma que el `Account` corresponde a la cuenta de estudio.
19. Ejecuta:

    ```powershell
    aws configure get region --profile <profile-name>
    ```

20. Confirma que la región devuelta es `<aws-region>`.
21. Abre **Billing and Cost Management > Budgets**.
22. Selecciona **Create budget**.
23. Elige un presupuesto de coste mensual.
24. Asigna el nombre `agentcore-study-budget`.
25. Define un importe mensual bajo y compatible con tu cuenta.
26. Configura una alerta de coste cuando se alcance el porcentaje elegido.
27. Añade un destinatario de alerta.
28. Revisa la configuración y crea el presupuesto.
29. Abre **Billing and Cost Management > Cost Explorer**.
30. Activa Cost Explorer si la consola lo solicita.
31. Guarda una captura del coste actual sin datos personales.
32. Abre **Amazon Bedrock > Model access** en `<aws-region>`.
33. Localiza `<model-id>`.
34. Si la consola muestra una acción de habilitación o solicitud de acceso,
    ejecútala para `<model-id>`.
35. Espera el estado habilitado o aprobado antes de continuar.
36. Abre **Amazon Bedrock > Providers or Models** y confirma que el modelo
    está disponible en `<aws-region>`.
37. Ejecuta una prueba mínima desde la consola con texto sintético.
38. No pegues secretos, datos personales ni información de clientes en la
    prueba.
39. Abre **IAM > Policies > Create policy**.
40. Selecciona el servicio Amazon Bedrock.
41. Selecciona únicamente las acciones de invocación requeridas por el
    laboratorio, como `InvokeModel` y, si se usará, streaming.
42. Restringe el recurso al ARN del modelo `<model-id>` cuando la consola lo
    permita.
43. Nombra la política `agentcore-study-bedrock-invoke`.
44. Añade las etiquetas `Project=agentcore-study`,
    `Environment=learning` y `Owner=<alias>`.
45. Revisa el resumen de permisos.
46. Crea la política.
47. Abre **IAM > Roles > Create role**.
48. Selecciona el tipo de entidad o servicio que la pantalla de creación de
    AgentCore Runtime indique para asumir el rol.
49. No adivines el principal de confianza: copia únicamente el principal
    mostrado por la documentación o el asistente vigente de AgentCore.
50. Adjunta `agentcore-study-bedrock-invoke`.
51. Nombra el rol `agentcore-study-execution`.
52. Añade las etiquetas `Project=agentcore-study`,
    `Environment=learning`, `Owner=<alias>` y
    `DeleteAfter=<yyyy-mm-dd>`.
53. Revisa la política de confianza y los permisos.
54. Crea el rol.
55. Abre el rol recién creado y guarda solo su nombre y ARN en el inventario.
56. No guardes credenciales ni tokens.
57. Abre **Service Quotas** en `<aws-region>`.
58. Consulta las cuotas de Amazon Bedrock y AgentCore relacionadas con el
    laboratorio.
59. Registra las cuotas relevantes en el inventario.
60. No solicites aumentos de cuota para este ejercicio.
61. Abre **Amazon Bedrock AgentCore** en `<aws-region>`.
62. Comprueba que Runtime, Gateway y Memory aparecen disponibles para la
    región.
63. No crees todavía Runtime, Gateway ni Memory en este capítulo.
64. Confirma que Browser y Code Interpreter permanecen deshabilitados.
65. Crea localmente el archivo de inventario
    `course/entregas/capitulo-1/mapa-arquitectonico-agentcore.md`.
66. Completa región, cuenta, perfil, presupuesto, modelo, política y rol.
67. Añade las etiquetas y la fecha `DeleteAfter`.
68. Ejecuta:

    ```powershell
    aws resourcegroupstaggingapi get-resources `
      --region <aws-region> `
      --resources-per-page 100 `
      --profile <profile-name>
    ```

69. Revisa que no existan recursos de laboratorio inesperados.
70. Abre **Billing > Budgets** y confirma que `agentcore-study-budget` está
    activo.
71. Abre **Cost Explorer** y confirma el coste actual.
72. Guarda la evidencia sin incluir datos sensibles.
73. Si el rol de ejecución no se reutilizará en el capítulo 2, abre **IAM >
    Roles**, selecciona `agentcore-study-execution` y elimínalo.
74. Antes de eliminarlo, elimina las políticas inline y desasocia las
    políticas administradas exclusivas del rol.
75. Si la política `agentcore-study-bedrock-invoke` no se reutilizará, abre
    **IAM > Policies**, selecciona la política y elimínala.
76. Elimina `agentcore-study-budget` solo cuando ya no existan recursos del
    laboratorio.
77. Revoca sesiones temporales que ya no se utilicen.
78. Mantén MFA de la cuenta raíz y de la identidad administrativa.
79. Vuelve a ejecutar:

    ```powershell
    aws sts get-caller-identity --profile <profile-name>
    ```

80. Confirma que la cuenta y región siguen siendo las esperadas.
