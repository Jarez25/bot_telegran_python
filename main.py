import telebot
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Obtener el token del entorno
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Inicializar el bot
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hola, este bot está hecho para GBP.")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Ayuda: Este bot puede ayudarte a obtener información sobre GBP.")

@bot.message_handler(func=lambda message: True)
def send_message(message):
    bot.reply_to(message, message.text)

if __name__ == '__main__':
    try:
        print("Bot is running...")
        bot.polling()
    except Exception as e:
        print(f"An error occurred: {e}")
