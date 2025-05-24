from telebot.types import Message
import requests
import os


def comando_clima(bot, WEATHER_API_KEY):
    @bot.message_handler(commands=['clima'])
    def obtener_clima(message: Message):
        ciudad = "Managua,NI"
        url = f"https://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={WEATHER_API_KEY}&units=metric&lang=es"

        try:
            respuesta = requests.get(url)
            datos = respuesta.json()

            if datos.get("cod") != 200:
                bot.reply_to(
                    message, f"No se pudo obtener el clima: {datos.get('message', 'Error desconocido')}")
                return

            temp = datos['main']['temp']
            descripcion = datos['weather'][0]['description']
            humedad = datos['main']['humidity']
            viento = datos['wind']['speed']

            mensaje = (
                f"🌤️ Clima en Managua:\n"
                f"- Temperatura: {temp}°C\n"
                f"- Estado: {descripcion}\n"
                f"- Humedad: {humedad}%\n"
                f"- Viento: {viento} m/s"
            )
            bot.reply_to(message, mensaje)

        except Exception as e:
            bot.reply_to(message, f"Error al obtener el clima: {e}")
