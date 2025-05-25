from insert_user import insert_user


def registrar_agregar(bot):
    @bot.message_handler(commands=['agregar'])
    def agregar_usuario(message):
        telegram_id = message.from_user.id
        username = message.from_user.username
        insert_user(telegram_id, username)
        bot.reply_to(
            message, f"Usuario {username} agregado con ID {telegram_id}.")
