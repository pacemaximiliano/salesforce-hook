# salesforce-hook
_Permite a usuarios de Slack modificar el estado de casos en Salesforce mediante un usuario de servicio utilizando un comando dentro de Slack. El programa se puede modificar para impactar sobre los registros del objeto que se desee_
**¿Cómo funciona?**
1. El usuario ejecuta /update_case 5003h00001abcXYZ Closed
2. Slack envía el comando a tu app Python (Socket Mode)
3. La app valida el input y usa el usuario de servicio para autenticar contra Salesforce
4. Actualiza el campo Status del Case con el ID recibido
5. Envía una respuesta al canal de Slack confirmando el cambio.

**Componentes de la Solución**
* Slack App en modo Socket Mode.
* Slash Command: /update_case <CaseID> <NuevoEstado>
* Autenticación con Salesforce vía usuario de servicio y token de seguridad.
* API REST Salesforce usando simple_salesforce.
* Logs en consola y archivo (app.log) para trazabilidad.
* Gestión de variables sensibles con archivo .env.

**Organización sugerida de archivos**
slack_salesforce_app/
├── app.py
├── .env
├── app.log
└── requirements.txt

**Formato del Comando**
/update_case 5005g00001ABCxyz Cerrado
* 5005g00001ABCxyz → ID del registro Case en Salesforce.
* Cerrado → Nuevo valor para el campo Status.

**-- GUÍA DE IMPLEMENTACIÓN --**
Guía de implementación [Socket Mode]
Crea la aplicación en Slack:
* Ve a Slack API y haz clic en Create New App.
* Selecciona From scratch.
* Asigna un nombre a tu aplicación y selecciona el espacio de trabajo donde la instalarás
Habilitar Socket Mode:
* Dentro de tu aplicación en Slack, ve a Settings > Socket Mode.
* Habilita el Socket Mode para que la aplicación pueda comunicarse en tiempo real con Slack.
* Crea un App Token que te servirá para la conexión con Slack
Solicitar permisos de Slack API:
* En OAuth & Permissions, agrega los siguientes permisos que tu aplicación necesitará para interactuar con Slack:
    * chat:write: Para enviar mensajes.
    * commands: Para crear un comando en Slack (si deseas un comando específico para invocar esta acción).
Agregá un slash command en "Slash Commands":
* Command: /update_case
* Request URL: http://localhost:3000 (no importa para Socket Mode, pero Slack lo pide)


Crear Usuario de Servicio en Salesforce
1. Crear un usuario en Salesforce con acceso API y obtener los siguientes valores
    * client_id
    * client_secret
    * username
    * password
    * security_token 

Consideraciones del usuario
* Dedicado exclusivamente a la integración, no debe ser una cuenta personal.
* Idealmente de tipo "API Only User", si tu licencia lo permite.
* Puede usar el perfil “Integration User” o uno personalizado con permisos mínimos.

Dependiendo de lo que la app haga (ej. actualizar casos), otorgar:
API Enabled ✅ Obligatorio
Read/Write en objeto Case ✅
Acceso al campo Status del objeto Case ✅
View All / Modify All (solo si necesario)	❌ ⚠️ Solo si requiere acceder a todos los registros

_Se recomienda crear un Perfil personalizado o usar Permission Sets para aislar estos permisos_


**Crear la estructura del proyecto**
mkdir slack_salesforce_app
cd slack_salesforce_app
python -m venv venv
source venv/bin/activate # En Windows: venv\Scripts\activate

- Instalar las librerías necesarias
Crear los archivos .env y app.py
- Ejecutar la app
python app.py

Si todo está bien, se va a ver algo por consola como ⚡️ Bolt app is running!
Para probar en Slack, escribir el comando /update_case 5005g00001ABCXYZ Closed y debería verse una respuesta como ✅ Caso 5005g00001ABCXYZ actualizado a estado Closed

