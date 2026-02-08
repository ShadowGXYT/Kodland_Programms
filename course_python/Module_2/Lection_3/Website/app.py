from flask import Flask, render_template
import random

app = Flask(__name__)

facts = [
    "Honig verdirbt nie.",
    "Oktopusse haben drei Herzen.",
    "Die Banane ist eine Beere.",
    "Ein Tag auf der Venus ist länger als ein Jahr."
]

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

if __name__ == '__main__':
    app.run(debug=True)

