import telebot
from telebot import types
import requests
import os
import threading
from dotenv import load_dotenv
from bot.servicios.clima_servicio import comando_clima, enviar_clima_periodicamente
from bot.comandos.start import comandos_basicos, comandos_woo
from bot.woocomerce.categoria import comando_categorias
from bot.comandos.msm import registrar_mensajes
from bot.comandos.agregar import registrar_agregar
from bot.woocomerce.productos import registrar_comandos_woocommerce
from bot.woocomerce.pedidos import registrar_comandos_pedidos, registrar_comando_pedidos_por_estado, registrar_comando_factura_pdf
from conn.woocommerce_config import wcapi
from funciones.servidor_webhook import iniciar_servidor  # 💡 Agregado

# Cargar variables del .env
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API')
CHAT_ID = 573408663
bot = telebot.TeleBot(API_TOKEN)

# Registrar comandos
comandos_basicos(bot)
bot.set_my_commands(comandos_woo)
comando_clima(bot, WEATHER_API_KEY)
enviar_clima_periodicamente(bot, WEATHER_API_KEY, CHAT_ID)
registrar_agregar(bot)
registrar_comandos_woocommerce(bot)
comando_categorias(bot)
registrar_comandos_pedidos(bot)
registrar_comando_pedidos_por_estado(bot)
registrar_comando_factura_pdf(bot)
registrar_mensajes(bot)

if __name__ == '__main__':
    try:
        # Inicia el servidor en segundo plano
        threading.Thread(target=iniciar_servidor, daemon=True).start()
        print("Bot y servidor webhook activos...")
        bot.polling()
    except Exception as e:
        print(f"❌ Error general: {e}")
