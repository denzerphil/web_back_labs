from flask import Flask, url_for, request, redirect, abort
import datetime

app = Flask(__name__)


@app.route("/lab1/web")
def web():
    return """<!doctype html> \
        <html> \
            <body> \
               <h1>web-сервер на flask</h1> \
               <a href="/lab1/author">author</a> \
               <a href="/lab1/info">info</a> \
               <a href="/lab1/counter">counter</a> \
               <a href="/lab1/image">image</a> \
            </body> \
        </html>"""

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")  

@app.route("/lab1/author")
def author():
    name = "Филиппов Денис Максимович"
    group = "ФБИ-33"
    faculty = "Бизнес-информатика"
    return f"""<!doctype html>
        <html>
            <body>
                <p>Студент: {name}</p>
                <p>Группа: {group}</p>
                <p>Факультет: {faculty}</p>
                <a href="/lab1/web">web</a>
                <a href="/lab1/info">info</a>
            </body>
        </html>"""


@app.route('/lab1/image')
def image():
    css_url = url_for('static', filename='lab1.css')
    image_url = url_for('static', filename='oak.jpg')
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_url}">
    </head>
    <body>
        <div class="container">
            <h1>Дуб</h1>
            <img src="{image_url}" alt="Дуб">
            <p><a href="/lab1/web">Назад к меню</a></p>
        </div>
    </body>
</html>
'''


count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    url = request.url
    client_ip = request.remote_addr
    return f'''
<!doctype html>
<html>
    <body>
        <h2>Счетчик посещений</h2>
        <p>Сколько раз вы сюда заходили: {count}</p>
        <hr>
        <p>Дата и время: {time}</p>
        <p>Запрошенный адрес: {url}</p>
        <p>Ваш IP-адрес: {client_ip}</p>
        <a href="/lab1/clear_counter">Очистить счетчик</a><br>
        <a href="/lab1/web">Назад к меню</a>
    </body>
</html>
'''

@app.route('/lab1/clear_counter')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')


@app.route("/")
@app.route("/index")
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <nav>
            <ul>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ul>
        </nav>
        
        <footer>
            <hr>
            <p>Филиппов Денис Максимович, ФБИ-33, 3 курс, 2024</p>
        </footer>
    </body>
</html>
'''


@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная работа 1</h1>
        
        <p>
        Flask — фреймворк для создания веб-приложений на языке
        программирования Python, использующий набор инструментов
        Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
        называемых микрофреймворков — минималистичных каркасов
        веб-приложений, сознательно предоставляющих лишь самые ба-
        зовые возможности.
        </p>
        
        <a href="/">На главную страницу</a>
        
        <!-- ЗАДАНИЕ 10: Список роутов -->
        <h2>Список роутов</h2>
        <ul>
            <li><a href="/lab1/web">Web-сервер</a></li>
            <li><a href="/lab1/author">Автор</a></li>
            <li><a href="/lab1/info">Информация (редирект)</a></li>
            <li><a href="/lab1/image">Изображение</a></li>
            <li><a href="/lab1/counter">Счетчик</a></li>
        </ul>
    </body>
</html>
'''


@app.route('/400')
def bad_request():
    abort(400)

@app.route('/401')
def unauthorized():
    abort(401)

@app.route('/402')
def payment_required():
    abort(402)

@app.route('/403')
def forbidden():
    abort(403)

@app.route('/405')
def method_not_allowed():
    abort(405)

@app.route('/418')
def teapot():
    abort(418)


@app.errorhandler(404)
def not_found_error(error):
    return '''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <style>
            body {
                background-color: #ffe6e6;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            .error-code {
                font-size: 72px;
                color: #cc0000;
            }
            .message {
                font-size: 24px;
                margin: 20px 0;
            }
            img {
                max-width: 300px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="error-code">404</div>
        <div class="message">Упс! Страница не найдена</div>
        <img src="https://via.placeholder.com/300x200/cc0000/ffffff?text=404+Error" alt="Ошибка 404">
        <p>Запрашиваемая страница не существует. Проверьте URL или вернитесь на <a href="/">главную страницу</a>.</p>
    </body>
</html>
''', 404


@app.route('/error500')
def error500():
    # Вызываем ошибку деления на ноль
    x = 1 / 0
    return "Этот код никогда не выполнится"

@app.errorhandler(500)
def internal_error(error):
    return '''
<!doctype html>
<html>
    <head>
        <title>500 - Внутренняя ошибка сервера</title>
        <style>
            body {
                background-color: #fff0f0;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
            }
            .error-code {
                font-size: 72px;
                color: #ff0000;
            }
        </style>
    </head>
    <body>
        <div class="error-code">500</div>
        <h1>Внутренняя ошибка сервера</h1>
        <p>На сервере произошла непредвиденная ошибка. Пожалуйста, попробуйте позже.</p>
        <p><a href="/">Вернуться на главную страницу</a></p>
    </body>
</html>
''', 500

@app.route('/lab1/image_with_headers')
def image_with_headers():
    response = app.make_response(redirect(url_for('image')))
    response.headers['Content-Language'] = 'ru'
    response.headers['X-Developer'] = 'Филиппов Денис'
    response.headers['X-Lab-Work'] = 'Лабораторная 1'
    return response

if __name__ == '__main__':
    app.run(debug=False)  