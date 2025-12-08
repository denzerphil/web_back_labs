from flask import Blueprint, render_template, redirect, request
import datetime

lab2 = Blueprint('lab2', __name__)

@lab2.route('/lab2/example')
def example():
    name, lab_num, group, course = 'Филиппов Денис', 2, 'ФБИ-33', 3
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('lab2/example.html',
                         name=name, lab_num=lab_num, group=group,
                         course=course, fruits=fruits)

@lab2.route('/lab2/')
def lab():
    return render_template('lab2/lab2.html')

@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('lab2/filter.html', phrase=phrase)

@lab2.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@lab2.route('/lab2/calc/<int:a>')
def calc_one(a):
    return redirect(f'/lab2/calc/{a}/1')

@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    return f'''
    <!DOCTYPE html>
    <html>
    <body>
        <h1>Расчёт с параметрами:</h1>
        <p>{a} + {b} = {a + b}</p>
        <p>{a} - {b} = {a - b}</p>
        <p>{a} × {b} = {a * b}</p>
        <p>{a} / {b} = {a / b}</p>
        <p>{a}<sup>{b}</sup> = {a ** b}</p>
    </body>
    </html>
    '''

books = [
    {'author': 'Толстой', 'title': 'Война и мир', 'genre': 'Роман', 'pages': 1225},
    {'author': 'Достоевский', 'title': 'Преступление и наказание', 'genre': 'Роман', 'pages': 671},
    {'author': 'Булгаков', 'title': 'Мастер и Маргарита', 'genre': 'Роман', 'pages': 480},
    {'author': 'Оруэлл', 'title': '1984', 'genre': 'Антиутопия', 'pages': 328},
    {'author': 'Гоголь', 'title': 'Мёртвые души', 'genre': 'Поэма', 'pages': 352},
    {'author': 'Стругацкие', 'title': 'Пикник на обочине', 'genre': 'Фантастика', 'pages': 240},
    {'author': 'Пушкин', 'title': 'Евгений Онегин', 'genre': 'Роман в стихах', 'pages': 288},
    {'author': 'Хемингуэй', 'title': 'Старик и море', 'genre': 'Повесть', 'pages': 110},
    {'author': 'Толкин', 'title': 'Властелин Колец', 'genre': 'Фэнтези', 'pages': 1200},
    {'author': 'Чехов', 'title': 'Рассказы', 'genre': 'Классика', 'pages': 400}
]

@lab2.route('/lab2/books')
def show_books():
    return render_template('lab2/books.html', books=books)

berries = [
    {
        'id': 1,
        'name': 'Клубника',
        'description': 'Сладкая и ароматная ягода, богатая витамином C',
        'image': 'Клубника.webp',
        'season': 'май-июнь'
    },
    # ... остальные ягоды
]

@lab2.route('/lab2/berries')
def show_berries():
    return render_template('lab2/berries.html', berries=berries)

flowers_with_prices = [
    {'name': 'роза', 'price': 300},
    {'name': 'тюльпан', 'price': 310},
    {'name': 'незабудка', 'price': 320},
    {'name': 'ромашка', 'price': 330},
    {'name': 'георгин', 'price': 300},
    {'name': 'гладиолус', 'price': 310}
]

@lab2.route('/lab2/flowers/')
def all_flowers():
    return render_template('lab2/flowers.html', flowers=flowers_with_prices)

@lab2.route('/lab2/add_flower/', methods=['GET', 'POST'])
def add_flower_form():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        if name and price:
            flowers_with_prices.append({'name': name, 'price': int(price)})
            return redirect('/lab2/flowers/')
        else:
            return "Не указано имя или цена цветка", 400
    return render_template('lab2/add_flower.html')

@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    if flower_id >= len(flowers_with_prices) or flower_id < 0:
        abort(404)
    flowers_with_prices.pop(flower_id)
    return redirect('/lab2/flowers/')

@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flowers_with_prices.clear()
    return redirect('/lab2/flowers/')