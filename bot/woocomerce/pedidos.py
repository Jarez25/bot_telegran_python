# En bot/woocomerce/pedidos.py
from telebot import types
from telebot.types import Message
from conn.woocommerce_config import wcapi
from funciones.filtros_pedidos import obtener_pedidos_por_estado
from funciones.exportar_pedidos_csv import exportar_pedidos_csv


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
        print("Comando /pedidos_estado recibido:",
              message.text)  # <--- Print para debug
        try:
            texto = message.text.strip()
            partes = texto.split()
            if len(partes) < 2:
                bot.reply_to(
                    message, "❗️ Por favor, escribe el estado. Ejemplo: /pedidos_estado completed")
                return

            estado = partes[1].lower()
            pedidos = obtener_pedidos_por_estado(estado)

            # <--- Print para debug
            print(f"Pedidos obtenidos: {len(pedidos)}")

            if not pedidos:
                bot.reply_to(message, f"No hay pedidos con estado '{estado}'.")
                return

            respuesta = f"📋 Pedidos con estado *{estado}*:\n\n"
            for pedido in pedidos:
                cliente = f"{pedido['billing']['first_name']} {pedido['billing']['last_name']}"
                fecha = pedido['date_created'][:10]
                total = pedido['total']
                respuesta += f"🧾 #{pedido['id']} - {cliente} - ${total} - {fecha}\n"

            bot.reply_to(message, respuesta, parse_mode="Markdown")

        except Exception as e:
            print(f"Error en pedidos_por_estado: {e}")  # <--- Print para debug
            bot.reply_to(message, f"❌ Error al obtener pedidos: {e}")
