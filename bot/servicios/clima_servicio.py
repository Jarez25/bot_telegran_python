import requests
import threading
import time
from telebot.types import Message


def obtener_clima_texto(ciudad, WEATHER_API_KEY):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={WEATHER_API_KEY}&units=metric&lang=es"
    try:
        respuesta = requests.get(url)
        datos = respuesta.json()

        if datos.get("cod") != 200:
            return f"No se pudo obtener el clima: {datos.get('message', 'Error desconocido')}"

        temp = datos['main']['temp']
        descripcion = datos['weather'][0]['description']
        humedad = datos['main']['humidity']
        viento = datos['wind']['speed']

        mensaje = (
            f"🌤️ Clima en {ciudad}:\n"
            f"- Temperatura: {temp}°C\n"
            f"- Estado: {descripcion}\n"
            f"- Humedad: {humedad}%\n"
            f"- Viento: {viento} m/s"
        )
        return mensaje
    except Exception as e:
        return f"Error al obtener el clima: {e}"


def comando_clima(bot, WEATHER_API_KEY):
    @bot.message_handler(commands=['clima'])
    def manejar_clima(message: Message):
        ciudad = "Managua,NI"
        mensaje = obtener_clima_texto(ciudad, WEATHER_API_KEY)
        bot.reply_to(message, mensaje)


def enviar_clima_periodicamente(bot, WEATHER_API_KEY, chat_id, ciudad="Managua,NI"):
    def tarea():
        while True:
            mensaje = obtener_clima_texto(ciudad, WEATHER_API_KEY)
            bot.send_message(chat_id, mensaje)
            time.sleep(600)  # 600 segundos = 10 minutos
    hilo = threading.Thread(target=tarea)
    hilo.daemon = True
    hilo.start()
