import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from simple_salesforce import Salesforce
import certifi

# Configurar certificados SSL
os.environ['SSL_CERT_FILE'] = certifi.where()

# Cargar variables de entorno
load_dotenv()

# 🔧 Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuración Slack
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Configuración Salesforce
SF_USERNAME = os.getenv("SF_USERNAME")
SF_PASSWORD = os.getenv("SF_PASSWORD")
SF_TOKEN = os.getenv("SF_TOKEN")
SF_DOMAIN = "test"  # Cambiar a "test" si estás en sandbox

# 🔌 Conexión a Salesforce
try:
    logger.info("Conectando a Salesforce...")
    sf = Salesforce(
        username=SF_USERNAME,
        password=SF_PASSWORD,
        security_token=SF_TOKEN,
        domain=SF_DOMAIN
    )
    logger.info("Conexión a Salesforce exitosa.")
except Exception as e:
    logger.error(f"Error al conectar a Salesforce: {e}")
    raise

# 🤖 Crear app de Slack
app = App(token=SLACK_BOT_TOKEN)

# 🛠️ Comando personalizado
@app.command("/update_case")
def handle_command(ack, respond, command):
    ack()
    logger.info(f"Comando recibido: {command['text']} de {command['user_name']}")
    try:
        parts = command["text"].split()
        if len(parts) != 2:
            error_msg = "Formato inválido. Uso correcto: /update_case <CaseID> <NuevoEstado>"
            logger.warning(error_msg)
            respond(error_msg)
            return
        case_id, new_status = parts
    except ValueError:
        error_msg = "Formato inválido. Uso correcto: /update_case <CaseID> <NuevoEstado>"
        logger.warning(error_msg)
        respond(error_msg)
        return

    try:
        logger.info(f"Actualizando Case {case_id} con estado {new_status}")
        sf.Case.update(case_id, {"Status": new_status})
        logger.info(f"Case {case_id} actualizado correctamente.")
        respond(f"✅ Caso {case_id} actualizado a estado *{new_status}*")
    except Exception as e:
        logger.error(f"Error al actualizar el caso {case_id}: {e}")
        respond(f"❌ Error al actualizar el caso: {e}")

# 🚀 Iniciar Socket Mode
if __name__ == "__main__":
    logger.info("Iniciando aplicación Slack en modo socket...")
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
