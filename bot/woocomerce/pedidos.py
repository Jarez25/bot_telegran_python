# En bot/woocomerce/pedidos.py
from telebot import types
from telebot.types import Message
from conn.woocommerce_config import wcapi
from funciones.filtros_pedidos import obtener_pedidos_por_estado
from funciones.exportar_pedidos_csv import exportar_pedidos_csv
from pdf.factura_pdf import generar_factura_ultimo_pedido


def registrar_comandos_pedidos(bot):

    @bot.message_handler(commands=['descargar_pedidos'])
    def descargar_pedidos(message):
        bot.send_message(message.chat.id, "🔄 Generando archivo de pedidos...")

        try:
            archivo = exportar_pedidos_csv()
            with open(archivo, "rb") as f:
                bot.send_document(message.chat.id, f,
                                  caption="📦 Aquí tienes los pedidos en CSV.")
        except Exception as e:
            bot.send_message(
                message.chat.id, f"❌ Error al generar el archivo: {e}")

    from telebot.types import Message


def registrar_comando_pedidos_por_estado(bot):

    @bot.message_handler(commands=['pedidos_estado'])
    def pedidos_por_estado(message: Message):
        try:
            texto = message.text.strip()
            partes = texto.split()
            if len(partes) < 2:
                bot.reply_to(
                    message, "❗️ Por favor, escribe el estado. Ejemplo: /pedidos_estado completed")
                return

            estado = partes[1].lower()
            pedidos = obtener_pedidos_por_estado(estado)

            if not pedidos:
                bot.reply_to(message, f"No hay pedidos con estado '{estado}'.")
                return

            respuesta = f"📋 Pedidos con estado *{estado}*:\n\n"
            for pedido in pedidos:
                # Obtener nombre completo del cliente
                billing = pedido.get('billing', {})
                nombre_cliente = f"{billing.get('first_name', '')} {billing.get('last_name', '')}".strip(
                )
                fecha = pedido.get('date_created', '')[:10]
                total = pedido.get('total', '0')
                pedido_id = pedido.get('id', 'N/A')

                respuesta += f"🧾 Pedido #{pedido_id} - Cliente: {nombre_cliente} - Total: ${total} - Fecha: {fecha}\n"

            bot.reply_to(message, respuesta, parse_mode="Markdown")

        except Exception as e:
            print(f"Error en pedidos_por_estado: {e}")
            bot.reply_to(message, f"❌ Error al obtener pedidos: {e}")


def registrar_comando_factura_pdf(bot):

    @bot.message_handler(commands=['factura'])
    def enviar_factura_pdf(message: Message):
        bot.send_message(
            message.chat.id, "📄 Generando factura del último pedido...")

        try:
            archivo_pdf = generar_factura_ultimo_pedido()

            if archivo_pdf:
                with open(archivo_pdf, "rb") as f:
                    bot.send_document(message.chat.id, f,
                                      caption="🧾 Factura del último pedido")
            else:
                bot.send_message(
                    message.chat.id, "❌ No se pudo generar la factura. No hay pedidos.")
        except Exception as e:
            bot.send_message(
                message.chat.id, f"❌ Error al generar la factura: {e}")
