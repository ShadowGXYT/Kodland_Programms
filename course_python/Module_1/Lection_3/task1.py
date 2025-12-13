import telebot
import random
from bot_logic import gen_pass

    # Замени 'TOKEN' на токен твоего бота
    # Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot("8160895447:AAF8mFVOieZrH_gqrMPxVMSDse8O_7maLdM")
    
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")
    
@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.reply_to(message, "Привет! Как дела?")
    
@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.reply_to(message, "Пока! Удачи!")
    
@bot.message_handler(commands=['pw'])
def send_password(message):
    numbers = [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    def gen_pass(pass_length):
        elements = "+-/*!&$#?=@<>123456789"
        password = ""
        for i in range(pass_length):
            password += random.choice(elements)
        return password
    password = gen_pass(random.choice(numbers))
    bot.reply_to(message, password)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.polling()