import telebot
import random
from telebot import types

# Dein Bot-Token hier einfügen
TOKEN = "8160895447:AAF8mFVOieZrH_gqrMPxVMSDse8O_7maLdM"
bot = telebot.TeleBot(TOKEN)

user_dict = {}

# Klasse für Benutzer
class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None

# --- Grundbefehle ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")

@bot.message_handler(commands=['mem'])
def send_mem(message):
    with open('images/mem1.jpg', 'rb') as f:  
        bot.send_photo(message.chat.id, f)