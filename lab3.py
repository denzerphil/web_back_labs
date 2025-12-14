from flask import Blueprint, render_template, request, make_response, redirect, url_for

lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    
    return render_template('lab3/lab3.html', 
                         name=name, 
                         name_color=name_color,
                         age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    age = request.args.get('age')
    sex = request.args.get('sex')
   
    # Валидация
    if user == '':
        errors['user'] = 'Заполните поле!'
    if age == '':
        errors['age'] = 'Заполните поле!'
   
    return render_template('lab3/form1.html',
                         user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
   
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    
    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)

@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    
    if color:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('color', color)
        return resp
   
    color = request.cookies.get('color')
    return render_template('lab3/settings.html', color=color)

@lab3.route('/lab3/del_settings')
def del_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    return resp

@lab3.route('/lab3/ticket')
def ticket():
    return render_template('lab3/ticket_form.html')

@lab3.route('/lab3/ticket_result')
def ticket_result():
    errors = {}
    
    # Получаем данные
    fio = request.args.get('fio')
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    luggage = request.args.get('luggage')
    age = request.args.get('age')
    from_city = request.args.get('from_city')
    to_city = request.args.get('to_city')
    date = request.args.get('date')
    insurance = request.args.get('insurance')
    
    # Валидация
    if not fio or fio.strip() == '':
        errors['fio'] = 'Заполните поле ФИО'
    if not age:
        errors['age'] = 'Заполните поле возраст'
    elif int(age) < 1 or int(age) > 120:
        errors['age'] = 'Возраст должен быть от 1 до 120 лет'
    if not from_city or from_city.strip() == '':
        errors['from_city'] = 'Заполните пункт выезда'
    if not to_city or to_city.strip() == '':
        errors['to_city'] = 'Заполните пункт назначения'
    if not date:
        errors['date'] = 'Выберите дату'
    
    # Если есть ошибки, показываем форму снова
    if errors:
        return render_template('lab3/ticket_form.html',
                             errors=errors,
                             fio=fio, shelf=shelf, linen=linen,
                             luggage=luggage, age=age,
                             from_city=from_city, to_city=to_city,
                             date=date, insurance=insurance)
    
    # Расчет цены
    price = 1000 if int(age) >= 18 else 700  # взрослый/детский
    
    if shelf in ['lower', 'lower-side']:
        price += 100
    
    if linen == 'on':
        price += 75
    
    if luggage == 'on':
        price += 250
    
    if insurance == 'on':
        price += 150
    
    return render_template('lab3/ticket_result.html',
                         fio=fio, shelf=shelf, linen=linen,
                         luggage=luggage, age=age,
                         from_city=from_city, to_city=to_city,
                         date=date, insurance=insurance,
                         price=price)

# Дополнительное задание: Поиск товаров по диапазону цен

# Список товаров (20+ позиций)
products = [
    {'name': 'iPhone 15', 'price': 89990, 'brand': 'Apple', 'color': 'черный'},
    {'name': 'Samsung Galaxy S24', 'price': 79990, 'brand': 'Samsung', 'color': 'белый'},
    {'name': 'Xiaomi Redmi Note 13', 'price': 24990, 'brand': 'Xiaomi', 'color': 'синий'},
    {'name': 'Google Pixel 8', 'price': 69990, 'brand': 'Google', 'color': 'серый'},
    {'name': 'OnePlus 11', 'price': 54990, 'brand': 'OnePlus', 'color': 'зеленый'},
    {'name': 'Huawei P60', 'price': 65990, 'brand': 'Huawei', 'color': 'золотой'},
    {'name': 'Realme GT 3', 'price': 39990, 'brand': 'Realme', 'color': 'оранжевый'},
    {'name': 'Nokia G42', 'price': 18990, 'brand': 'Nokia', 'color': 'фиолетовый'},
    {'name': 'Motorola Edge 40', 'price': 42990, 'brand': 'Motorola', 'color': 'черный'},
    {'name': 'Sony Xperia 5 V', 'price': 89990, 'brand': 'Sony', 'color': 'синий'},
    {'name': 'Asus Zenfone 10', 'price': 59990, 'brand': 'Asus', 'color': 'красный'},
    {'name': 'Honor 90', 'price': 34990, 'brand': 'Honor', 'color': 'серебристый'},
    {'name': 'Vivo V29', 'price': 45990, 'brand': 'Vivo', 'color': 'розовый'},
    {'name': 'Oppo Reno 10', 'price': 37990, 'brand': 'Oppo', 'color': 'голубой'},
    {'name': 'Poco X5 Pro', 'price': 27990, 'brand': 'Poco', 'color': 'желтый'},
    {'name': 'Infinix Zero 30', 'price': 22990, 'brand': 'Infinix', 'color': 'черный'},
    {'name': 'Tecno Phantom V', 'price': 31990, 'brand': 'Tecno', 'color': 'белый'},
    {'name': 'ZTE Nubia Z50', 'price': 49990, 'brand': 'ZTE', 'color': 'красный'},
    {'name': 'Apple iPhone 14', 'price': 74990, 'brand': 'Apple', 'color': 'фиолетовый'},
    {'name': 'Samsung Galaxy A54', 'price': 32990, 'brand': 'Samsung', 'color': 'зеленый'},
    {'name': 'Google Pixel 7a', 'price': 44990, 'brand': 'Google', 'color': 'коралловый'},
    {'name': 'Nothing Phone 2', 'price': 46990, 'brand': 'Nothing', 'color': 'белый'},
]

@lab3.route('/lab3/products')
def products_search():
    # Получаем параметры из GET-запроса или куки
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    # Если параметры не пришли, пробуем взять из куки
    if not min_price and not max_price:
        min_price = request.cookies.get('min_price')
        max_price = request.cookies.get('max_price')
    
    # Конвертируем в числа, если это возможно
    min_price_int = None
    max_price_int = None
    
    try:
        if min_price:
            min_price_int = int(min_price)
    except:
        min_price_int = None
    
    try:
        if max_price:
            max_price_int = int(max_price)
    except:
        max_price_int = None
    
    # Находим минимальную и максимальную цены среди всех товаров
    all_prices = [p['price'] for p in products]
    global_min_price = min(all_prices)
    global_max_price = max(all_prices)
    
    # Фильтрация товаров
    filtered_products = []
    
    for product in products:
        price = product['price']
        
        # Проверяем, попадает ли цена в диапазон
        price_ok = True
        
        if min_price_int is not None and price < min_price_int:
            price_ok = False
        
        if max_price_int is not None and price > max_price_int:
            price_ok = False
        
        if price_ok:
            filtered_products.append(product)
    
    # Если пользователь перепутал min и max, меняем их местами
    if min_price_int is not None and max_price_int is not None and min_price_int > max_price_int:
        min_price_int, max_price_int = max_price_int, min_price_int
        # Перефильтруем с правильными значениями
        filtered_products = []
        for product in products:
            price = product['price']
            if min_price_int <= price <= max_price_int:
                filtered_products.append(product)
    
    # Создаем ответ
    resp = make_response(render_template('lab3/products.html',
                                       products=filtered_products,
                                       min_price=min_price,
                                       max_price=max_price,
                                       global_min_price=global_min_price,
                                       global_max_price=global_max_price,
                                       count=len(filtered_products)))
    
    # Сохраняем значения в куки
    if min_price or max_price:
        if min_price:
            resp.set_cookie('min_price', min_price, max_age=30*24*60*60)  # 30 дней
        if max_price:
            resp.set_cookie('max_price', max_price, max_age=30*24*60*60)  # 30 дней
    
    return resp

@lab3.route('/lab3/products_reset')
def products_reset():
    # Сбрасываем фильтры и куки
    resp = make_response(redirect('/lab3/products'))
    resp.delete_cookie('min_price')
    resp.delete_cookie('max_price')
    return resp