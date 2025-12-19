from flask import Blueprint, render_template, request, session
import sqlite3
import os

lab6 = Blueprint('lab6', __name__)

def get_db_connection():
    """Создает соединение с базой данных SQLite"""
    dir_path = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(dir_path, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Возвращает строки как словари
    return conn

def init_offices_if_needed():
    """Инициализирует офисы в БД если их нет"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Проверяем, есть ли офисы в БД
    cur.execute("SELECT COUNT(*) FROM offices")
    count = cur.fetchone()[0]
    
    if count == 0:
        import random
        # Добавляем 10 офисов
        for i in range(1, 11):
            price = random.choice([500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500])
            cur.execute("INSERT INTO offices (number, tenant, price) VALUES (?, ?, ?)",
                       (i, "", price))
        conn.commit()
        print("Инициализированы офисы в БД")
    
    conn.close()

@lab6.route('/lab6/')
def main():
    user_login = session.get('login')
    user_name = session.get('name', user_login)
    
    # Инициализируем офисы если нужно
    init_offices_if_needed()
    
    return render_template('lab6/lab6.html',
                         login=user_login,
                         name=user_name)

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    # Получаем данные из запроса
    data = request.json
    method = data.get('method')
    request_id = data.get('id')
    
    # Получаем логин пользователя из сессии
    login = session.get('login')
    
    # Подключаемся к БД
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Обработка метода info - получение информации о всех офисах
    if method == 'info':
        cur.execute("SELECT number, tenant, price FROM offices ORDER BY number")
        offices = []
        for row in cur.fetchall():
            offices.append({
                'number': row['number'],
                'tenant': row['tenant'] if row['tenant'] else "",
                'price': row['price']
            })
        
        conn.close()
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': request_id
        }
    
    # Обработка метода booking - бронирование офиса
    elif method == 'booking':
        # Проверка авторизации
        if not login:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': request_id
            }
        
        # Получаем номер офиса из параметров
        office_number = data.get('params')
        
        # Проверяем, существует ли офис
        cur.execute("SELECT tenant FROM offices WHERE number = ?", (office_number,))
        office = cur.fetchone()
        
        if not office:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office not found'
                },
                'id': request_id
            }
        
        # Проверяем, свободен ли офис
        if office['tenant']:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Office already rented'
                },
                'id': request_id
            }
        
        # Бронируем офис
        cur.execute("UPDATE offices SET tenant = ? WHERE number = ?", (login, office_number))
        conn.commit()
        conn.close()
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': request_id
        }
    
    # Обработка метода cancellation - снятие брони
    elif method == 'cancellation':
        # Проверка авторизации
        if not login:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 1,
                    'message': 'Unauthorized'
                },
                'id': request_id
            }
        
        # Получаем номер офиса из параметров
        office_number = data.get('params')
        
        # Проверяем, существует ли офис
        cur.execute("SELECT tenant FROM offices WHERE number = ?", (office_number,))
        office = cur.fetchone()
        
        if not office:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office not found'
                },
                'id': request_id
            }
        
        # Проверяем, арендован ли офис
        if not office['tenant']:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Office is not rented'
                },
                'id': request_id
            }
        
        # Проверяем, принадлежит ли аренда текущему пользователю
        if office['tenant'] != login:
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 5,
                    'message': 'You are not the tenant of this office'
                },
                'id': request_id
            }
        
        # Снимаем бронь
        cur.execute("UPDATE offices SET tenant = '' WHERE number = ?", (office_number,))
        conn.commit()
        conn.close()
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': request_id
        }
    
    # Если метод не найден
    else:
        conn.close()
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': request_id
        }