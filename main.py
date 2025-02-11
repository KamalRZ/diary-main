# Импорт
from flask import Flask, render_template, request, redirect
import datetime as dt
# Подключение библиотеки баз данных
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Подключение SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Создание db
db = SQLAlchemy(app)
# Создание таблицы
db.Model()


class Card(db.Model):
    # Создание полей
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Заголовок
    title = db.Column(db.String(100), nullable=False)
    # Описание
    subtitle = db.Column(db.String(300), nullable=False)
    # Текст
    text = db.Column(db.Text, nullable=False)
    user = db.Column(db.String(100))

    # Вывод объекта и id
    def __repr__(self):
        return f'<Card {self.id}>'


# Задание №1. Создать таблицу User

class User(db.Model):
    # Создание полей
    # id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=True)


# Запуск страницы с контентом
@app.route('/', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']

    # Задание №4. Реализовать проверку пользователей
        users_db = User.query.all()
        for user in users_db:
            if form_login == user.login and form_password == user.password:

                return redirect(f'/index/{form_login}/{form_password}')
        else:
            error = 'Неправильно указан пользователь или пароль'
            print(request.form)
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        login = request.form['email']
        password = request.form['password']

        # Задание №3. Реализовать запись пользователей
        user = User(login=login, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(f'/index/{login}/{password}')

    else:
        return render_template('registration.html')


# Запуск страницы с контентом
@app.route('/index/<login>/<password>')
def index(login, password):
    # Отображение объектов из БД
    cards = Card.query.order_by(Card.id).filter_by(user=login)
    return render_template('index.html',
                           cards=cards,
                           login=login,
                           password=password)


# Запуск страницы c картой
@app.route('/card/<int:id>/<login>/<password>')
def card(id, login, password):
    card = Card.query.get(id)

    return render_template('card.html',
                           card=card,
                           login=login,
                           password=password)


# Запуск страницы c созданием карты
@app.route('/create/<l>/<ps>')
def create(login, ps):
    with open("logs.txt", "w") as f:
        f.write(f"[{dt.time()}]")
    return render_template('create_card.html', login=login, password=ps)


# Форма карты
@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    print("password")
    for i in request.form.keys():

        if i.startswith("login="):
            login = i
            print(login)
        if i.startswith("password="):
            password = i
            print(password)
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']
        login = login.replace("login=", "")
        password = password.replace("password=", "")
        # Создание объкта для передачи в дб

        card = Card(title=title, subtitle=subtitle, text=text, user=login)

        db.session.add(card)
        db.session.commit()
        return redirect(f"index/{login}/{password}")
    else:
        return render_template('/create_card.html')


if __name__ == "__main__":
    app.run(debug=True)
