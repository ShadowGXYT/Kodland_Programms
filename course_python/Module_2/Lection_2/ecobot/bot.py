import telebot
from config import TOKEN
from tips import get_tip
from challenges import get_challenge

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🌍 Welcome to Eco Bot!\n\n"
        "I help adults reduce waste in everyday life.\n\n"
        "Commands:\n"
        "/tip – Get an eco tip 🌱\n"
        "/challenge – Get a daily challenge ♻️\n"
        "/help – Show help ℹ️"
    )

@bot.message_handler(commands=["tip"])
def tip(message):
    bot.send_message(message.chat.id, get_tip())

@bot.message_handler(commands=["challenge"])
def challenge(message):
    bot.send_message(
        message.chat.id,
        "♻️ Today's challenge:\n" + get_challenge()
    )

@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ This bot gives simple eco tips and challenges\n"
        "to help adults live more sustainably."
    )

bot.polling()
