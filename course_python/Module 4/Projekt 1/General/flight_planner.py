import os
import json

# NEUER SUCHPFAD (sucht direkt im selben General-Ordner):
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "flights.json")

def load_flight_database():
    try:
        with open(JSON_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

FLIGHT_DATABASE = load_flight_database()

# Wechselkurse und Symbole erweitert (Wechselkurs CHF zu RUB angepasst)
CURRENCY_RATES = {"CHF": 1.0, "EUR": 1.06, "USD": 1.12, "GBP": 0.88, "RUB": 102.5}
CURRENCY_SYMBOLS = {"CHF": "CHF", "EUR": "€", "USD": "$", "GBP": "£", "RUB": "₽"}

# 1. FLUGHAFEN-ÜBERSETZER (Um Moskau SVO und St. Petersburg LED erweitert)
AIRPORT_TRANSLATOR = {
    "ZURICH": "ZRH", "ZÜRICH": "ZRH", "ZH": "ZRH", "ZRH": "ZRH", "ZURIGO": "ZRH", "ЦЮРИХ": "ZRH",
    "BASEL": "BSL", "BALE": "BSL", "BASILEA": "BSL", "БАЗЕЛЬ": "BSL", "BSL": "BSL",
    "GENEVA": "GVA", "GENF": "GVA", "GENEVE": "GVA", "GINEVRA": "GVA", "ЖЕНЕВА": "GVA", "GVA": "GVA",
    "DUBAI": "DXB", "DUBAÏ": "DXB", "ДУБАЙ": "DXB", "DXB": "DXB",
    "LONDON": "LHR", "LONDRES": "LHR", "LONDRA": "LHR", "ЛОНДОН": "LHR", "LHR": "LHR",
    "NEW YORK": "JFK", "NEW-YORK": "JFK", "НЬЮ-ЙОРК": "JFK", "JFK": "JFK",
    "BARCELONA": "BCN", "BARCELONE": "BCN", "БАРСЕЛОНА": "BCN", "BCN": "BCN",
    "MALLORCA": "PMI", "PALMA": "PMI", "MAJORQUE": "PMI", "МАЛЬОРКА": "PMI", "PMI": "PMI",
    "MADRID": "MAD", "МАДРИД": "MAD", "MAD": "MAD",
    "MOSKAU": "SVO", "MOSCOW": "SVO", "MOSCOU": "SVO", "МОСКВА": "SVO", "SVO": "SVO",
    "ST. PETERSBURG": "LED", "SAINT PETERSBURG": "LED", "САНКТ-ПЕТЕРБУРГ": "LED", "LED": "LED"
}

# 2. LÄNDER-ÜBERSETZER (Russland hinzugefügt)
COUNTRY_TO_AIRPORTS = {
    "SCHWEIZ": ["ZRH", "BSL", "GVA"], "SWITZERLAND": ["ZRH", "BSL", "GVA"], "CH": ["ZRH", "BSL", "GVA"], "SUISSE": ["ZRH", "BSL", "GVA"], "SVIZZERA": ["ZRH", "BSL", "GVA"], "ШВЕЙЦАРИЯ": ["ZRH", "BSL", "GVA"],
    "SPANIEN": ["BCN", "PMI", "MAD"], "SPAIN": ["BCN", "PMI", "MAD"], "ES": ["BCN", "PMI", "MAD"], "ESPAGNE": ["BCN", "PMI", "MAD"], "SPAGNA": ["BCN", "PMI", "MAD"], "ИСПАНИЯ": ["BCN", "PMI", "MAD"],
    "USA": ["JFK"], "VEREINIGTE STAATEN": ["JFK"], "UNITED STATES": ["JFK"], "ETATS-UNIS": ["JFK"], "STATI UNITI": ["JFK"], "США": ["JFK"],
    "VAE": ["DXB"], "DUBAI": ["DXB"], "UNITED ARAB EMIRATES": ["DXB"], "ОАЭ": ["DXB"],
    "ENGLAND": ["LHR"], "GROSSBRITANNIEN": ["LHR"], "UK": ["LHR"], "UNITED KINGDOM": ["LHR"], "ВЕЛИКОБРИТАНИЯ": ["LHR"],
    "RUSSLAND": ["SVO", "LED"], "RUSSIA": ["SVO", "LED"], "RUSSIE": ["SVO", "LED"], "ROSSIA": ["SVO", "LED"], "РОССИЯ": ["SVO", "LED"]
}

# 3. INTERNATIONALE ÜBERSETZUNGEN
TRANSLATIONS = {
    "DE": {
        "title": "SWISS Inspired Search", "subtitle": "Automatisierte Flugsuche",
        "from": "Abflughafen / Land (oder leer lassen)", "to": "Zielflughafen / Land (oder leer lassen)",
        "max_price": "Maximaler Preis", "class": "Reiseklasse",
        "search_btn": "Flüge suchen", "results_title": "Beste Optionen für Sie:",
        "no_flights": "Keine Flüge für diese Kriterien gefunden.",
        "placeholder_from": "z.B. Zürich, Schweiz oder 'any'", "placeholder_to": "z.B. Spanien oder 'any'",
        "time_pref": "Gewünschte Uhrzeit (Optional)", "placeholder_time": "z.B. 15:30 oder 15"
    },
    "EN": {
        "title": "SWISS Inspired Search", "subtitle": "Automated Flight Search",
        "from": "Departure Airport / Country (or leave empty)", "to": "Destination / Country (or leave empty)",
        "max_price": "Maximum Price", "class": "Travel Class",
        "search_btn": "Search Flights", "results_title": "Best options for you:",
        "no_flights": "No flights found for these criteria.",
        "placeholder_from": "e.g. Zurich, Switzerland or 'any'", "placeholder_to": "e.g. Spain or 'any'",
        "time_pref": "Preferred Time (Optional)", "placeholder_time": "e.g. 15:30 or 15"
    },
    "FR": {
        "title": "SWISS Inspired Search", "subtitle": "Recherche de vols automatisée",
        "from": "Aéroport de départ / Pays (ou laisser vide)", "to": "Destination / Pays (ou laisser vide)",
        "max_price": "Prix maximum", "class": "Classe de voyage",
        "search_btn": "Rechercher des vols", "results_title": "Meilleures options pour vous:",
        "no_flights": "Aucun vol trouvé pour ces critères.",
        "placeholder_from": "ex. Zurich, Suisse ou 'any'", "placeholder_to": "ex. Espagne ou 'any'",
        "time_pref": "Heure souhaitée (Optionnel)", "placeholder_time": "ex. 15:30 ou 15"
    },
    "IT": {
        "title": "SWISS Inspired Search", "subtitle": "Ricerca voli automatizzata",
        "from": "Aeroporto di partenza / Paese (o lascia vuoto)", "to": "Destinazione / Paese (o lascia vuoto)",
        "max_price": "Prezzo massimo", "class": "Classe di viaggio",
        "search_btn": "Cerca voli", "results_title": "Le migliori opzioni per te:",
        "no_flights": "Nessun volo trovato per questi criteri.",
        "placeholder_from": "es. Zurigo, Svizzera o 'any'", "placeholder_to": "es. Spagna o 'any'",
        "time_pref": "Orario preferito (Opzionale)", "placeholder_time": "es. 15:30 ou 15"
    },
    "RU": {
        "title": "SWISS Inspired Search", "subtitle": "Автоматический поиск рейсов",
        "from": "Аэропорт вылета / Страна (или оставить пустым)", "to": "Пункт назначения / Страна (или оставить пустым)",
        "max_price": "Максимальная цена", "class": "Класс обслуживания",
        "search_btn": "Найти рейсы", "results_title": "Лучшие варианты для вас:",
        "no_flights": "Рейсы по этим критериям не найдены.",
        "placeholder_from": "например, Цюрих, Швейцария или 'any'", "placeholder_to": "например, Испания oder 'any'",
        "time_pref": "Желаемое время (Опционально)", "placeholder_time": "например, 15:30 или 15"
    }
}

def get_possible_airports(input_string):
    if not input_string:
        return []
    clean_input = input_string.upper().strip()
    if clean_input in ["ANY", "ANYWHERE", "ALLE", "ALLES", "LEER", "EVERYWHERE", "ПОВСЮДУ", "ЛЮБОЙ", "-"]:
        return []
    if clean_input in COUNTRY_TO_AIRPORTS:
        return COUNTRY_TO_AIRPORTS[clean_input]
    if clean_input in AIRPORT_TRANSLATOR:
        return [AIRPORT_TRANSLATOR[clean_input]]
    return [clean_input]

def calculate_price(price_chf, target_currency):
    rate = CURRENCY_RATES.get(target_currency, 1.0)
    return round(price_chf * rate, 2)

def is_time_matching(flight_time, target_time):
    if not target_time or target_time.upper().strip() in ["ANY", "ANYWHERE", "EGAL", "ALLE", "-"]:
        return True
    target = target_time.strip()
    if ":" not in target and len(target) <= 2:
        return flight_time.startswith(target + ":")
    return target in flight_time

def search_best_flights(origin, destination, max_price, travel_class, currency, preferred_time="any"):
    allowed_origins = get_possible_airports(origin)
    allowed_destinations = get_possible_airports(destination)
    
    rate = CURRENCY_RATES.get(currency, 1.0)
    
    if max_price is None or max_price <= 0:
        max_price_chf = 999999.0
    else:
        max_price_chf = max_price / rate
    
    results = []
    
    # 1. Durchlauf: Richtungs-Match
    for flight in FLIGHT_DATABASE:
        match_origin = not allowed_origins or (flight["von"] in allowed_origins)
        match_dest = not allowed_destinations or (flight["nach"] in allowed_destinations)
        match_time = is_time_matching(flight["zeit"], preferred_time)
        
        if match_origin and match_dest and match_time:
            price_chf = flight["preis_biz"] if travel_class == "BIZ" else flight["preis_eco"]
            if price_chf <= max_price_chf:
                results.append({
                    "von": flight["von"],
                    "nach": flight["nach"],
                    "zeit": flight["zeit"],
                    "preis": calculate_price(price_chf, currency),
                    "airline": flight["airline"]
                })
                
    # 2. Durchlauf: Gegenrichtung
    if not results and allowed_origins and allowed_destinations:
        for flight in FLIGHT_DATABASE:
            match_origin_rev = flight["von"] in allowed_destinations
            match_dest_rev = flight["nach"] in allowed_origins
            match_time = is_time_matching(flight["zeit"], preferred_time)
            
            if match_origin_rev and match_dest_rev and match_time:
                price_chf = flight["preis_biz"] if travel_class == "BIZ" else flight["preis_eco"]
                if price_chf <= max_price_chf:
                    results.append({
                        "von": flight["von"],
                        "nach": flight["nach"],
                        "zeit": flight["zeit"],
                        "preis": calculate_price(price_chf, currency),
                        "airline": flight["airline"] + " (Rückflug)"
                    })

    results.sort(key=lambda x: x["preis"])
    return results[:5]