from flask import Blueprint, redirect, url_for, request
import datetime

lab1 = Blueprint('lab1', __name__)

count = 0

@lab1.route("/lab1")
def lab():
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

# Остальные роуты остаются без изменений
@lab1.route("/lab1/web")
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

@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")  

@lab1.route("/lab1/author")
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

@lab1.route('/lab1/image')
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

@lab1.route('/lab1/counter')
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

@lab1.route('/lab1/clear_counter')
def clear_counter():
    global count
    count = 0
    return redirect('/lab1/counter')