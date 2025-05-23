import telebot
from telebot import types
import requests
import os
import subprocess
from insert_user import insert_user
from dotenv import load_dotenv
from woocommerce_import import obtener_producto_por_sku

API_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API')
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola, este bot está hecho para GBP.")


@bot.message_handler(commands=['help'])
def send_help(message):
    texto_ayuda = (
        "🤖 *Funciones del bot GBP:*\n\n"
        "/start - Inicia el bot y muestra un mensaje de bienvenida.\n"
        "/help - Muestra esta lista de comandos disponibles.\n"
        "/clima - Muestra el clima actual de Managua.\n"
        "/Woo - Pregunta si quieres sincronizar los productos en tu tienda WooCommerce.\n"
        "/update - Actualiza los productos en tu tienda WooCommerce.\n"
        "/producto SKU - Consulta la información de un producto usando su SKU.\n"
    )
    bot.reply_to(message, texto_ayuda, parse_mode="Markdown")


@bot.message_handler(commands=['clima'])
def obtener_clima(message):
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

        mensaje = f"🌤️ Clima en Managua:\n- Temperatura: {temp}°C\n- Estado: {descripcion}\n- Humedad: {humedad}%\n- Viento: {viento} m/s"
        bot.reply_to(message, mensaje)

    except Exception as e:
        bot.reply_to(message, f"Error al obtener el clima: {e}")


@bot.message_handler(commands=['agregar'])
def agregar_usuario(message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    insert_user(telegram_id, username)
    bot.reply_to(message, f"Usuario {username} agregado con ID {telegram_id}.")


@bot.message_handler(commands=['Woo'])
def send_option(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_si = types.InlineKeyboardButton('Sí', callback_data='Ejecutar')
    btn_no = types.InlineKeyboardButton('No', callback_data='cancelar')
    markup.add(btn_si, btn_no)
    bot.send_message(
        message.chat.id, "¿Quieres sincronizar tus productos en tu tienda?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Ejecutar':
        bot.send_message(call.message.chat.id, "🔄 Sincronizando productos...")
        try:
            # Ejecuta el script de importación
            subprocess.run(["python", "woocommerce_import.py"], check=True)

            # Lee los mensajes generados
            with open("mensajes_bot.txt", "r", encoding="utf-8") as f:
                mensajes = f.readlines()

            # Envía los mensajes al usuario uno por uno
            if mensajes:
                for msg in mensajes:
                    bot.send_message(call.message.chat.id, msg.strip())
            else:
                bot.send_message(call.message.chat.id,
                                 "⚠️ No se generaron mensajes.")

        except subprocess.CalledProcessError as e:
            bot.send_message(call.message.chat.id,
                             f"❌ Error al sincronizar: {e}")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ Error inesperado: {e}")

    elif call.data == 'cancelar':
        bot.send_message(call.message.chat.id, "❌ Sincronización cancelada.")


@bot.message_handler(commands=['update'])
def update_products(message):
    bot.send_message(message.chat.id, "🔄 Actualizando productos...")

    try:
        subprocess.run(
            ["python", "woocommerce_import.py", "update"], check=True)

        with open("mensajes_bot.txt", "r", encoding="utf-8") as f:
            mensajes = f.readlines()

        if mensajes:
            for msg in mensajes:
                bot.send_message(message.chat.id, msg.strip())
        else:
            bot.send_message(message.chat.id, "⚠️ No se generaron mensajes.")

    except subprocess.CalledProcessError as e:
        bot.send_message(message.chat.id, f"❌ Error al actualizar: {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error inesperado: {e}")


@bot.message_handler(commands=['producto'])  # obtener producto por SKU
def consultar_producto(message):
    partes = message.text.strip().split()
    if len(partes) < 2:
        bot.send_message(
            message.chat.id, "❗️Por favor, usa el comando así: /producto SKU_DEL_PRODUCTO")
        return

    sku = partes[1]
    producto = obtener_producto_por_sku(sku)

    if producto:
        tipo = producto.get("type", "desconocido")
        nombre = producto.get("name", "Sin nombre")
        precio = producto.get("regular_price", "No disponible")
        stock = producto.get("stock_quantity", "No gestionado")
        status = producto.get("status", "desconocido")
        mensaje = (
            f"📦 *Producto encontrado*\n"
            f"🆔 SKU: `{sku}`\n"
            f"📛 Nombre: *{nombre}*\n"
            f"🔖 Tipo: `{tipo}`\n"
            f"💰 Precio: {precio}\n"
            f"📦 Stock: {stock}\n"
            f"📡 Estado: {status}"
        )
        bot.send_message(message.chat.id, mensaje, parse_mode="Markdown")
    else:
        bot.send_message(
            message.chat.id, f"❌ No se encontró ningún producto con el SKU `{sku}`.", parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    try:
        print("Bot is running...")
        bot.polling()
    except Exception as e:
        print(f"An error occurred: {e}")
