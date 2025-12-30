from flask import Blueprint, render_template, request, jsonify, session
import random
import json
from datetime import datetime
from db import db
from db.models import users
from flask_login import login_required, current_user

lab9 = Blueprint('lab9', __name__)

# Данные для подарков
gifts_data = {
    'gifts': [
        {
            'id': 1,
            'name': 'Книга мудрости',
            'message': 'Пусть новый год принесёт тебе новые знания и мудрость!',
            'image': 'gift_book.png',
            'type': 'common',
            'requires_auth': False
        },
        {
            'id': 2,
            'name': 'Сердце дружбы',
            'message': 'Пусть в новом году у тебя будет много верных друзей!',
            'image': 'gift_heart.png',
            'type': 'common',
            'requires_auth': False
        },
        {
            'id': 3,
            'name': 'Ключ успеха',
            'message': 'Пусть в новом году все двери успеха будут открыты для тебя!',
            'image': 'gift_key.png',
            'type': 'common',
            'requires_auth': False
        },
        {
            'id': 4,
            'name': 'Звезда удачи',
            'message': 'Пусть удача всегда светит тебе яркой звездой!',
            'image': 'gift_star.png',
            'type': 'common',
            'requires_auth': False
        },
        {
            'id': 5,
            'name': 'Часы времени',
            'message': 'Цени каждый момент нового года - время бесценно!',
            'image': 'gift_clock.png',
            'type': 'common',
            'requires_auth': False
        },
        {
            'id': 6,
            'name': 'Глобус путешествий',
            'message': 'Пусть новый год откроет для тебя новые горизонты!',
            'image': 'gift_globe.png',
            'type': 'common',
            'requires_auth': False
        },
        {
            'id': 7,
            'name': 'Кубок побед',
            'message': 'Пусть в новом году все твои цели будут достигнуты!',
            'image': 'gift_cup.png',
            'type': 'special',
            'requires_auth': True
        },
        {
            'id': 8,
            'name': 'Корона лидера',
            'message': 'Пусть новый год сделает тебя лидером во всех начинаниях!',
            'image': 'gift_crown.png',
            'type': 'special',
            'requires_auth': True
        },
        {
            'id': 9,
            'name': 'Сундук сокровищ',
            'message': 'Пусть в новом году ты найдёшь свои самые большие сокровища!',
            'image': 'gift_chest.png',
            'type': 'special',
            'requires_auth': True
        },
        {
            'id': 10,
            'name': 'Волшебная палочка',
            'message': 'Пусть все твои мечты сбудутся в новом году!',
            'image': 'gift_magic.png',
            'type': 'special',
            'requires_auth': True
        }
    ]
}

def init_gift_session():
    """Инициализация данных о подарках в сессии"""
    if 'gifts' not in session:
        # Создаем позиции для 10 коробок
        gift_positions = []
        for i in range(10):
            # Генерируем случайные позиции
            gift_positions.append({
                'id': i + 1,
                'top': random.randint(10, 70),  # в процентах
                'left': random.randint(5, 85),   # в процентах
                'opened': False,
                'gift_id': i
            })
        
        # Сохраняем в сессии
        session['gifts'] = json.dumps(gift_positions)
        session['opened_count'] = 0
        session['initialized'] = True
    
    return json.loads(session['gifts'])

@lab9.route('/lab9/')
def main():
    """Главная страница лабораторной работы 9"""
    gift_positions = init_gift_session()
    opened_count = session.get('opened_count', 0)
    remaining_gifts = 10 - opened_count
    
    return render_template('lab9/index.html', 
                         gifts=gift_positions,
                         opened_count=opened_count,
                         remaining_gifts=remaining_gifts,
                         gifts_data=gifts_data,
                         current_user=current_user)

@lab9.route('/lab9/open_gift', methods=['POST'])
def open_gift():
    """Обработка открытия подарка (JSON API)"""
    try:
        data = request.get_json()
        gift_position_id = data.get('position_id')
        
        if not gift_position_id:
            return jsonify({'error': 'Не указан ID подарка'}), 400
        
        # Получаем текущее состояние подарков
        gift_positions = json.loads(session.get('gifts', '[]'))
        opened_count = session.get('opened_count', 0)
        
        # Проверяем, можно ли открывать еще подарки
        if opened_count >= 3:
            return jsonify({
                'error': True,
                'message': 'Вы уже открыли максимальное количество подарков (3)!'
            }), 400
        
        # Находим нужный подарок
        gift_to_open = None
        for gift in gift_positions:
            if gift['id'] == gift_position_id:
                gift_to_open = gift
                break
        
        if not gift_to_open:
            return jsonify({'error': 'Подарок не найден'}), 404
        
        # Проверяем, не открыт ли уже этот подарок
        if gift_to_open['opened']:
            return jsonify({
                'error': True,
                'message': 'Этот подарок уже открыт!'
            }), 400
        
        # Получаем информацию о подарке из данных
        gift_id = gift_to_open['gift_id']
        gift_info = gifts_data['gifts'][gift_id]
        
        # Проверяем, требует ли подарок авторизации
        if gift_info['requires_auth'] and not current_user.is_authenticated:
            return jsonify({
                'error': True,
                'message': 'Этот подарок доступен только для авторизованных пользователей!',
                'requires_login': True
            }), 403
        
        # Открываем подарок
        gift_to_open['opened'] = True
        
        # Обновляем счетчик открытых подарков
        opened_count += 1
        
        # Сохраняем изменения в сессии
        session['gifts'] = json.dumps(gift_positions)
        session['opened_count'] = opened_count
        
        # Возвращаем информацию о подарке
        return jsonify({
            'success': True,
            'gift': gift_info,
            'opened_count': opened_count,
            'remaining_gifts': 10 - opened_count
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@lab9.route('/lab9/reset_gifts', methods=['POST'])
@login_required
def reset_gifts():
    """Сброс всех подарков (только для авторизованных пользователей)"""
    # Очищаем данные о подарках в сессии
    session.pop('gifts', None)
    session.pop('opened_count', None)
    session.pop('initialized', None)
    
    return jsonify({
        'success': True,
        'message': 'Все подарки были восстановлены Дедом Морозом!'
    })

@lab9.route('/lab9/get_gifts_state')
def get_gifts_state():
    """Получение текущего состояния подарков"""
    gift_positions = json.loads(session.get('gifts', '[]'))
    opened_count = session.get('opened_count', 0)
    
    return jsonify({
        'gifts': gift_positions,
        'opened_count': opened_count,
        'remaining_gifts': 10 - opened_count,
        'is_authenticated': current_user.is_authenticated
    })

@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    """Специальный вход для лабораторной 9"""
    from flask_login import login_user
    from werkzeug.security import check_password_hash
    from db.models import users
    
    if request.method == 'GET':
        return render_template('lab9/login.html')
    
    login_form = request.form.get('login', '').strip()
    password_form = request.form.get('password', '').strip()
    remember_me = request.form.get('remember', False)
    
    if not login_form or not password_form:
        return render_template('lab9/login.html', 
                             error='Заполните все поля')
    
    # Ищем пользователя
    user = users.query.filter_by(login=login_form).first()
    
    if user and check_password_hash(user.password, password_form):
        login_user(user, remember=remember_me)
        return redirect('/lab9/')
    
    return render_template('lab9/login.html', 
                         error='Неверный логин или пароль')