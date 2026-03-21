#Импорт
from flask import Flask, render_template,request, redirect



app = Flask(__name__)

#Запуск страницы с контентом
@app.route('/')
def index():
    return render_template('index.html')

import smtplib

@app.route('/', methods=['POST'])
def send_mail():
    email = request.form['email']
    text = request.form['text']

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("alhswiss@gmail.com", "DEIN_APP_PASSWORT")

    message = f"From: {email}\n\n{text}"
    server.sendmail(email, "alhswiss@gmail.com", message)

    server.quit()
    return redirect('/')

#Динамичные скиллы
@app.route('/', methods=['POST'])
def process_form():
    button_python = request.form.get('button_python')
    return render_template('index.html', button_python=button_python)


if __name__ == "__main__":
    app.run(debug=True)