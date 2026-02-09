from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Zufällige Fakten
facts = [
    "Honig verdirbt nie.",
    "Oktopusse haben drei Herzen.",
    "Die Banane ist eine Beere.",
    "Ein Tag auf der Venus ist länger als ein Jahr."
]

# Mapping für Hausgröße (Rechner-Beispiel)
size_map = {'small': 50, 'medium': 100, 'large': 200}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/secret')
def secret():
    ergebnis = random.choice(["🪙 Kopf", "🪙 Zahl"])
    return render_template('secret.html', ergebnis=ergebnis)

@app.route('/random_fact')
def random_fact():
    fact = random.choice(facts)
    return render_template('random_fact.html', fact=fact)

# Energieeffizienz-Rechner – Schritt 1: Hausgröße
@app.route('/<size>/lights')
def lights(size):
    return render_template('lights.html', size=size)

# Schritt 2: Lampen
@app.route('/<size>/electronics/<lampen>')
def electronics(size, lampen):
    return render_template('electronics.html', size=size, lampen=lampen)

# Schritt 3: Ergebnis
@app.route('/<size>/result/<lampen>/<geraete>')
def result(size, lampen, geraete):
    effizienz = int(size_map.get(size, 50)) + int(lampen) * 10 + int(geraete) * 15
    return render_template('energieeffizienz.html', effizienz=effizienz)

if __name__ == '__main__':
    app.run(debug=True)
