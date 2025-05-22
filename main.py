import telebot
from telebot import types
import requests
import os

from insert_user import insert_user
from dotenv import load_dotenv

# Tu token de Telegram
API_TOKEN = os.getenv('TELEGRAM_TOKEN') 

# API Key de OpenWeatherMap
WEATHER_API_KEY = os.getenv('WEATHER_API')

bot = telebot.TeleBot(API_TOKEN)


# Lista de desarrolladores
desarrolladores = ["@jarez", "(vacío)", "(vacío)"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola, este bot está hecho para GBP.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Ayuda:\n/agregar nombre - Agrega un nombre de usuario\n/clima - Muestra el clima actual de Managua\n/desarrolladores - Ver los desarrolladores de GBP")

@bot.message_handler(commands=['agregar'])
def agregar_usuario(message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    insert_user(telegram_id, username)
    bot.reply_to(message, f"Usuario {username} agregado con ID {telegram_id}.")

@bot.message_handler(commands=['clima'])
def obtener_clima(message):
    ciudad = "Managua,NI"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={WEATHER_API_KEY}&units=metric&lang=es"
    
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()

        if datos.get("cod") != 200:
            bot.reply_to(message, f"No se pudo obtener el clima: {datos.get('message', 'Error desconocido')}")
            return

        temp = datos['main']['temp']
        descripcion = datos['weather'][0]['description']
        humedad = datos['main']['humidity']
        viento = datos['wind']['speed']

        mensaje = f"🌤️ Clima en Managua:\n- Temperatura: {temp}°C\n- Estado: {descripcion}\n- Humedad: {humedad}%\n- Viento: {viento} m/s"
        bot.reply_to(message, mensaje)

    except Exception as e:
        bot.reply_to(message, f"Error al obtener el clima: {e}")

@bot.message_handler(commands=['desarrolladores'])
def mostrar_desarrolladores(message):
    mensaje = "👨‍💻 Desarrolladores de GBP:\n"
    for i, dev in enumerate(desarrolladores, start=1):
        mensaje += f"{i}. {dev}\n"
    bot.reply_to(message, mensaje)



@bot.message_handler(commands=['Woo'])
def send_option(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_si = types.InlineKeyboardButton('Sí', callback_data='Ejecutar')
    btn_no = types.InlineKeyboardButton('No', callback_data='cancelar')    
    
    markup.add(btn_si, btn_no)
    bot.send_message(message.chat.id, "¿Quieres sincronizar tus productos en tu tienda?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Ejecutar':
        bot.send_message(call.message.chat.id, "Sincronizando productos...")
    elif call.data == 'cancelar':
        bot.send_message(call.message.chat.id, "Sincronización cancelada.")
        

@bot.message_handler(commands=['waifu'])
def send_waifu(message):
    image_url = "https://i.pinimg.com/736x/d9/3e/39/d93e397f69f3d0eb75969cf9bde0dd85.jpg"
    try:
        bot.send_photo(message.chat.id, image_url)
    except Exception as e:
        bot.reply_to(message, f"Error al enviar la imagen: {e}")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
      
if __name__ == '__main__':
    try:
        print("Bot is running...")
        bot.polling()
    except Exception as e:
        print(f"An error occurred: {e}")
