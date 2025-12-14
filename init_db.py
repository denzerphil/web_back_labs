#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных.
Запустите этот скрипт один раз для создания таблиц.
"""

import sqlite3
import os

def init_sqlite_db():
    """Инициализация базы данных SQLite"""
    db_path = "database.db"
    
    # Удаляем существующую БД (если нужно)
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Удалена существующая база данных: {db_path}")
    
    # Создаём новую БД
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Создаём таблицу пользователей
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login VARCHAR(30) UNIQUE NOT NULL,
            password VARCHAR(162) NOT NULL,
            name VARCHAR(100)
        )
    """)
    
    # Создаём таблицу статей
    cur.execute("""
        CREATE TABLE articles (
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
    
    conn.commit()
    conn.close()
    
    print(f"База данных создана: {db_path}")
    print("Добавлены тестовые пользователи:")
    for login, _, name in test_users:
        print(f"  - {name} (логин: {login})")

if __name__ == "__main__":
    init_sqlite_db()
    print("\nБаза данных готова к использованию!")