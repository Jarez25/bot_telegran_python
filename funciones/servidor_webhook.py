# funciones/servidor_webhook.py
from flask import Flask, request
from bot.woocomerce.notificaciones import notificar_nuevo_pedido
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = 573408663  # O puedes usar os.getenv("CHAT_ID")

app = Flask(__name__)


@app.route('/webhook/pedido', methods=['POST'])
def recibir_pedido():
    data = request.json
    # Imprime los datos recibidos para depurar
    print("Webhook recibido:", data)
    # Solo notificamos si el pedido está completado
    if data and data.get('status') == 'completed':
        notificar_nuevo_pedido(data, BOT_TOKEN, CHAT_ID)
    return {"ok": True}


def iniciar_servidor():
    app.run(host="0.0.0.0", port=5000)
