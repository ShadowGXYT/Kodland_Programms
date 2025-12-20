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

# --- Passwort Generator ---
@bot.message_handler(commands=['pw'])
def send_password(message):
    elements = "+-/*!&$#?=@<>123456789"
    pass_length = random.randint(8, 24)
    password = "".join(random.choice(elements) for _ in range(pass_length))
    bot.reply_to(message, password)

# --- Emoji Generator ---
@bot.message_handler(commands=['emoji'])
def gen_emoji(message):
    emojis = ["😀", "🙂", "😆", "🤣"]
    bot.reply_to(message, random.choice(emojis))

# --- Münzwurf ---
@bot.message_handler(commands=['flip_coin'])
def flip_coin(message):
    result = random.choice(["ОРЕЛ", "РЕШКА"])
    bot.reply_to(message, result)

# --- 'heh' Command ---
@bot.message_handler(commands=['heh'])
def send_heh(message):
    count = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count)

# --- Sterne-Shop ---
PRICES = {
    '10 Stars': 10,
    '50 Stars': 45,
    '100 Stars': 80,
    '500 Stars': 350
}

@bot.message_handler(commands=['buy_stars'])
def send_shop(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [types.KeyboardButton(product) for product in PRICES.keys()]
    markup.add(*buttons)
    bot.reply_to(message,
                 "Welcome to Stars Payment Bot!\nPlease select amount of stars to purchase:",
                 reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in PRICES.keys())
def handle_product_selection(message):
    product = message.text
    price = PRICES[product]
    prices = [types.LabeledPrice(label=product, amount=price)]
    bot.send_invoice(
        message.chat.id,
        title=f"Purchase {product}",
        description=f"Buy {product} for your account",
        provider_token='',
        currency='XTR',
        prices=prices,
        start_parameter='stars-payment',
        invoice_payload=product
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    product = message.successful_payment.invoice_payload
    bot.reply_to(message, f"Payment for {product} successful!")

# --- User Form (/who_am_I) ---
@bot.message_handler(commands=['who_am_I'])
def send_form(message):
    msg = bot.reply_to(message, "Hi there, I am Example bot. What's your name?")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        user = User(message.text)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except:
        bot.reply_to(message, 'oooops')

def process_age_step(message):
    try:
        chat_id = message.chat.id
        if not message.text.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = message.text
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender?', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except:
        bot.reply_to(message, 'oooops')

def process_sex_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        if message.text in ['Male', 'Female']:
            user.sex = message.text
            bot.send_message(chat_id, f'Nice to meet you {user.name}\nAge: {user.age}\nSex: {user.sex}')
        else:
            raise Exception("Unknown sex")
    except:
        bot.reply_to(message, 'oooops')

# --- Help Command ---
@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message,
                 "📖 Available commands:\n"
                 "/start – start the bot\n"
                 "/hello – greeting\n"
                 "/bye – goodbye\n"
                 "/pw – generate random password\n"
                 "/emoji – random emoji\n"
                 "/flip_coin – coin flip\n"
                 "/heh [number] – repeat 'he'\n"
                 "/buy_stars – stars shop\n"
                 "/who_am_I – user form\n"
                 "/help – show this message")

# --- Echo Handler ---
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# --- Save & Load Next Step Handlers ---
bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

# --- Start Bot ---
bot.infinity_polling()
