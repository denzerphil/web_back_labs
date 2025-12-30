#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных для лабораторной работы 8.
Создаёт файл den_filippov_orm.db и таблицы через SQLAlchemy.
"""
import os
from app import app
from db import db
from db.models import users, articles

def init_lab8_db():
    """Инициализация базы данных для 8-й лабораторной"""
    with app.app_context():
        # Создаём все таблицы
        db.create_all()
        
        # Проверяем, есть ли тестовые пользователи
        if users.query.count() == 0:
            # Добавляем тестовых пользователей
            from werkzeug.security import generate_password_hash
            
            test_users = [
                ("test", "test123", None),
                ("demo", "demo123", None),
                ("admin", "admin123", None),
            ]
            
            for login, password, name in test_users:
                password_hash = generate_password_hash(password)
                new_user = users(login=login, password=password_hash)
                db.session.add(new_user)
            
            db.session.commit()
            print(f"Добавлены тестовые пользователи: {len(test_users)}")
        
        print("База данных для лабораторной работы 8 готова!")
        print(f"Файл: den_filippov_orm.db")

if __name__ == "__main__":
    init_lab8_db()