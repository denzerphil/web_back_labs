from flask import Blueprint, render_template, request, redirect, flash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def index():
    return render_template('lab8/index.html', current_user=current_user)

# Регистрация
@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()
    
    # Проверка на пустые значения
    if not login_form:
        return render_template('lab8/register.html', error='Логин не может быть пустым')
    
    if not password_form:
        return render_template('lab8/register.html', error='Пароль не может быть пустым')
    
    # Проверка существования пользователя
    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html', error='Такой пользователь уже существует')
    
    # Создание нового пользователя
    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    
    db.session.add(new_user)
    db.session.commit()
    
    # Автоматический логин после регистрации
    login_user(new_user, remember=False)
    
    return redirect('/lab8/')

# Авторизация
@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()
    remember_me = request.form.get('remember', False)
    
    # Проверка на пустые значения
    if not login_form:
        return render_template('lab8/login.html', error='Введите логин')
    
    if not password_form:
        return render_template('lab8/login.html', error='Введите пароль')
    
    # Поиск пользователя
    user = users.query.filter_by(login=login_form).first()
    
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me)
        return redirect('/lab8/')
    
    return render_template('lab8/login.html', error='Ошибка входа: логин и/или пароль неверны')

# Выход из системы
@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

# Список статей (только для авторизованных)
@lab8.route('/lab8/articles/')
@login_required
def article_list():
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    public_articles = articles.query.filter_by(is_public=True).all()
    return render_template('lab8/articles.html', 
                         user_articles=user_articles,
                         public_articles=public_articles,
                         current_user=current_user)

# Создание статьи
@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create_article.html')
    
    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title:
        return render_template('lab8/create_article.html', error='Название статьи не может быть пустым')
    
    if not article_text:
        return render_template('lab8/create_article.html', error='Текст статьи не может быть пустым')
    
    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        is_public=is_public,
        likes=0
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles/')

# Редактирование статьи
@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    # Проверка прав доступа
    if article.login_id != current_user.id:
        return redirect('/lab8/articles/')
    
    if request.method == 'GET':
        return render_template('lab8/edit_article.html', article=article)
    
    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title:
        return render_template('lab8/edit_article.html', article=article, error='Название статьи не может быть пустым')
    
    if not article_text:
        return render_template('lab8/edit_article.html', article=article, error='')
                               
    article.title = title
    article.article_text = article_text
    article.is_favorite = is_favorite
    article.is_public = is_public
    
    db.session.commit()
    
    return redirect('/lab8/articles/')

# Удаление статьи
@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)
    
    # Проверка прав доступа
    if article.login_id != current_user.id:
        return redirect('/lab8/articles/')
    
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles/')

# Поиск статей (дополнительное задание)
@lab8.route('/lab8/search', methods=['GET', 'POST'])
def search_articles():
    if request.method == 'GET':
        return render_template('lab8/search.html')
    
    search_text = request.form.get('search_text', '').strip()
    
    if not search_text:
        return render_template('lab8/search.html', error='Введите текст для поиска')
    
    # Поиск с использованием ilike для регистронезависимого поиска
    search_pattern = f'%{search_text}%'
    
    # Поиск в своих статьях (если авторизован)
    user_articles = []
    public_articles = []
    
    if current_user.is_authenticated:
        user_articles = articles.query.filter(
            articles.login_id == current_user.id,
            db.or_(
                articles.title.ilike(search_pattern),
                articles.article_text.ilike(search_pattern)
            )
        ).all()
    
    # Поиск в публичных статьях
    public_articles = articles.query.filter(
        articles.is_public == True,
        db.or_(
            articles.title.ilike(search_pattern),
            articles.article_text.ilike(search_pattern)
        )
    ).all()
    
    return render_template('lab8/search_results.html',
                         search_text=search_text,
                         user_articles=user_articles,
                         public_articles=public_articles,
                         current_user=current_user)