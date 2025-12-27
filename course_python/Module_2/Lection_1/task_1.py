import telebot
import random
from random import choice
from telebot import types

# Bot-Token hier einfügen
TOKEN = "8160895447:AAF8mFVOieZrH_gqrMPxVMSDse8O_7maLdM"
bot = telebot.TeleBot(TOKEN)
memes = ('course_python\Module_2\Lection_1\images\mem1.png', 'course_python\Module_2\Lection_1\images\mem2.png', 'course_python\Module_2\Lection_1\images\mem3.png')

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
    with open(random.choice(memes), 'rb') as f:  
        bot.send_photo(message.chat.id, f)

# --- Start Bot ---
bot.polling()