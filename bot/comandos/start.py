from telebot.types import Message
from telebot.types import BotCommand


def comandos_basicos(bot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message: Message):
        bot.reply_to(message,
                     "👋 ¡Hola! Bienvenido al *Bot de Gestión WooCommerce*.\n\n"
                     "Con este bot podrás consultar productos, sincronizar inventario y realizar acciones útiles para tu tienda en línea.\n\n"
                     "Escribe /help para ver la lista de comandos disponibles.",
                     parse_mode="Markdown")

    @bot.message_handler(commands=['help'])
    def send_help(message: Message):
        texto_ayuda = (
            "🤖 *Funciones del bot WooCommerce:*\n\n"
            "/start - Inicia el bot y muestra un mensaje de bienvenida.\n"
            "/help - Muestra esta lista de comandos disponibles.\n"
            "/clima - Muestra el clima actual de Managua.\n"
            "/woo - Pregunta si quieres sincronizar los productos en tu tienda WooCommerce.\n"
            "/update - Actualiza los productos en tu tienda WooCommerce.\n"
            "/producto SKU - Consulta la información de un producto usando su SKU.\n"
            "/nueva_categoria Nombre - Crea una nueva categoría (ejemplo: /nueva_categoria BOLSO).\n"
            "/listar_categorias - Lista todas las categorías existentes.\n"
            "/editar_categoria ID NuevoNombre - Edita una categoría existente.\n"
            "/eliminar_categoria ID - Elimina una categoría por su ID.\n"
            "/descargar_pedidos - Descarga todos los pedidos en formato CSV.\n"
            "/pedido_estado Estado - Descarga pedidos por estado (ejemplo: /pedido_estado completed).\n"
            "/conteo_productos - Muestra el número total de productos en la tienda.\n"
            "/todos_los_productos - Lista los productos existentes.\n"
            "/exportar_productos - Exporta todos los productos a CSV.\n"
            "/factura - Genera factura PDF del último pedido."
        )
        bot.reply_to(message, texto_ayuda, parse_mode="Markdown")


comandos_woo = [
    BotCommand("start", "Iniciar el bot y mostrar bienvenida"),
    BotCommand("help", "Mostrar lista de comandos"),
    BotCommand("clima", "Mostrar clima de Managua"),
    BotCommand("woo", "Sincronizar productos WooCommerce"),
    BotCommand("update", "Actualizar productos WooCommerce"),
    BotCommand("producto", "Consultar producto por SKU"),
    BotCommand("nueva_categoria", "Crear nueva categoría"),
    BotCommand("listar_categorias", "Listar todas las categorías"),
    BotCommand("editar_categoria", "Editar una categoría existente"),
    BotCommand("eliminar_categoria", "Eliminar una categoría"),
    BotCommand("descargar_pedidos", "Descargar pedidos como CSV"),
    BotCommand("pedido_estado", "Descargar pedidos por estado"),
    BotCommand("conteo_productos", "Mostrar número total de productos"),
    BotCommand("todos_los_productos", "Listar los productos existentes"),
    BotCommand("exportar_productos", "Exportar todos los productos a CSV"),
    BotCommand("factura", "Generar factura PDF del último pedido")
]
