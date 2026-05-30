import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DIR = os.path.dirname(BASE_DIR)
if MAIN_DIR not in sys.path:
    sys.path.insert(0, MAIN_DIR)

from flask import Flask, render_template, request
from General.flight_planner import search_best_flights, CURRENCY_SYMBOLS, TRANSLATIONS

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'), static_folder=os.path.join(BASE_DIR, 'static'))

@app.route("/", methods=["GET", "POST"])
def index():
    flights = []
    error = None
    lang = request.args.get("lang", "DE").upper()
    currency = request.args.get("currency", "CHF").upper()
    
    # Standard-Übersetzungstexte um Zeitfelder erweitern, falls nicht vorhanden
    for l in TRANSLATIONS:
        if "time_pref" not in TRANSLATIONS[l]:
            TRANSLATIONS[l]["time_pref"] = "Gewünschte Uhrzeit (Optional)" if l == "DE" else "Preferred Time (Optional)"
            TRANSLATIONS[l]["placeholder_time"] = "z.B. 15:30 oder 15" if l == "DE" else "e.g. 15:30 or 15"

    if request.method == "POST":
        lang = request.form.get("lang_hidden", lang)
        currency = request.form.get("currency_hidden", currency)
        
        origin = request.form.get("von", "")
        destination = request.form.get("nach", "")
        travel_class = request.form.get("klasse", "ECO")
        pref_time = request.form.get("uhrzeit", "any")
        
        try:
            max_p_str = request.form.get("max_preis", "")
            max_price = float(max_p_str) if max_p_str else None
        except (ValueError, TypeError):
            max_price = None
            
        flights = search_best_flights(origin, destination, max_price, travel_class, currency, pref_time)
        if not flights:
            error = TRANSLATIONS.get(lang, TRANSLATIONS["DE"])["no_flights"]
            
    return render_template(
        "index.html",
        ergebnisse=flights,
        fehler=error,
        symbol=CURRENCY_SYMBOLS.get(currency, "CHF"),
        currency=currency,
        lang=lang,
        text=TRANSLATIONS.get(lang, TRANSLATIONS["DE"]),
        kriterien={"von": request.form.get("von", ""), "nach": request.form.get("nach", "")}
    )

@app.route("/book", methods=["POST"])
def book_flight():
    # Holt die Details des geklickten Fluges aus dem Formular
    flug_daten = {
        "airline": request.form.get("airline"),
        "von": request.form.get("von"),
        "nach": request.form.get("nach"),
        "zeit": request.form.get("zeit"),
        "preis": request.form.get("preis")
    }
    symbol = request.form.get("symbol", "CHF")
    lang = request.form.get("lang_hidden", "DE")
    
    return render_template(
        "booking.html", 
        flug=flug_daten, 
        symbol=symbol, 
        lang=lang
    )

if __name__ == "__main__":
    app.run(port=5000, debug=True)