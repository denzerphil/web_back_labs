from flask import Blueprint, render_template, request, session, jsonify
import random

lab6 = Blueprint('lab6', __name__)

# Глобальная переменная для хранения офисов
# Храним офисы в формате: {"number": номер, "tenant": арендатор, "price": стоимость}
offices = []
for i in range(1, 11):
    # Генерируем случайную стоимость от 500 до 1500 с шагом 100
    price = random.choice([500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500])
    offices.append({"number": i, "tenant": "", "price": price})

@lab6.route('/lab6/')
def main():
    user_login = session.get('login')
    user_name = session.get('name', user_login)
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
    
    # Обработка метода info - получение информации о всех офисах
    if method == 'info':
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': request_id
        }
    
    # Обработка метода booking - бронирование офиса
    elif method == 'booking':
        # Проверка авторизации
        if not login:
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
        
        # Ищем офис
        for office in offices:
            if office['number'] == office_number:
                # Проверяем, свободен ли офис
                if office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Office already rented'
                        },
                        'id': request_id
                    }
                
                # Бронируем офис
                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': request_id
                }
        
        # Если офис не найден
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': request_id
        }
    
    # Обработка метода cancellation - снятие брони
    elif method == 'cancellation':
        # Проверка авторизации
        if not login:
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
        
        # Ищем офис
        for office in offices:
            if office['number'] == office_number:
                # Проверяем, арендован ли офис
                if not office['tenant']:
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
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 5,
                            'message': 'You are not the tenant of this office'
                        },
                        'id': request_id
                    }
                
                # Снимаем бронь
                office['tenant'] = ""
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': request_id
                }
        
        # Если офис не найден
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 3,
                'message': 'Office not found'
            },
            'id': request_id
        }
    
    # Если метод не найден
    else:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': -32601,
                'message': 'Method not found'
            },
            'id': request_id
        }