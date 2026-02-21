from flask import Flask, render_template, request
import random

app = Flask(__name__)

# -----------------------
# Zufällige Fakten
# -----------------------
facts = [
    "Honig verdirbt nie.",
    "Oktopusse haben drei Herzen.",
    "Die Banane ist eine Beere.",
    "Ein Tag auf der Venus ist länger als ein Jahr."
]

# -----------------------
# Energieeffizienz-Rechner (Mehrstufig)
# -----------------------
size_map = {'small': 50, 'medium': 100, 'large': 200}

def result_calculate(size, lights, device):
    home_coef = 100
    light_coef = 0.04
    devices_coef = 5
    return size * home_coef + lights * light_coef + device * devices_coef


# -----------------------
# Hauptseiten
# -----------------------
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


# -----------------------
# Mehrstufiger Rechner
# -----------------------
@app.route('/<size>/lights')
def lights(size):
    return render_template('lights.html', size=size)

@app.route('/<size>/electronics/<lampen>')
def electronics(size, lampen):
    return render_template('electronics.html', size=size, lampen=lampen)

@app.route('/<size>/result/<lampen>/<geraete>')
def result(size, lampen, geraete):
    effizienz = int(size_map.get(size, 50)) + int(lampen) * 10 + int(geraete) * 15
    return render_template('energieeffizienz.html', effizienz=effizienz)


# -----------------------
# Einfacher Rechner (Formular)
# -----------------------
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    result = None

    if request.method == 'POST':
        persons = int(request.form.get('persons'))
        devices = int(request.form.get('devices'))
        result = persons * devices * 10

    return render_template('calculator.html', result=result)


# -----------------------
# NEU: Energieeffizienz Formular
# -----------------------
@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    address = request.form['address']
    date = request.form['date']

    return render_template(
        'form_result.html',
        name=name,
        email=email,
        address=address,
        date=date
    )


if __name__ == '__main__':
    app.run(debug=True)
