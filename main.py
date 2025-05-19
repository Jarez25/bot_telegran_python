import telebot
import requests
import os
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
    nombre = message.text[len('/agregar '):].strip()
    if len(nombre) >= 3:
        bot.reply_to(message, f"Usuario '{nombre}' agregado correctamente.")
    else:
        bot.reply_to(message, "El nombre debe tener al menos 3 caracteres.")

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

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    try:
        print("Bot is running...")
        bot.polling()
    except Exception as e:
        print(f"An error occurred: {e}")
