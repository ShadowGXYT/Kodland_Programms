import os
import sys

# Systempfad setzen, um Zugriff auf 'General' zu erlauben
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from General.flight_planner import search_best_flights, AIRPORT_TRANSLATOR, COUNTRY_TO_AIRPORTS

BOT_TOKEN = "8988008991:AAEfj7PwPH2RND4tCEpcEKDX4bzALOPcvdA"
bot = telebot.TeleBot(BOT_TOKEN)

# Temporärer Speicher für die interaktive Suche (User-ID -> Suchdaten)
USER_SEARCHES = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "✈️ *Welcome to the Interactive SWISS Inspired Bot!*\n\n"
        "You no longer need to type long commands. Just press the button below or type `/flight` to start an interactive search!\n\n"
        "Available Commands:\n"
        "🔍 `/flight` - Start interactive flight search\n"
        "⭐ `/rate` - Rate your experience"
    )
    # Start-Button direkt mitsenden
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔍 Start Flight Search", callback_data="search_start"))
    bot.reply_to(message, welcome_text, parse_mode="Markdown", reply_markup=markup)


# ==================== INTERAKTIVER SCHRITT 1: ABFLUGORT ====================
@bot.message_handler(commands=['flight'])
def handle_flight_command(message):
    start_interactive_search(message.chat.id)

def start_interactive_search(chat_id):
    # Such-Objekt für den User initialisieren
    USER_SEARCHES[chat_id] = {"von": "any", "nach": "any", "klasse": "ECO", "preis": None, "zeit": "any"}
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🇨🇭 Switzerland", callback_data="from_Switzerland"),
        InlineKeyboardButton("🇪🇸 Spain", callback_data="from_Spain"),
        InlineKeyboardButton("🇬🇧 UK (London)", callback_data="from_UK"),
        InlineKeyboardButton("🇦🇪 Dubai", callback_data="from_Dubai"),
        InlineKeyboardButton("🇺🇸 USA (New York)", callback_data="from_USA"),
        InlineKeyboardButton("🌍 Everywhere (Any)", callback_data="from_any")
    )
    bot.send_message(chat_id, "🛫 *Step 1: Where are you departing from?*", parse_mode="Markdown", reply_markup=markup)


# ==================== CALLBACK HANDLER FÜR ALLE SCHRITTE ====================
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    chat_id = call.message.chat.id
    data = call.data

    # Falls der User die Suche über den Start-Button im Welcome-Text aktiviert
    if data == "search_start":
        bot.answer_callback_query(call.id)
        start_interactive_search(chat_id)
        return

    # Zurückweisung, falls die Session abgelaufen ist (z.B. Bot-Neustart)
    if chat_id not in USER_SEARCHES and not data.startswith("rate_"):
        bot.send_message(chat_id, "⚠️ Your session expired. Please type `/flight` to start a new search.")
        bot.answer_callback_query(call.id)
        return

    # STEP 1 ERGEBNIS -> ZU STEP 2 (Zielort)
    if data.startswith("from_"):
        selected_origin = data.split("_")[1]
        USER_SEARCHES[chat_id]["von"] = selected_origin
        
        bot.answer_callback_query(call.id)
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🇨🇭 Switzerland", callback_data="to_Switzerland"),
            InlineKeyboardButton("🇪🇸 Spain", callback_data="to_Spain"),
            InlineKeyboardButton("🇬🇧 UK (London)", callback_data="to_UK"),
            InlineKeyboardButton("🇦🇪 Dubai", callback_data="to_Dubai"),
            InlineKeyboardButton("🇺🇸 USA (New York)", callback_data="to_USA"),
            InlineKeyboardButton("🌍 Anywhere (Any)", callback_data="to_any")
        )
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"🛫 *Origin selected:* {selected_origin.upper()}\n\n🛬 *Step 2: Where do you want to go?*",
            parse_mode="Markdown",
            reply_markup=markup
        )

    # STEP 2 ERGEBNIS -> ZU STEP 3 (Reiseklasse)
    elif data.startswith("to_"):
        selected_dest = data.split("_")[1]
        USER_SEARCHES[chat_id]["nach"] = selected_dest
        
        bot.answer_callback_query(call.id)
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("🎫 Economy Class", callback_data="class_ECO"),
            InlineKeyboardButton("💼 Business Class", callback_data="class_BIZ")
        )
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"🛫 *Origin:* {USER_SEARCHES[chat_id]['von'].upper()}\n🛬 *Destination:* {selected_dest.upper()}\n\n💺 *Step 3: Select your Travel Class:*",
            parse_mode="Markdown",
            reply_markup=markup
        )

    # STEP 3 ERGEBNIS -> ZU STEP 4 (Preisfilter via Chat-Eingabe)
    elif data.startswith("class_"):
        selected_class = data.split("_")[1]
        USER_SEARCHES[chat_id]["klasse"] = selected_class
        
        bot.answer_callback_query(call.id)
        
        # Ein Button für "Kein Limit", falls man nichts tippen will
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("💰 No Price Limit", callback_data="price_skip"))
        
        msg = bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=(
                f"🛫 *Origin:* {USER_SEARCHES[chat_id]['von'].upper()}\n"
                f"🛬 *Destination:* {USER_SEARCHES[chat_id]['nach'].upper()}\n"
                f"💺 *Class:* {selected_class}\n\n"
                f"💵 *Step 4: Please TYPE your maximum price in CHF into the chat now:* (or click below)"
            ),
            parse_mode="Markdown",
            reply_markup=markup
        )
        # Wartet auf die nächste Text-Nachricht des Users im Chat
        bot.register_next_step_handler(msg, process_price_input)

    # STEP 4 ÜBERSPRINGEN -> FINALE SUCHEAUSFÜHRUNG
    elif data == "price_skip":
        USER_SEARCHES[chat_id]["preis"] = None
        bot.answer_callback_query(call.id)
        execute_final_search(chat_id, call.message)

    # BEWERTUNGS-SYSTEM (Bleibt wie vorher)
    elif data.startswith("rate_"):
        rating_value = data.split('_')[1]
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=call.message.message_id,
            text=f"❤️ Thank you! You rated us *{rating_value}/5 stars*. Your feedback helps us improve!",
            parse_mode="Markdown"
        )


# ==================== HILFSFUNKTIONEN FÜR TEXTEINGABE & AUSWERTUNG ====================

def process_price_input(message):
    chat_id = message.chat.id
    if chat_id not in USER_SEARCHES:
        return

    user_text = message.text.strip()
    
    # Versuche die Zahl zu extrahieren
    try:
        # Filtert Buchstaben wie 'CHF' raus, falls der User sie mittiopt
        clean_number = "".join([c for c in user_text if c.isdigit() or c == "."])
        USER_SEARCHES[chat_id]["preis"] = float(clean_number)
    except ValueError:
        # Falls es keine Zahl war, ignorieren wir das Limit einfach (Kulanz)
        USER_SEARCHES[chat_id]["preis"] = None

    # Sende eine Bestätigung und führe die Suche aus
    execute_final_search(chat_id, message)

def execute_final_search(chat_id, message):
    search_data = USER_SEARCHES[chat_id]
    
    # Suche im flight_planner triggern
    flights = search_best_flights(
        origin=search_data["von"],
        destination=search_data["nach"],
        max_price=search_data["preis"],
        travel_class=search_data["klasse"],
        currency="CHF",
        preferred_time="any"
    )
    
    # Schickes visuelles Feedback bauen
    header = (
        f"📊 *Search Summary:*\n"
        f"🛫 From: {search_data['von'].upper()}\n"
        f"🛬 To: {search_data['nach'].upper()}\n"
        f"💺 Class: {search_data['klasse']}\n"
        f"💵 Max Budget: {f'{search_data['preis']:.2f} CHF' if search_data['preis'] else 'Unlimited'}\n"
        f"===========================\n\n"
    )
    
    if not flights:
        bot.send_message(chat_id, header + "❌ *No flights found matching these criteria.*", parse_mode="Markdown")
        return

    response = header + "✨ *Best options found for you:* \n\n"
    for f in flights:
        # Optische Aufwertung durch Airline-Zuweisung
        airline_emoji = "👑" if "Emirates" in f['airline'] else "✈️"
        response += (
            f"{airline_emoji} *{f['airline']}*\n"
            f"📍 Route: {f['von']} → {f['nach']}\n"
            f"🕒 Time: {f['zeit']}\n"
            f"💰 Price: {f['preis']:.2f} CHF\n"
            f"---------------------------\n"
        )
    
    bot.send_message(chat_id, response, parse_mode="Markdown")
    
    # Speicher bereinigen nach erfolgreicher Suche
    del USER_SEARCHES[chat_id]


@bot.message_handler(commands=['rate'])
def handle_rating_request(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("⭐", callback_data="rate_1"),
        InlineKeyboardButton("⭐⭐", callback_data="rate_2"),
        InlineKeyboardButton("⭐⭐⭐", callback_data="rate_3"),
        InlineKeyboardButton("⭐⭐⭐⭐", callback_data="rate_4"),
        InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="rate_5")
    )
    bot.send_message(message.chat.id, "How would you rate your flight search experience?", reply_markup=markup)

if __name__ == "__main__":
    print("🚀 Interactive Bot is polling...")
    bot.infinity_polling()