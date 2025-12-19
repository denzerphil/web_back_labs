#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных.
Запустите этот скрипт один раз для создания таблиц.
"""
import sqlite3
import os
import random

def init_sqlite_db():
    """Инициализация базы данных SQLite"""
    db_path = "database.db"
   
    # Проверяем существование БД
    db_exists = os.path.exists(db_path)
    
    # Подключаемся к БД
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Создаём таблицу пользователей (если не существует)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login VARCHAR(30) UNIQUE NOT NULL,
            password VARCHAR(162) NOT NULL,
            name VARCHAR(100)
        )
    """)
   
    # Создаём таблицу статей (если не существует)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login_id INTEGER NOT NULL,
            title VARCHAR(50),
            article_text TEXT,
            is_favorite BOOLEAN,
            is_public BOOLEAN,
            likes INTEGER,
            FOREIGN KEY (login_id) REFERENCES users (id)
        )
    """)
    
    # Создаём таблицу офисов для лабораторной работы 6 (если не существует)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS offices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER UNIQUE NOT NULL,
            tenant VARCHAR(100),
            price INTEGER NOT NULL
        )
    """)
    
    # Проверяем, нужно ли добавлять тестовые данные
    cur.execute("SELECT COUNT(*) FROM offices")
    office_count = cur.fetchone()[0]
    
    if office_count == 0:
        # Добавляем 10 офисов
        for i in range(1, 11):
            # Генерируем случайную стоимость от 500 до 1500 с шагом 100
            price = random.choice([500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500])
            cur.execute("""
                INSERT INTO offices (number, tenant, price)
                VALUES (?, ?, ?)
            """, (i, "", price))
        print("Добавлено 10 офисов в таблицу offices")
    
    # Проверяем, нужно ли добавлять тестовых пользователей
    cur.execute("SELECT COUNT(*) FROM users")
    user_count = cur.fetchone()[0]
    
    if user_count == 0:
        # Добавляем тестовых пользователей
        from werkzeug.security import generate_password_hash
        
        test_users = [
            ("alex", "123", "Алексей Петров"),
            ("bob", "555", "Борис Сидоров"),
            ("anna", "777", "Анна Иванова"),
            ("maria", "888", "Мария Смирнова"),
        ]
        
        for login, password, name in test_users:
            password_hash = generate_password_hash(password)
            cur.execute("INSERT INTO users (login, password, name) VALUES (?, ?, ?)",
                       (login, password_hash, name))
        print(f"Добавлены тестовые пользователи: {len(test_users)}")
    
    conn.commit()
    conn.close()
    
    if not db_exists:
        print(f"Создана новая база данных: {db_path}")
    else:
        print(f"Обновлена существующая база данных: {db_path}")
    print("\nБаза данных готова к использованию!")

if __name__ == "__main__":
    init_sqlite_db()