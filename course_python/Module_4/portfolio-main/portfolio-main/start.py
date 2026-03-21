from flask import Flask, render_template, request, redirect
import smtplib

app = Flask(__name__)

# About-Me Texte in allen Sprachen
about_texts = {
    'en': "Im a student from Switzerland. I enjoy playing tennis in my free time and Im very interested in technology and programming. I regularly take programming courses at Kodland, where I improve my skills in web development, Python, and building projects like bots and websites.",
    'de': "Ich bin ein Schüler aus der Schweiz. In meiner Freizeit spiele ich gerne Tennis und interessiere mich sehr für Technologie und Programmierung. Ich nehme regelmäßig an Programmierkursen bei Kodland teil, wo ich meine Fähigkeiten in Webentwicklung, Python und beim Erstellen von Projekten wie Bots und Websites verbessere.",
    'ru': "Я ученик из Швейцарии. В свободное время я люблю играть в теннис и очень интересуюсь технологиями и программированием. Я регулярно прохожу курсы программирования в Kodland, где улучшаю свои навыки веб-разработки, Python и создания проектов, таких как боты и сайты."
}

@app.route('/', methods=['GET', 'POST'])
def index():
    button_python = None
    if request.method == 'POST':
        # Feedback-Formular senden
        if 'email' in request.form and 'text' in request.form:
            email = request.form['email']
            text = request.form['text']

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("alhswiss@gmail.com", "DEIN_APP_PASSWORT")  # Dein App-Passwort

            message = f"From: {email}\n\n{text}"
            server.sendmail("alhswiss@gmail.com", "alhswiss@gmail.com", message)
            server.quit()

        # Skill-Buttons
        button_python = request.form.get('button_python')

    # Standard About-Text in Englisch
    about_text = about_texts['en']

    return render_template('index.html', 
                           button_python=button_python, 
                           about_texts=about_texts,
                           about_text=about_text)

if __name__ == "__main__":
    app.run(debug=True)