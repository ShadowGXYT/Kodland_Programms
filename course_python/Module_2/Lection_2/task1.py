import telebot
import random

TOKEN = "8167751851:AAEK5N99dVhKqBlKuJAm_sdXMdx8Tw5vk88"
bot = telebot.TeleBot(TOKEN)

eco_tips = [
    "Nimm beim Einkaufen immer eine Stofftasche statt Plastiktüten.",
    "Kaufe Obst und Gemüse lose und vermeide Plastikverpackungen.",
    "Nutze eine wiederverwendbare Trinkflasche statt Einwegflaschen.",
    "Plane deine Einkäufe, um Lebensmittelverschwendung zu vermeiden.",
    "Reparieren statt wegwerfen – viele Dinge lassen sich leicht reparieren.",
    "Verwende Mehrwegbehälter für Essen to go.",
    "Trenne deinen Müll konsequent zu Hause."
]

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "🌱 Willkommen beim Umwelt-Bot!\n\n"
        "Ich helfe dir, im Alltag weniger Abfall zu produzieren.\n\n"
        "Befehle:\n"
        "/tipp – Erhalte einen Umwelt-Tipp\n"
        "/challenge – Kleine Aufgabe für heute\n"
        "/hilfe – Hilfe anzeigen"
    )

@bot.message_handler(commands=["tipp"])
def tip(message):
    bot.send_message(message.chat.id, random.choice(eco_tips))

@bot.message_handler(commands=["challenge"])
def challenge(message):
    bot.send_message(
        message.chat.id,
        "♻️ Tages-Challenge:\n"
        "Versuche heute, keinen Einweg-Plastikartikel zu benutzen!"
    )

@bot.message_handler(commands=["hilfe"])
def help_command(message):
    bot.send_message(
        message.chat.id,
        "ℹ️ Dieser Bot gibt dir einfache Tipps,\n"
        "um als Erwachsener umweltfreundlicher zu leben."
    )

bot.polling()
