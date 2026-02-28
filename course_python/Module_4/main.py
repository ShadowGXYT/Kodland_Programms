# Импорт
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ==============================
# Модель
# ==============================
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Card {self.id}>'


# ==============================
# Главная страница + поиск
# ==============================
@app.route('/')
def index():
    search_query = request.args.get('search')

    if search_query:
        cards = Card.query.filter(
            Card.title.contains(search_query) |
            Card.subtitle.contains(search_query)
        ).all()
    else:
        cards = Card.query.order_by(Card.id).all()

    return render_template('index.html', cards=cards)


# ==============================
# Детальная страница
# ==============================
@app.route('/card/<int:id>')
def card_detail(id):
    card = Card.query.get_or_404(id)
    return render_template('card.html', card=card)


# ==============================
# Создание карточки
# ==============================
@app.route('/create')
def create():
    return render_template('create_card.html')


@app.route('/form_create', methods=['POST'])
def form_create():
    title = request.form['title']
    subtitle = request.form['subtitle']
    text = request.form['text']

    new_card = Card(title=title, subtitle=subtitle, text=text)
    db.session.add(new_card)
    db.session.commit()

    return redirect('/')


# ==============================
# ✏ EDIT
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
# 🗑 DELETE
# ==============================
@app.route('/delete/<int:id>')
def delete_card(id):
    card = Card.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    return redirect('/')


# ==============================
# Запуск
# ==============================
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)