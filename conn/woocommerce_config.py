import os
from dotenv import load_dotenv
from woocommerce import API

# Cargar el archivo .env desde la raíz del proyecto
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

# Obtener las variables del entorno
WC_URL = os.getenv("WC_URL")
WC_CONSUMER_KEY = os.getenv("WC_CONSUMER_KEY")
WC_CONSUMER_SECRET = os.getenv("WC_CONSUMER_SECRET")

# Conexión WooCommerce
wcapi = API(
    url=WC_URL,
    consumer_key=WC_CONSUMER_KEY,
    consumer_secret=WC_CONSUMER_SECRET,
    version="wc/v3",
    timeout=30
)

mensajes_bot = []
