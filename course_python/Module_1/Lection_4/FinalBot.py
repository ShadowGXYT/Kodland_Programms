import telebot
import random
from telebot import types 
import os

    # Замени 'TOKEN' на токен твоего бота
    # Этот токен ты получаешь от BotFather, чтобы бот мог работать
bot = telebot.TeleBot("8160895447:AAF8mFVOieZrH_gqrMPxVMSDse8O_7maLdM")

user_dict = {}

class User:
    def __init__(self, name):
        self.name = name
        self.age = None
        self.sex = None

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

@bot.message_handler(commands=['emoji'])
def gen_emodji():
    emodji = ["\U0001f600", "\U0001f642", "\U0001F606", "\U0001F923"]
    return random.choice(emodji)

@bot.message_handler(commands=['flip_coin'])
def flip_coin():
    flip = random.randint(0, 2)
    if flip == 0:
        return "ОРЕЛ"
    else:
        return "РЕШКА"

# Обработчик команды '/heh'
@bot.message_handler(commands=['heh'])
def send_heh(message):
    count_heh = int(message.text.split()[1]) if len(message.text.split()) > 1 else 5
    bot.reply_to(message, "he" * count_heh)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Product prices in stars
PRICES = {
    '10 Stars': 10,   # $1.00 - Entry level package
    '50 Stars': 45,   # $4.50 - Medium package with 10% discount
    '100 Stars': 80,  # $8.00 - Large package with 20% discount
    '500 Stars': 350  # $35.00 - Bulk package with 30% discount
}

# Handler for /start command - Then the bot will send amount stars to purchase
@bot.message_handler(commands=['start2'])
def send_welcome(message):
    # Create a custom keyboard with 2 buttons per row
    markup = types.ReplyKeyboardMarkup(row_width=2)
    # Generate buttons for each product in our PRICES dictionary
    buttons = [types.KeyboardButton(product) for product in PRICES.keys()]
    # Add all buttons to the markup
    markup.add(*buttons)
    
    # Send welcome message with the custom keyboard
    bot.reply_to(message, 
                 "Welcome to Stars Payment Bot!\nPlease select amount of stars to purchase:",
                 reply_markup=markup)

# Handler for when user selects a product from the keyboard
@bot.message_handler(func=lambda message: message.text in PRICES.keys())
def handle_product_selection(message):
    # Get selected product and its price
    product = message.text
    price = PRICES[product]
    
    # Create invoice with product details
    prices = [types.LabeledPrice(label=product, amount=price)]
    
    # Send payment invoice to user
    bot.send_invoice(
        message.chat.id,  # Chat ID to send invoice to
        title=f"Purchase {product}",  # Title of the invoice
        description=f"Buy {product} for your account",  # Description shown on invoice
        provider_token='',  # Payment provider token (empty for testing)
        currency='XTR',  # Currency code
        prices=prices,  # List of prices (we only have one item)
        start_parameter='stars-payment',  # Deep-linking parameter
        invoice_payload=product  # Payload to identify the product after payment
    )

# Pre-checkout handler - Called before payment is completed
@bot.pre_checkout_query_handler(func=lambda query: True)
def process_pre_checkout_query(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Handler for successful payments
@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message):
    # Get the product that was purchased from the invoice payload
    product = message.successful_payment.invoice_payload
    bot.reply_to(message, 
                 f"Payment for {product} successful!")

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start3'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Hi there, I am Example bot.
What's your name?
""")
    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        user = user_dict[chat_id]
        user.age = age
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Male', 'Female')
        msg = bot.reply_to(message, 'What is your gender', reply_markup=markup)
        bot.register_next_step_handler(msg, process_sex_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_sex_step(message):
    try:
        chat_id = message.chat.id
        sex = message.text
        user = user_dict[chat_id]
        if (sex == u'Male') or (sex == u'Female'):
            user.sex = sex
        else:
            raise Exception("Unknown sex")
        bot.send_message(chat_id, 'Nice to meet you ' + user.name + '\n Age:' + str(user.age) + '\n Sex:' + user.sex)
    except Exception as e:
        bot.reply_to(message, 'oooops')

# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.polling()