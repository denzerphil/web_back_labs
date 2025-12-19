from flask import Blueprint, render_template, request, jsonify
from datetime import datetime

lab7 = Blueprint('lab7', __name__)

# Начальный список фильмов
films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину (которая предположительно соединяет области пространства-времени через большое расстояние) в путешествие, чтобы превзойти прежнее ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящим по обе стороны решётки. Каждый, кто попадает в эти стены, становится их рабом до конца жизни. Но Энди, обладающий живым умом и доброй душой, находит подход как к заключённым, так и к охранникам, добиваясь их особого к себе расположения."
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Пол Эджкомб — начальник блока смертников в тюрьме «Холодная гора». Каждый из узников которого однажды проходит зелёную милю по пути к месту казни. Пол повидал много заключённых и надзирателей за время работы. Однако гигант Джон Коффи, обвинённый в страшном преступлении, стал одним из самых необычных обитателей блока."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Сотрудник страховой компании страдает хронической бессонницей и отчаянно пытается вырваться из мучительно скучной жизни. Он посещает группы поддержки для людей с тяжёлыми заболеваниями, чтобы делиться своей болью с другими. Но всё меняется, когда на одном из таких собраний он встречает загадочного торговца мылом по имени Тайлер Дёрден."
    },
    {
        "title": "Léon",
        "title_ru": "Леон",
        "year": 1994,
        "description": "Профессиональный убийца Леон неожиданно для себя самого решает помочь 12-летней соседке Матильде, семью которой убили коррумпированные полицейские."
    }
]

def validate_film(film):
    """Валидация данных фильма"""
    errors = {}
    
    # Проверка русского названия
    title_ru = film.get('title_ru', '').strip()
    if not title_ru:
        errors['title_ru'] = 'Русское название обязательно'
    elif len(title_ru) > 200:
        errors['title_ru'] = 'Русское название слишком длинное (максимум 200 символов)'
    
    # Проверка оригинального названия
    title = film.get('title', '').strip()
    if not title and not title_ru:
        errors['title'] = 'Оригинальное название обязательно, если русское не задано'
    elif len(title) > 200:
        errors['title'] = 'Оригинальное название слишком длинное (максимум 200 символов)'
    
    # Проверка года
    year = film.get('year')
    current_year = datetime.now().year
    if not year:
        errors['year'] = 'Год обязателен'
    elif not isinstance(year, int):
        errors['year'] = 'Год должен быть числом'
    elif year < 1895 or year > current_year:
        errors['year'] = f'Год должен быть между 1895 и {current_year}'
    
    # Проверка описания
    description = film.get('description', '').strip()
    if not description:
        errors['description'] = 'Описание обязательно'
    elif len(description) > 2000:
        errors['description'] = 'Описание слишком длинное (максимум 2000 символов)'
    
    return errors

@lab7.route('/lab7/')
def main():
    """Главная страница лабораторной работы 7"""
    return render_template('lab7/index.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    """Получение списка всех фильмов"""
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    """Получение информации о конкретном фильме"""
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    """Удаление фильма"""
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    """Редактирование существующего фильма"""
    if id < 0 or id >= len(films):
        return jsonify({"error": "Film not found"}), 404
    
    film = request.get_json()
    
    # Если оригинальное название пустое, а русское задано - копируем русское
    if film.get('title', '').strip() == '' and film.get('title_ru', '').strip() != '':
        film['title'] = film['title_ru']
    
    # Валидация
    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    films[id] = film
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    """Добавление нового фильма"""
    film = request.get_json()
    
    # Если оригинальное название пустое, а русское задано - копируем русское
    if film.get('title', '').strip() == '' and film.get('title_ru', '').strip() != '':
        film['title'] = film['title_ru']
    
    # Валидация
    errors = validate_film(film)
    if errors:
        return jsonify(errors), 400
    
    films.append(film)
    return jsonify({"id": len(films) - 1})