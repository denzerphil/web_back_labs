from flask import Flask, url_for, request, redirect, abort, render_template, session
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from db import db
from flask_login import LoginManager
from db.models import users

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный-секрет')
app.config['DB_TYPE'] = os.environ.get('DB_TYPE', 'sqlite')

# Настройка соединения с БД
if app.config['DB_TYPE'] == 'postgres':
    db_name = 'ivan_ivanov_orm'
    db_user = 'ivan_ivanov_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "ivan_ivanov_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация БД
db.init_app(app)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

# Импортируем blueprint'ы после создания app
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8

# Регистрируем blueprint'ы
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)

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
                <li><a href="/lab2/">Вторая лабораторная</a></li>
                <li><a href="/lab3/">Третья лабораторная</a></li>
                <li><a href="/lab4/">Четвёртая лабораторная</a></li>
                <li><a href="/lab5/">Пятая лабораторная</a></li>
                <li><a href="/lab6/">Шестая лабораторная</a></li>
                <li><a href="/lab7/">Седьмая лабораторная</a></li>
                <li><a href="/lab8/">Восьмая лабораторная</a></li>
            </ul>
        </nav>
       
        <footer>
            <hr>
            <p>Филиппов Денис Максимович, ФБИ-33, 3 курс, 2024</p>
        </footer>
    </body>
</html>
'''

# ... остальной код без изменений (обработчики ошибок и т.д.)
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
    image_url = url_for('static', filename='lab1/404.webp')
    return f'''
<!doctype html>
<html>
    <head>
        <title>404 - Страница не найдена</title>
        <style>
            body {{
                background-color: #ffe6e6;
                font-family: Arial, sans-serif;
                text-align: center;
                padding: 50px;
                color: #333;
            }}
            .error-code {{
                font-size: 72px;
                color: #cc0000;
                margin-bottom: 20px;
            }}
            .message {{
                font-size: 24px;
                margin: 20px 0;
                color: #666;
            }}
            .error-image {{
                max-width: 400px;
                width: 100%;
                height: auto;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
                margin: 20px 0;
            }}
            .home-link {{
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #cc0000;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background-color 0.3s;
            }}
            .home-link:hover {{
                background-color: #a30000;
            }}
        </style>
    </head>
    <body>
        <div class="error-code">404</div>
        <div class="message">Упс! Страница не найдена</div>
        <img src="{image_url}" alt="Ошибка 404 - Страница не найдена" class="error-image">
        <p>Запрашиваемая страница не существует. Проверьте URL или вернитесь на главную страницу.</p>
        <a href="/" class="home-link">Вернуться на главную страницу</a>
    </body>
</html>
''', 404

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)