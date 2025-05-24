from telebot.types import Message
from telebot.types import BotCommand


def comandos_basicos(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        bot.reply_to(message,
                     "👋 ¡Hola! Bienvenido al *Bot de Gestión WooCommerce*.\n\n"
                     "Con este bot podrás consultar productos, sincronizar inventario y realizar acciones útiles para tu tienda en línea.\n\n"
                     "Escribe /help para ver la lista de comandos disponibles.",)

    @bot.message_handler(commands=['help'])
    def send_help(message: Message):
        texto_ayuda = (
            "🤖 *Funciones del bot WooCommerce:*\n\n"
            "/start \\- Inicia el bot y muestra un mensaje de bienvenida\\.\n"
            "/help \\- Muestra esta lista de comandos disponibles\\.\n"
            "/clima \\- Muestra el clima actual de Managua\\.\n"
            "/woo \\- Pregunta si quieres sincronizar los productos en tu tienda WooCommerce\\.\n"
            "/update \\- Actualiza los productos en tu tienda WooCommerce\\.\n"
            "/producto SKU \\- Consulta la información de un producto usando su SKU\\.\n"
            "/nueva\\_categoria \\- Crea una nueva categoría \\(ejemplo: /nueva\\_categoria BOLSO\\)\\.\n"
        )
        bot.reply_to(message, texto_ayuda, parse_mode="Markdown")


comandos_woo = [
    BotCommand("start", "Iniciar el bot y mostrar bienvenida"),
    BotCommand("help", "Mostrar lista de comandos"),
    BotCommand("clima", "Mostrar clima de Managua"),
    BotCommand("woo", "Sincronizar productos WooCommerce"),  # minúscula
    BotCommand("update", "Actualizar productos WooCommerce"),
    BotCommand("producto", "Consultar producto por SKU"),
    BotCommand("nueva_categoria", "Crear nueva categoría"),
]
