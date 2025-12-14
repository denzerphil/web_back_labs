from flask import Blueprint, render_template, request, redirect, session
import math

lab4 = Blueprint('lab4', __name__)

# Глобальная переменная для счётчика деревьев
tree_count = 0

# Список пользователей (логин, пароль, имя)
users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей Петров', 'gender': 'мужской'},
    {'login': 'bob', 'password': '555', 'name': 'Борис Сидоров', 'gender': 'мужской'},
    {'login': 'anna', 'password': '777', 'name': 'Анна Иванова', 'gender': 'женский'},
    {'login': 'maria', 'password': '888', 'name': 'Мария Смирнова', 'gender': 'женский'}
]

# Главная страница лабораторной
@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

# --- Задание 6: Деление чисел (POST) ---
@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены')
    
    try:
        x1_num = int(x1)
        x2_num = int(x2)
    except ValueError:
        return render_template('lab4/div.html', error='Введите целые числа')
    
    if x2_num == 0:
        return render_template('lab4/div.html', error='Деление на ноль невозможно')
    
    result = x1_num / x2_num
    return render_template('lab4/div.html', x1=x1_num, x2=x2_num, result=result)

# --- Задание 7: Арифметика ---
@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1', '0')
    x2 = request.form.get('x2', '0')
    
    try:
        x1_num = int(x1) if x1 != '' else 0
        x2_num = int(x2) if x2 != '' else 0
    except ValueError:
        return render_template('lab4/sum.html', error='Введите целые числа')
    
    result = x1_num + x2_num
    return render_template('lab4/sum.html', x1=x1_num, x2=x2_num, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1', '1')
    x2 = request.form.get('x2', '1')
    
    try:
        x1_num = int(x1) if x1 != '' else 1
        x2_num = int(x2) if x2 != '' else 1
    except ValueError:
        return render_template('lab4/mul.html', error='Введите целые числа')
    
    result = x1_num * x2_num
    return render_template('lab4/mul.html', x1=x1_num, x2=x2_num, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены')
    
    try:
        x1_num = int(x1)
        x2_num = int(x2)
    except ValueError:
        return render_template('lab4/sub.html', error='Введите целые числа')
    
    result = x1_num - x2_num
    return render_template('lab4/sub.html', x1=x1_num, x2=x2_num, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены')
    
    try:
        x1_num = int(x1)
        x2_num = int(x2)
    except ValueError:
        return render_template('lab4/pow.html', error='Введите целые числа')
    
    if x1_num == 0 and x2_num == 0:
        return render_template('lab4/pow.html', error='Недопустимая операция: 0^0')
    
    result = x1_num ** x2_num
    return render_template('lab4/pow.html', x1=x1_num, x2=x2_num, result=result)

# --- Задание 8: POST/Redirect/GET (Счётчик деревьев) ---
@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    # Если метод POST
    operation = request.form.get('operation')
    
    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:  # Максимум 10 деревьев
        tree_count += 1
    
    return redirect('/lab4/tree')

# --- Задание 9-11: Авторизация с сессиями ---
@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    # Если пользователь уже авторизован
    if 'login' in session:
        user_login = session['login']
        # Находим пользователя в списке
        user = next((u for u in users if u['login'] == user_login), None)
        if user:
            return render_template('lab4/login.html', 
                                 authorized=True, 
                                 login=user['login'],
                                 name=user['name'])
    
    # Если метод GET - просто показываем форму
    if request.method == 'GET':
        return render_template('lab4/login.html', 
                             authorized=False, 
                             login='', 
                             error='',
                             prev_login='')
    
    # Если метод POST - обрабатываем авторизацию
    user_login = request.form.get('login', '')
    password = request.form.get('password', '')
    
    # Проверка на пустые поля
    if not user_login:
        return render_template('lab4/login.html',
                             authorized=False,
                             login='',
                             error='Не введён логин',
                             prev_login='')
    
    if not password:
        return render_template('lab4/login.html',
                             authorized=False,
                             login='',
                             error='Не введён пароль',
                             prev_login=user_login)
    
    # Проверяем пользователя в списке
    for user in users:
        if user['login'] == user_login and user['password'] == password:
            # Сохраняем в сессию
            session['login'] = user_login
            return redirect('/lab4/login')
    
    # Если не нашли пользователя
    return render_template('lab4/login.html',
                         authorized=False,
                         login='',
                         error='Неверные логин и/или пароль',
                         prev_login=user_login)

# Выход из системы
@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

# --- Самостоятельное задание 2: Холодильник ---
@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html', 
                             temp=None, 
                             message='', 
                             snowflakes=0,
                             error='')
    
    temp_str = request.form.get('temp', '')
    
    if not temp_str:
        return render_template('lab4/fridge.html',
                             temp=None,
                             message='',
                             snowflakes=0,
                             error='Ошибка: не задана температура')
    
    try:
        temp = int(temp_str)
    except ValueError:
        return render_template('lab4/fridge.html',
                             temp=None,
                             message='',
                             snowflakes=0,
                             error='Ошибка: введите целое число')
    
    if temp < -12:
        return render_template('lab4/fridge.html',
                             temp=temp,
                             message='',
                             snowflakes=0,
                             error='Не удалось установить температуру — слишком низкое значение')
    
    if temp > -1:
        return render_template('lab4/fridge.html',
                             temp=temp,
                             message='',
                             snowflakes=0,
                             error='Не удалось установить температуру — слишком высокое значение')
    
    # Определяем количество снежинок
    if -12 <= temp <= -9:
        snowflakes = 3
        message = f'Установлена температура: {temp}°C'
    elif -8 <= temp <= -5:
        snowflakes = 2
        message = f'Установлена температура: {temp}°C'
    elif -4 <= temp <= -1:
        snowflakes = 1
        message = f'Установлена температура: {temp}°C'
    else:
        snowflakes = 0
        message = ''
    
    return render_template('lab4/fridge.html',
                         temp=temp,
                         message=message,
                         snowflakes=snowflakes,
                         error='')

# --- Самостоятельное задание 3: Заказ зерна ---
@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        return render_template('lab4/grain.html',
                             grain_type='',
                             weight='',
                             total=0,
                             discount=0,
                             message='',
                             error='')
    
    grain_type = request.form.get('grain_type', '')
    weight_str = request.form.get('weight', '')
    
    # Цены за тонну
    prices = {
        'barley': 12000,   # ячмень
        'oats': 8500,      # овёс
        'wheat': 9000,     # пшеница
        'rye': 15000       # рожь
    }
    
    # Названия зерна
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс',
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    # Проверка выбора зерна
    if not grain_type:
        return render_template('lab4/grain.html',
                             grain_type='',
                             weight=weight_str,
                             total=0,
                             discount=0,
                             message='',
                             error='Выберите тип зерна')
    
    # Проверка веса
    if not weight_str:
        return render_template('lab4/grain.html',
                             grain_type=grain_type,
                             weight='',
                             total=0,
                             discount=0,
                             message='',
                             error='Укажите вес')
    
    try:
        weight = float(weight_str)
    except ValueError:
        return render_template('lab4/grain.html',
                             grain_type=grain_type,
                             weight=weight_str,
                             total=0,
                             discount=0,
                             message='',
                             error='Введите число для веса')
    
    if weight <= 0:
        return render_template('lab4/grain.html',
                             grain_type=grain_type,
                             weight=weight_str,
                             total=0,
                             discount=0,
                             message='',
                             error='Вес должен быть положительным числом')
    
    if weight > 100:
        return render_template('lab4/grain.html',
                             grain_type=grain_type,
                             weight=weight,
                             total=0,
                             discount=0,
                             message='',
                             error='Извините, такого объёма нет в наличии (максимум 100 тонн)')
    
    # Расчёт суммы
    price_per_ton = prices[grain_type]
    total = weight * price_per_ton
    discount = 0
    
    # Применение скидки
    if weight > 10:
        discount = total * 0.1
        total -= discount
    
    grain_name = grain_names[grain_type]
    discount_text = f' (скидка 10% за большой объём: {discount:.0f} руб.)' if discount > 0 else ''
    
    message = f'Заказ успешно сформирован. Вы заказали {grain_name}. Вес: {weight} т. Сумма к оплате: {total:.0f} руб.{discount_text}'
    
    return render_template('lab4/grain.html',
                         grain_type=grain_type,
                         weight=weight,
                         total=total,
                         discount=discount,
                         message=message,
                         error='')

# --- Дополнительное задание: Регистрация и управление пользователями ---
@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html',
                             error='',
                             success='',
                             login='',
                             name='',
                             gender='')
    
    # Получаем данные из формы
    login = request.form.get('login', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    name = request.form.get('name', '').strip()
    gender = request.form.get('gender', '')
    
    # Валидация
    if not login:
        return render_template('lab4/register.html',
                             error='Введите логин',
                             success='',
                             login=login,
                             name=name,
                             gender=gender)
    
    if not password:
        return render_template('lab4/register.html',
                             error='Введите пароль',
                             success='',
                             login=login,
                             name=name,
                             gender=gender)
    
    if password != confirm_password:
        return render_template('lab4/register.html',
                             error='Пароли не совпадают',
                             success='',
                             login=login,
                             name=name,
                             gender=gender)
    
    if not name:
        return render_template('lab4/register.html',
                             error='Введите имя',
                             success='',
                             login=login,
                             name=name,
                             gender=gender)
    
    # Проверяем, не занят ли логин
    for user in users:
        if user['login'] == login:
            return render_template('lab4/register.html',
                                 error='Этот логин уже занят',
                                 success='',
                                 login='',
                                 name=name,
                                 gender=gender)
    
    # Добавляем нового пользователя
    new_user = {
        'login': login,
        'password': password,
        'name': name,
        'gender': gender
    }
    users.append(new_user)
    
    return render_template('lab4/register.html',
                         error='',
                         success='Регистрация успешна! Теперь вы можете войти в систему.',
                         login='',
                         name='',
                         gender='')

# Список пользователей (только для авторизованных)
@lab4.route('/lab4/users')
def show_users():
    # Проверка авторизации
    if 'login' not in session:
        return redirect('/lab4/login')
    
    return render_template('lab4/users.html',
                         users=users,
                         current_user=session['login'])

# Удаление своего профиля
@lab4.route('/lab4/delete_user', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_login = session['login']
    
    # Находим и удаляем пользователя
    for i, user in enumerate(users):
        if user['login'] == current_login:
            users.pop(i)
            session.pop('login', None)
            return redirect('/lab4/login')
    
    return redirect('/lab4/users')

# Редактирование профиля
@lab4.route('/lab4/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    # Проверка авторизации
    if 'login' not in session:
        return redirect('/lab4/login')
    
    current_login = session['login']
    
    # Находим текущего пользователя
    current_user = None
    for user in users:
        if user['login'] == current_login:
            current_user = user
            break
    
    if not current_user:
        session.pop('login', None)
        return redirect('/lab4/login')
    
    if request.method == 'GET':
        return render_template('lab4/edit_profile.html',
                             user=current_user,
                             error='',
                             success='')
    
    # Если метод POST - обновляем данные
    new_login = request.form.get('login', '').strip()
    new_name = request.form.get('name', '').strip()
    new_gender = request.form.get('gender', '')
    new_password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    # Валидация
    if not new_login:
        return render_template('lab4/edit_profile.html',
                             user=current_user,
                             error='Введите логин',
                             success='')
    
    if not new_name:
        return render_template('lab4/edit_profile.html',
                             user=current_user,
                             error='Введите имя',
                             success='')
    
    # Проверяем, не занят ли новый логин другим пользователем
    if new_login != current_login:
        for user in users:
            if user['login'] == new_login:
                return render_template('lab4/edit_profile.html',
                                     user=current_user,
                                     error='Этот логин уже занят',
                                     success='')
    
    # Если введён новый пароль
    if new_password:
        if new_password != confirm_password:
            return render_template('lab4/edit_profile.html',
                                 user=current_user,
                                 error='Пароли не совпадают',
                                 success='')
        current_user['password'] = new_password
    
    # Обновляем данные пользователя
    current_user['login'] = new_login
    current_user['name'] = new_name
    current_user['gender'] = new_gender
    
    # Обновляем логин в сессии, если он изменился
    session['login'] = new_login
    
    return render_template('lab4/edit_profile.html',
                         user=current_user,
                         error='',
                         success='Данные успешно обновлены!')