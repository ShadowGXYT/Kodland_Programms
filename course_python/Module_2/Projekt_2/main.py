# Импорт
from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Secret Key für Session
app.secret_key = 'my_top_secret_123'

# SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ==============================
# USER MODELL
# ==============================
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.id}>'


# ==============================
# CARD MODELL
# ==============================
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    # Besitzer
    user_email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'


# ==============================
# LOGIN
# ==============================
@app.route('/', methods=['GET','POST'])
def login():
    error = ""

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session['user_email'] = email
            return redirect('/index')
        else:
            error = "Login falsch"

    return render_template('login.html', error=error)


# ==============================
# REGISTRATION
# ==============================
@app.route('/reg', methods=['GET','POST'])
def reg():

    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        new_user = User(email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/')

    return render_template('registration.html')

# ==============================
# LOGOUT
# ==============================
@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect('/')

# ==============================
# DELETE ACCOUNT
# ==============================
@app.route('/delete_account')
def delete_account():
    email = session.get('user_email')
    user = User.query.filter_by(email=email).first()

    if user:
        Card.query.filter_by(user_email=email).delete()
        db.session.delete(user)
        db.session.commit()

    session.clear()
    return redirect('/')

# ==============================
# INDEX (NUR EIGENE CARDS)
# ==============================
@app.route('/index')
def index():

    if 'user_email' not in session:
        return redirect('/')

    cards = Card.query.filter_by(user_email=session['user_email']).order_by(Card.id).all()

    return render_template('index.html', cards=cards)


# ==============================
# DETAIL SEITE
# ==============================
@app.route('/card/<int:id>')
def card_detail(id):
    card = Card.query.get_or_404(id)
    return render_template('card.html', card=card)


# ==============================
# CREATE PAGE
# ==============================
@app.route('/create')
def create():

    if 'user_email' not in session:
        return redirect('/')

    return render_template('create_card.html')


# ==============================
# CREATE FORM
# ==============================
@app.route('/form_create', methods=['POST'])
def form_create():

    title = request.form['title']
    subtitle = request.form['subtitle']
    text = request.form['text']

    new_card = Card(
        title=title,
        subtitle=subtitle,
        text=text,
        user_email=session['user_email']
    )

    db.session.add(new_card)
    db.session.commit()

    return redirect('/index')


# ==============================
# EDIT
# ==============================
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_card(id):
    card = Card.query.get_or_404(id)

    if request.method == 'POST':
        card.title = request.form['title']
        card.subtitle = request.form['subtitle']
        card.text = request.form['text']

        db.session.commit()
        return redirect(url_for('card_detail', id=card.id))

    return render_template('edit_card.html', card=card)


# ==============================
# DELETE
# ==============================
@app.route('/delete/<int:id>')
def delete_card(id):
    card = Card.query.get_or_404(id)

    db.session.delete(card)
    db.session.commit()

    return redirect('/index')


# ==============================
# START
# ==============================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)