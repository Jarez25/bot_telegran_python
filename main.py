import telebot
from telebot import types
import requests
import os
import subprocess
from insert_user import insert_user
from dotenv import load_dotenv
from funciones.conteo_productos import contar_productos
from funciones.obtener_producto_sku import obtener_producto_por_sku
from funciones.actualizar_producto import actualizar_producto
from bot.servicios.clima_servicio import comando_clima
from bot.comandos.start import comandos_basicos, comandos_woo
from bot.woocomerce.categoria import comando_categorias
from conn.woocommerce_config import wcapi


API_TOKEN = os.getenv('TELEGRAM_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API')
bot = telebot.TeleBot(API_TOKEN)


comandos_basicos(bot)
bot.set_my_commands(comandos_woo)

comando_clima(bot, WEATHER_API_KEY)


@bot.message_handler(commands=['agregar'])
def agregar_usuario(message):
    telegram_id = message.from_user.id
    username = message.from_user.username
    insert_user(telegram_id, username)
    bot.reply_to(message, f"Usuario {username} agregado con ID {telegram_id}.")


@bot.message_handler(commands=['woo'])
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


# cuenta total de productos
@bot.message_handler(commands=['conteo_productos'])
def handler_contar_productos(message):
    total = contar_productos()
    bot.send_message(
        message.chat.id,
        f"📊 Total de productos en la tienda: *{total}*",
        parse_mode="Markdown"
    )


@bot.message_handler(commands=['todos_los_productos'])  # lista los productos
def listar_productos(message):
    productos = []
    pagina = 1

    while True:
        response = wcapi.get("products", params={
                             "per_page": 100, "page": pagina}).json()
        if not response:
            break
        productos.extend(response)
        pagina += 1

    if productos:
        mensaje = f"📦 Se encontraron *{len(productos)}* productos:\n\n"
        # Muestra los primeros 10 para no saturar
        for producto in productos[:10]:
            nombre = producto.get("name", "Sin nombre")
            sku = producto.get("sku", "Sin SKU")
            mensaje += f"🔹 *{nombre}* (`{sku}`)\n"
        if len(productos) > 10:
            mensaje += f"\n...y {len(productos) - 10} más."
    else:
        mensaje = "❌ No se encontraron productos en la tienda."

    bot.send_message(message.chat.id, mensaje, parse_mode="Markdown")


# sección de categorías
comando_categorias(bot)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
    try:
        print("Bot is running...")
        bot.polling()
    except Exception as e:
        print(f"An error occurred: {e}")
