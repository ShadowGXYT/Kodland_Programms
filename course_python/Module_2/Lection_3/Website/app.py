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


from PIL import Image, ImageDraw, ImageFont
import os, uuid
from flask import request, render_template

@app.route('/meme', methods=['GET','POST'])
def meme():
    folder='static/meme_img'
    os.makedirs(folder,exist_ok=True)
    images=[f for f in os.listdir(folder) if f.lower().endswith(('png','jpg','jpeg')) and not f.startswith('result_')]

    result=None

    if request.method=='POST':
        file=request.files.get('upload')
        image_name=request.form.get('image')

        if file and file.filename:
            path=os.path.join(folder,str(uuid.uuid4())+"_"+file.filename)
            file.save(path)
        else:
            path=os.path.join(folder,image_name)

        img=Image.open(path)
        draw=ImageDraw.Draw(img)
        font=ImageFont.load_default()

        def outline(x,y,text):
            for dx in [-2,-1,1,2]:
                for dy in [-2,-1,1,2]:
                    draw.text((x+dx,y+dy),text,font=font,fill='black')
            draw.text((x,y),text,font=font,fill='white')

        outline(10,10,request.form.get('top',''))
        outline(10,img.height-25,request.form.get('bottom',''))

        name='result_'+str(uuid.uuid4())+'.png'
        save=os.path.join(folder,name)
        img.save(save)
        result='meme_img/'+name

    gallery=[f for f in os.listdir(folder) if f.startswith('result_')]
    return render_template('meme.html',images=images,result=result,gallery=gallery)

