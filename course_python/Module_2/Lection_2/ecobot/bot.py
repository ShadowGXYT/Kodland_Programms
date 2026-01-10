import telebot
from dotenv import load_dotenv
import os
from tips import get_tip
from challenges import get_challenge

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🌍 Welcome to Eco Bot!\n\n"
        "Commands:\n"
        "/tip – Get an eco tip 🌱\n"
        "/challenge – Get a daily challenge ♻️\n"
        "/help – Show help ℹ️\n"
        "/clear – Clear previous messages 🧹"
    )

@bot.message_handler(commands=["tip"])
def tip(message):
    bot.send_message(message.chat.id, get_tip())

@bot.message_handler(commands=["challenge"])
def challenge(message):
    bot.send_message(message.chat.id, "♻️ Today's challenge:\n" + get_challenge())

@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ Commands:\n"
        "/tip – Get an eco tip 🌱\n"
        "/challenge – Get a daily challenge ♻️\n"
        "/clear – Clear previous messages 🧹"
    )

# ======================
# /clear Funktion
# ======================
@bot.message_handler(commands=["clear"])
def clear(message):
    chat_id = message.chat.id
    # Versuche die letzten 100 Nachrichten zu löschen
    for i in range(100):
        try:
            bot.delete_message(chat_id, message.message_id - i)
        except:
            pass  # Fehler ignorieren (z.B. wenn die Nachricht schon gelöscht oder nicht erlaubt)
    bot.send_message(chat_id, "🧹 Chat cleared (Bot messages only in private chats).")

bot.polling()
