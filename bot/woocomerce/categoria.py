from funciones.crear_categoria import crear_categoria
from funciones.listar_categorias import listar_categorias
from funciones.editar_categoria import editar_categoria
from funciones.eliminar_categoria import eliminar_categoria


def comando_categorias(bot):
    @bot.message_handler(commands=['nueva_categoria'])
    def comando_crear_categoria(message):
        partes = message.text.strip().split(maxsplit=1)
        if len(partes) < 2:
            bot.send_message(message.chat.id, "❗️Uso: /nueva_categoria Nombre")
            return

        nombre_categoria = partes[1]
        resultado = crear_categoria(nombre_categoria)
        if resultado:
            bot.send_message(
                message.chat.id,
                f"✅ Categoría creada:\n📛 *{resultado['name']}*\n🆔 `{resultado['id']}`",
                parse_mode="Markdown"
            )
        else:
            bot.send_message(
                message.chat.id, "❌ No se pudo crear la categoría.")

    @bot.message_handler(commands=['listar_categorias'])
    def comando_listar_categorias(message):
        categorias = listar_categorias()
        if not categorias:
            bot.send_message(
                message.chat.id, "❌ No se pudieron obtener las categorías.")
            return

        texto = "📂 *Categorías:*\n\n"
        for cat in categorias:
            texto += f"🆔 `{cat['id']}` - *{cat['name']}*\n"
        bot.send_message(message.chat.id, texto, parse_mode="Markdown")

    @bot.message_handler(commands=['editar_categoria'])
    def comando_editar_categoria(message):
        partes = message.text.strip().split(maxsplit=2)
        if len(partes) < 3:
            bot.send_message(
                message.chat.id, "❗️Uso: /editar_categoria ID NuevoNombre")
            return

        categoria_id = partes[1]
        nuevo_nombre = partes[2]
        resultado = editar_categoria(categoria_id, nuevo_nombre)
        if resultado:
            bot.send_message(
                message.chat.id,
                f"✅ Categoría actualizada:\n🆔 `{resultado['id']}`\n📛 *{resultado['name']}*",
                parse_mode="Markdown"
            )
        else:
            bot.send_message(
                message.chat.id, "❌ No se pudo editar la categoría.")

    @bot.message_handler(commands=['eliminar_categoria'])
    def comando_eliminar_categoria(message):
        partes = message.text.strip().split(maxsplit=1)
        if len(partes) < 2 or not partes[1].isdigit():
            bot.send_message(
                message.chat.id,
                "❗️Por favor, usa el comando así:\n/eliminar_categoria ID_de_la_categoria"
            )
            return

        categoria_id = int(partes[1])
        resultado = eliminar_categoria(categoria_id)

        if resultado:
            bot.send_message(
                message.chat.id,
                f"🗑 Categoría eliminada:\n📛 *{resultado['name']}*\n🆔 `{resultado['id']}`",
                parse_mode="Markdown"
            )
        else:
            bot.send_message(
                message.chat.id, "❌ No se pudo eliminar la categoría.")
