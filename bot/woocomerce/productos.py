import subprocess
from telebot import types
# ajusta si estos están en otro archivo
from conn.woocommerce_config import wcapi
from funciones.conteo_productos import contar_productos
from funciones.obtener_producto_sku import obtener_producto_por_sku


def registrar_comandos_woocommerce(bot):

    @bot.message_handler(commands=['woo'])
    def send_option(message):
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_si = types.InlineKeyboardButton('Sí', callback_data='Ejecutar')
        btn_no = types.InlineKeyboardButton('No', callback_data='cancelar')
        markup.add(btn_si, btn_no)
        bot.send_message(
            message.chat.id,
            "¿Quieres sincronizar tus productos en tu tienda?",
            reply_markup=markup
        )

    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(call):
        if call.data == 'Ejecutar':
            bot.send_message(call.message.chat.id,
                             "🔄 Sincronizando productos...")
            try:
                subprocess.run(["python", "woocommerce_import.py"], check=True)
                with open("mensajes_bot.txt", "r", encoding="utf-8") as f:
                    mensajes = f.readlines()
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
                bot.send_message(call.message.chat.id,
                                 f"❌ Error inesperado: {e}")
        elif call.data == 'cancelar':
            bot.send_message(call.message.chat.id,
                             "❌ Sincronización cancelada.")

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
                bot.send_message(
                    message.chat.id, "⚠️ No se generaron mensajes.")
        except subprocess.CalledProcessError as e:
            bot.send_message(message.chat.id, f"❌ Error al actualizar: {e}")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Error inesperado: {e}")

    @bot.message_handler(commands=['producto'])
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

    @bot.message_handler(commands=['conteo_productos'])
    def handler_contar_productos(message):
        total = contar_productos()
        bot.send_message(
            message.chat.id,
            f"📊 Total de productos en la tienda: *{total}*",
            parse_mode="Markdown"
        )

    @bot.message_handler(commands=['todos_los_productos'])
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
            for producto in productos[:10]:
                nombre = producto.get("name", "Sin nombre")
                sku = producto.get("sku", "Sin SKU")
                mensaje += f"🔹 *{nombre}* (`{sku}`)\n"
            if len(productos) > 10:
                mensaje += f"\n...y {len(productos) - 10} más."
        else:
            mensaje = "❌ No se encontraron productos en la tienda."

        bot.send_message(message.chat.id, mensaje, parse_mode="Markdown")
