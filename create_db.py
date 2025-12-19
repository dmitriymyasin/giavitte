#!/usr/bin/env python3
"""
Полное пересоздание базы данных с правильными паролями для SQLite
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
from datetime import datetime
import sqlite3

def recreate_database():
    print("=" * 60)
    print("Пересоздание базы данных 'Корочки.есть' (SQLite)")
    print("=" * 60)
    
    # Определяем путь к базе данных
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, 'vitte.db')
    
    print(f"📂 Путь к базе данных: {db_path}")
    
    try:
        # Удаляем старую базу данных если она существует
        if os.path.exists(db_path):
            os.remove(db_path)
            print("🗑️  Старая база данных удалена")
        
        # Создаем подключение к SQLite
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        print("\n1. Создание таблиц...")
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                login VARCHAR(50) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                full_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Индексы для users
        cursor.execute('CREATE INDEX idx_users_login ON users(login)')
        cursor.execute('CREATE INDEX idx_users_email ON users(email)')
        print("   ✅ Таблица 'users' создана")
        
        # Таблица курсов
        cursor.execute('''
            CREATE TABLE courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX idx_courses_name ON courses(name)')
        print("   ✅ Таблица 'courses' создана")
        
        # Таблица заявок
        cursor.execute('''
            CREATE TABLE applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                desired_start_date DATE NOT NULL,
                payment_method TEXT NOT NULL CHECK (payment_method IN ('cash', 'bank_transfer')),
                status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'completed')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        ''')
        
        # Индексы для applications
        cursor.execute('CREATE INDEX idx_applications_user_id ON applications(user_id)')
        cursor.execute('CREATE INDEX idx_applications_status ON applications(status)')
        cursor.execute('CREATE INDEX idx_applications_created_at ON applications(created_at)')
        print("   ✅ Таблица 'applications' создана")
        
        # Таблица отзывов
        cursor.execute('''
            CREATE TABLE reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                application_id INTEGER NOT NULL UNIQUE,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
            )
        ''')
        
        # Индексы для reviews
        cursor.execute('CREATE INDEX idx_reviews_rating ON reviews(rating)')
        cursor.execute('CREATE INDEX idx_reviews_created_at ON reviews(created_at)')
        print("   ✅ Таблица 'reviews' создана")
        
        # Таблица статистики отзывов
        cursor.execute('''
            CREATE TABLE review_stats (
                course_id INTEGER PRIMARY KEY,
                total_reviews INTEGER DEFAULT 0,
                average_rating REAL DEFAULT 0.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
            )
        ''')
        print("   ✅ Таблица 'review_stats' создана")
        
        # Таблица истории статусов
        cursor.execute('''
            CREATE TABLE application_status_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                application_id INTEGER NOT NULL,
                old_status TEXT CHECK (old_status IN ('new', 'in_progress', 'completed')),
                new_status TEXT NOT NULL CHECK (new_status IN ('new', 'in_progress', 'completed')),
                changed_by VARCHAR(50) DEFAULT 'Admin',
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE
            )
        ''')
        
        # Индексы для history
        cursor.execute('CREATE INDEX idx_history_application_id ON application_status_history(application_id)')
        cursor.execute('CREATE INDEX idx_history_changed_at ON application_status_history(changed_at)')
        print("   ✅ Таблица 'application_status_history' создана")
        
        # Генерация правильных хешей паролей
        print("\n2. Генерация паролей...")
        passwords = {
            'Admin': 'KorokNET',
            'user1': 'password123',
            'user2': 'password456',
            'user3': 'password789',
            'user4': 'password012',
            'user5': 'password345'
        }
        
        hashes = {}
        for user, password in passwords.items():
            hashed = generate_password_hash(password)
            hashes[user] = hashed
            print(f"   ✅ {user}: {password} -> хеш создан")
        
        # Заполняем данными
        print("\n3. Заполнение данными...")
        
        # Курсы с описаниями
        courses_data = [
            ('Основы алгоритмизации и программирования', 'Курс по основам алгоритмов и программирования на Python и C++. Изучаем базовые структуры данных, алгоритмы сортировки и поиска, принципы ООП. Подходит для начинающих программистов.'),
            ('Основы веб-дизайна', 'Курс по основам дизайна веб-приложений. Изучаем HTML, CSS, основы UX/UI, адаптивную верстку, работу с Figma и Adobe XD. Научитесь создавать современные интерфейсы.'),
            ('Основы проектирования баз данных', 'Курс по проектированию и разработке баз данных. Изучаем SQL, нормализацию, проектирование ER-диаграмм, оптимизацию запросов, работу с MySQL и PostgreSQL.'),
            ('Машинное обучение для начинающих', 'Введение в машинное обучение на Python. Изучаем библиотеки scikit-learn, pandas, основы нейронных сетей, работу с данными и построение моделей.'),
            ('Разработка мобильных приложений', 'Курс по разработке мобильных приложений на React Native. Создаем кроссплатформенные приложения для iOS и Android с нуля.')
        ]
        
        cursor.executemany('INSERT INTO courses (name, description) VALUES (?, ?)', courses_data)
        print("   ✅ Курсы добавлены")
        
        # Пользователи
        users_data = [
            ('Admin', hashes['Admin'], 'Администратор Системы', '8(999)123-45-67', 'admin@korokki-est.ru'),
            ('user1', hashes['user1'], 'Иванов Иван Иванович', '8(911)111-11-11', 'ivanov@example.com'),
            ('user2', hashes['user2'], 'Петров Петр Петрович', '8(922)222-22-22', 'petrov@example.com'),
            ('user3', hashes['user3'], 'Сидорова Анна Сергеевна', '8(933)333-33-33', 'sidorova@example.com'),
            ('user4', hashes['user4'], 'Кузнецова Мария Дмитриевна', '8(944)444-44-44', 'kuznetsova@example.com'),
            ('user5', hashes['user5'], 'Смирнов Алексей Владимирович', '8(955)555-55-55', 'smirnov@example.com')
        ]
        
        cursor.executemany('''
            INSERT INTO users (login, password_hash, full_name, phone, email) 
            VALUES (?, ?, ?, ?, ?)
        ''', users_data)
        print("   ✅ Пользователи добавлены")
        
        # Заявки
        print("\n4. Добавление заявок...")
        applications_data = [
            # user1
            (2, 1, '2024-09-01', 'cash', 'completed'),
            (2, 2, '2024-10-15', 'bank_transfer', 'completed'),
            (2, 3, '2024-11-01', 'cash', 'in_progress'),
            # user2
            (3, 1, '2024-09-10', 'bank_transfer', 'completed'),
            (3, 4, '2024-10-20', 'cash', 'completed'),
            (3, 5, '2024-12-01', 'bank_transfer', 'new'),
            # user3
            (4, 2, '2024-08-15', 'cash', 'completed'),
            (4, 3, '2024-09-20', 'bank_transfer', 'completed'),
            (4, 5, '2025-01-10', 'cash', 'in_progress'),
            # user4
            (5, 1, '2024-07-01', 'bank_transfer', 'completed'),
            (5, 4, '2024-08-10', 'cash', 'completed'),
            # user5
            (6, 2, '2024-09-05', 'cash', 'completed'),
            (6, 3, '2024-10-10', 'bank_transfer', 'completed')