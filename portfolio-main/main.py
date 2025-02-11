# Импорт
from flask import Flask, render_template, request, redirect


def fw():
    email = request.form['email']
    text = request.form['text']
    with open("fb.txt", "a") as f:
        f.write("ertyjk")
        f.write(f'{len(email)}:{email}:\n{text}')
        f.close()


app = Flask(__name__)


# Запуск страницы с контентом
@app.route('/')
def index():
    return render_template('index.html')


# Динамичные скиллы
@app.route('/', methods=['POST'])
def process_form():
    button_python = request.form.get('button_python')
    return render_template('index.html', button_python=button_python)


@app.route('/', methods=['POST'])
def fb():
    fw()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
