import telebot
import random

import telebot
import random

TOKEN = 8167751851:AAEK5N99dVhKqBlKuJAm_sdXMdx8Tw5vk88" bot = telebot.TeleBot(TOKEN)

eco_tips = [
    "Bring a reusable bag when shopping instead of using plastic bags.",
    "Buy fruits and vegetables without plastic packaging.",
    "Use a reusable water bottle instead of single-use bottles.",
    "Plan your shopping to reduce food waste.",
    "Repair items instead of throwing them away.",
    "Use reusable containers for take-away food.",
    "Separate your waste properly at home."
]

eco_challenges = [
    "Avoid single-use plastic for the whole day.",
    "Drink only tap water or water from a reusable bottle today.",
    "Buy at least one product without plastic packaging.",
    "Do not throw away any food today.",
    "Use public transport, walk, or bike instead of a car.",
    "Reuse something instead of buying it new today.",
    "Sort all your waste correctly today."
]

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🌱 Welcome to the Eco Bot!\n\n"
        "I help adults reduce waste in everyday life.\n\n"
        "Commands:\n"
        "/tip – Get an eco-friendly tip\n"
        "/challenge – Get a daily eco challenge\n"
        "/help – Show help"
    )

@bot.message_handler(commands=["tip"])
def tip(message):
    bot.send_message(message.chat.id, random.choice(eco_tips))

@bot.message_handler(commands=["challenge"])
def challenge(message):
    bot.send_message(
        message.chat.id,
        "♻️ Today's challenge:\n"
        + random.choice(eco_challenges)
    )

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ This bot gives simple tips and challenges\n"
        "to help adults live more sustainably."
    )

bot.polling()