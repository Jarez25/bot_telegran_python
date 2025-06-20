from flask import Flask, request
import telebot
from dotenv import load_dotenv
import os
# from bot.woocomerce.notificaciones import notificar_nuevo_pedido  # ← Desactivado temporalmente

# Cargar variables de entorno
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = 573408663  # Puedes también usar os.getenv("CHAT_ID")

# Crear instancia de Flask y del bot
app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# Webhook de WooCommerce (no envía nada por Telegram ahora)


@app.route('/webhook/pedido', methods=['POST'])
def recibir_pedido():
    data = request.json
    print("Webhook recibido:", data)
    if data and data.get('status') == 'completed':
        # notificar_nuevo_pedido(data, BOT_TOKEN, CHAT_ID)  # ← Comenta esta línea
        print("Notificación desactivada: pedido completado.")
    return {"ok": True}

# Webhook de Telegram (solo imprime, no responde)


@app.route(f'/webhook/telegram/{BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    json_data = request.get_json(force=True)
    update = telebot.types.Update.de_json(json_data)
    print("Mensaje de Telegram recibido:",
          update.message.text if update.message else "Otro tipo")
    # bot.process_new_updates([update])  # ← Si no quieres procesar nada, comenta esta línea
    return {"ok": True}

# Iniciar el servidor Flask


def iniciar_servidor():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    iniciar_servidor()
