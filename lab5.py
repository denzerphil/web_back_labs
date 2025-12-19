from flask import Blueprint, render_template, request, session, redirect, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

# Функция для подключения к БД
def db_connect():
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            conn = psycopg2.connect(
                host='127.0.0.1',
                database='denis_filippov_knowledge_base',
                user='denis_filippov_knowledge_base',
                password='123'
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
        else:
            dir_path = path.dirname(path.realpath(__file__))
            db_path = path.join(dir_path, "database.db")
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        raise
# Ф
# Функция для закрытия соединения с БД
def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# Главная страница лабораторной
@lab5.route('/lab5/')
def lab():
    user_login = session.get('login')
    user_name = session.get('name', user_login)
    return render_template('lab5/lab5.html', 
                         login=user_login,
                         name=user_name)

# Регистрация
@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    # Получаем параметр next
    next_page = request.args.get('next', '/lab5')
    
    if request.method == 'GET':
        return render_template('lab5/register.html', next=next_page)
    
    login = request.form.get('login', '').strip()
    password = request.form.get('password', '')
    name = request.form.get('name', '').strip()
    
    # Валидация
    if not login or not password:
        return render_template('lab5/register.html',
                             error='Заполните все поля',
                             login=login,
                             name=name,
                             next=next_page)
    
    # Подключаемся к БД
    conn, cur = db_connect()
    
    # Проверяем, существует ли пользователь
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))
    
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                             error='Такой пользователь уже существует',
                             login=login,
                             name=name,
                             next=next_page)
    
    # Хешируем пароль
    password_hash = generate_password_hash(password)
    
    # Добавляем пользователя в БД
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password, name) VALUES (%s, %s, %s)",
                   (login, password_hash, name))
    else:
        cur.execute("INSERT INTO users (login, password, name) VALUES (?, ?, ?)",
                   (login, password_hash, name))
    
    db_close(conn, cur)
    
    # Автоматически входим после регистрации
    session['login'] = login
    session['name'] = name if name else login
    
    # Получаем ID пользователя
    conn, cur = db_connect()
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    user = cur.fetchone()
    if user:
        session['user_id'] = user[0] if isinstance(user, tuple) else user['id']
    db_close(conn, cur)
    
    # Редирект на страницу, указанную в next
    return redirect(next_page)

# Вход в систему
@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    # Получаем параметр next (куда вернуться после авторизации)
    next_page = request.args.get('next', '/lab5')
    
    if request.method == 'GET':
        return render_template('lab5/login.html', next=next_page)
    
    login_user = request.form.get('login', '').strip()
    password = request.form.get('password', '')
    
    if not login_user or not password:
        return render_template('lab5/login.html',
                             error='Заполните все поля',
                             login=login_user,
                             next=next_page)
    
    # Подключаемся к БД
    conn, cur = db_connect()
    
    # Ищем пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login_user,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login_user,))
    
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                             error='Логин и/или пароль неверны',
                             login=login_user,
                             next=next_page)
    
    # Проверяем пароль
    if isinstance(user, dict):
        # PostgreSQL
        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html',
                                 error='Логин и/или пароль неверны',
                                 login=login_user,
                                 next=next_page)
        
        # Сохраняем данные в сессии
        session['login'] = user['login']
        session['user_id'] = user['id']
        session['name'] = user.get('name', user['login'])
    else:
        # SQLite
        if not check_password_hash(user['password'], password):
            db_close(conn, cur)
            return render_template('lab5/login.html',
                                 error='Логин и/или пароль неверны',
                                 login=login_user,
                                 next=next_page)
        
        # Сохраняем данные в сессии
        session['login'] = user['login']
        session['user_id'] = user['id']
        session['name'] = user['name'] if user['name'] else user['login']
    
    db_close(conn, cur)
    # Редирект на страницу, указанную в next, или на /lab5 по умолчанию
    return redirect(next_page)

# Выход из системы
@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    session.pop('user_id', None)
    session.pop('name', None)
    return redirect('/lab5')

# Создание статьи
@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    # Проверка аутентификации
    if 'login' not in session:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    # Получаем данные из формы
    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    
    # Валидация
    if not title or not article_text:
        return render_template('lab5/create_article.html', 
                             error='Заполните все поля',
                             title=title,
                             article_text=article_text)
    
    # Подключаемся к БД
    conn, cur = db_connect()
    
    # Добавляем статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO articles (login_id, title, article_text, is_favorite, is_public, likes) 
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (session['user_id'], title, article_text, False, False, 0))
    else:
        cur.execute("""
            INSERT INTO articles (login_id, title, article_text, is_favorite, is_public, likes) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (session['user_id'], title, article_text, False, False, 0))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

# Список статей пользователя
@lab5.route('/lab5/list')
def list_articles():
    # Проверка аутентификации
    if 'login' not in session:
        return redirect('/lab5/login')
    
    # Подключаемся к БД
    conn, cur = db_connect()
    
    # Получаем статьи пользователя
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT * FROM articles 
            WHERE login_id=%s 
            ORDER BY is_favorite DESC, id DESC
        """, (session['user_id'],))
    else:
        cur.execute("""
            SELECT * FROM articles 
            WHERE login_id=? 
            ORDER BY is_favorite DESC, id DESC
        """, (session['user_id'],))
    
    articles = cur.fetchall()
    
    # Если articles - это список строк SQLite, преобразуем в список словарей
    if articles and not isinstance(articles[0], dict):
        articles_list = []
        for article in articles:
            articles_list.append({
                'id': article[0],
                'login_id': article[1],
                'title': article[2],
                'article_text': article[3],
                'is_favorite': bool(article[4]),
                'is_public': bool(article[5]),
                'likes': article[6]
            })
        articles = articles_list
    
    db_close(conn, cur)
    
    return render_template('lab5/articles.html', 
                         articles=articles,
                         name=session.get('name', session['login']))

# Редактирование статьи
@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    # Проверка аутентификации
    if 'login' not in session:
        return redirect('/lab5/login')
    
    # Подключаемся к БД
    conn, cur = db_connect()
    
    # Проверяем, принадлежит ли статья пользователю
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND login_id=%s", 
                   (article_id, session['user_id']))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND login_id=?", 
                   (article_id, session['user_id']))
    
    article = cur.fetchone()
    
    if not article:
        db_close(conn, cur)
        return redirect('/lab5/list')
    
    if request.method == 'GET':
        # Преобразуем в словарь для SQLite
        if not isinstance(article, dict):
            article_dict = {
                'id': article[0],
                'title': article[2],
                'article_text': article[3],
                'is_favorite': bool(article[4]),
                'is_public': bool(article[5])
            }
        else:
            article_dict = article
        
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article_dict)
    
    # Получаем данные из формы
    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    # Валидация
    if not title or not article_text:
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', 
                             article=article,
                             error='Заполните все поля')
    
    # Обновляем статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            UPDATE articles 
            SET title=%s, article_text=%s, is_favorite=%s, is_public=%s 
            WHERE id=%s AND login_id=%s
        """, (title, article_text, is_favorite, is_public, article_id, session['user_id']))
    else:
        cur.execute("""
            UPDATE articles 
            SET title=?, article_text=?, is_favorite=?, is_public=? 
            WHERE id=? AND login_id=?
        """, (title, article_text, is_favorite, is_public, article_id, session['user_id']))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

# Удаление статьи
@lab5.route('/lab5/delete/<int:article_id>')
def delete_article(article_id):
    # Проверка аутентификации
    if 'login' not in session:
        return redirect('/lab5/login')
    
    # Подключаемся к БД
    conn, cur = db_connect()
    
    # Удаляем статью
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s AND login_id=%s", 
                   (article_id, session['user_id']))
    else:
        cur.execute("DELETE FROM articles WHERE id=? AND login_id=?", 
                   (article_id, session['user_id']))
    
    db_close(conn, cur)
    return redirect('/lab5/list')

# Публичные статьи (для всех пользователей)
@lab5.route('/lab5/public')
def public_articles():
    # Подключаемся к БД
    conn, cur = db_connect()
    
    # Получаем публичные статьи
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            SELECT a.*, u.login as author 
            FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.is_public = TRUE 
            ORDER BY a.likes DESC, a.id DESC
        """)
    else:
        cur.execute("""
            SELECT a.*, u.login as author 
            FROM articles a 
            JOIN users u ON a.login_id = u.id 
            WHERE a.is_public = 1 
            ORDER BY a.likes DESC, a.id DESC
        """)
    
    articles = cur.fetchall()
    
    # Преобразуем SQLite строки в словари
    if articles and not isinstance(articles[0], dict):
        articles_list = []
        for article in articles:
            articles_list.append({
                'id': article[0],
                'login_id': article[1],
                'title': article[2],
                'article_text': article[3],
                'is_favorite': bool(article[4]),
                'is_public': bool(article[5]),
                'likes': article[6],
                'author': article[7]
            })
        articles = articles_list
    
    db_close(conn, cur)
    
    return render_template('lab5/public_articles.html', 
                         articles=articles,
                         is_authenticated='login' in session)

# Изменение настроек профиля
@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    # Проверка аутентификации
    if 'login' not in session:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/profile.html',
                             name=session.get('name', session['login']))
    
    # Получаем данные из формы
    name = request.form.get('name', '').strip()
    new_password = request.form.get('new_password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Подключаемся к БД
    conn, cur = db_connect()
    
    # Обновляем имя
    if name:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET name=%s WHERE id=%s", 
                       (name, session['user_id']))
        else:
            cur.execute("UPDATE users SET name=? WHERE id=?", 
                       (name, session['user_id']))
        session['name'] = name
    
    # Обновляем пароль, если он введён
    if new_password:
        if new_password != confirm_password:
            db_close(conn, cur)
            return render_template('lab5/profile.html',
                                 name=session.get('name', session['login']),
                                 error='Пароли не совпадают')
        
        password_hash = generate_password_hash(new_password)
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users SET password=%s WHERE id=%s", 
                       (password_hash, session['user_id']))
        else:
            cur.execute("UPDATE users SET password=? WHERE id=?", 
                       (password_hash, session['user_id']))
    
    db_close(conn, cur)
    
    if new_password or name:
        return render_template('lab5/profile.html',
                             name=session.get('name', session['login']),
                             success='Данные успешно обновлены')
    
    return render_template('lab5/profile.html',
                         name=session.get('name', session['login']))

# Список всех пользователей
@lab5.route('/lab5/users')
def all_users():
    # Проверка аутентификации
    if 'login' not in session:
        return redirect('/lab5/login')
    
    # Подключаемся к БД
    conn, cur = db_connect()
    
    # Получаем всех пользователей
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id, login, name FROM users ORDER BY login")
    else:
        cur.execute("SELECT id, login, name FROM users ORDER BY login")
    
    users = cur.fetchall()
    
    # Преобразуем SQLite строки в словари
    if users and not isinstance(users[0], dict):
        users_list = []
        for user in users:
            users_list.append({
                'id': user[0],
                'login': user[1],
                'name': user[2] if user[2] else user[1]
            })
        users = users_list
    
    db_close(conn, cur)
    
    return render_template('lab5/all_users.html', users=users)

# Лайк статьи
@lab5.route('/lab5/like/<int:article_id>')
def like_article(article_id):
    # Проверка аутентификации
    if 'login' not in session:
        return redirect('/lab5/login')
    
    # Подключаемся к БД
    conn, cur = db_connect()
    
    # Увеличиваем количество лайков
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET likes = likes + 1 WHERE id=%s", (article_id,))
    else:
        cur.execute("UPDATE articles SET likes = likes + 1 WHERE id=?", (article_id,))
    
    db_close(conn, cur)
    return redirect('/lab5/public')