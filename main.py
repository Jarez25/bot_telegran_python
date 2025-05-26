import telebot
from telebot import types
import requests
import os
from dotenv import load_dotenv
from bot.servicios.clima_servicio import comando_clima
from bot.comandos.start import comandos_basicos, comandos_woo
from bot.woocomerce.categoria import comando_categorias
from bot.comandos.msm import registrar_mensajes
from bot.comandos.agregar import registrar_agregar
from bot.woocomerce.productos import registrar_comandos_woocommerce
from bot.woocomerce.pedidos import registrar_comandos_pedidos, registrar_comando_pedidos_por_estado, registrar_comando_factura_pdf
from conn.woocommerce_config import wcapi


API_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API')
bot = telebot.TeleBot(API_TOKEN)


comandos_basicos(bot)
bot.set_my_commands(comandos_woo)

comando_clima(bot, WEATHER_API_KEY)

# registar agregar usuario
registrar_agregar(bot)

registrar_comandos_woocommerce(bot)
# exportar productos a CSV


# sección de categorías
comando_categorias(bot)
# pedidos CSV
registrar_comandos_pedidos(bot)

registrar_comandos_pedidos(bot)
registrar_comando_pedidos_por_estado(bot)
registrar_comando_factura_pdf(bot)

# mensajes espejos
registrar_mensajes(bot)

if __name__ == '__main__':
    try:
        print("Bot is running...")
        bot.polling()
    except Exception as e:
        print(f"An error occurred: {e}")
