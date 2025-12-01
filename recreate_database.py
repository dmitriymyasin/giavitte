#!/usr/bin/env python3
"""
Полное пересоздание базы данных с правильными паролями
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
import pymysql

def recreate_database():
    print("=" * 60)
    print("Пересоздание базы данных 'Корочки.есть'")
    print("=" * 60)
    
    # Параметры подключения
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'HfgFGty217GF',
        'database': 'vitte'
    }
    
    try:
        # Подключаемся к MySQL
        connection = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # Удаляем и создаем базу данных
            print("1. Создание базы данных...")
            cursor.execute(f"DROP DATABASE IF EXISTS {config['database']}")
            cursor.execute(f"CREATE DATABASE {config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            cursor.execute(f"USE {config['database']}")
            print("   ✅ База данных создана")
            
            # Создаем таблицы
            print("\n2. Создание таблиц...")
            
            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE users (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    login VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100) NOT NULL,
                    phone VARCHAR(20) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    INDEX idx_login (login),
                    INDEX idx_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            print("   ✅ Таблица 'users' создана")
            
            # Таблица курсов
            cursor.execute('''
                CREATE TABLE courses (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    INDEX idx_name (name)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            print("   ✅ Таблица 'courses' создана")
            
            # Таблица заявок
            cursor.execute('''
                CREATE TABLE applications (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    course_id INT NOT NULL,
                    desired_start_date DATE NOT NULL,
                    payment_method ENUM('cash', 'bank_transfer') NOT NULL,
                    status ENUM('new', 'in_progress', 'completed') DEFAULT 'new',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
                    
                    INDEX idx_user_id (user_id),
                    INDEX idx_status (status),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            print("   ✅ Таблица 'applications' создана")
            
            # Таблица отзывов
            cursor.execute('''
                CREATE TABLE reviews (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    user_id INT NOT NULL,
                    application_id INT NOT NULL UNIQUE,
                    rating TINYINT NOT NULL,
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
                    
                    CONSTRAINT check_rating_range CHECK (rating BETWEEN 1 AND 5),
                    INDEX idx_rating (rating),
                    INDEX idx_created_at (created_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            print("   ✅ Таблица 'reviews' создана")
            
            # Таблица истории статусов
            cursor.execute('''
                CREATE TABLE application_status_history (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    application_id INT NOT NULL,
                    old_status ENUM('new', 'in_progress', 'completed'),
                    new_status ENUM('new', 'in_progress', 'completed') NOT NULL,
                    changed_by VARCHAR(50) DEFAULT 'Admin',
                    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (application_id) REFERENCES applications(id) ON DELETE CASCADE,
                    
                    INDEX idx_application_id (application_id),
                    INDEX idx_changed_at (changed_at)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            print("   ✅ Таблица 'application_status_history' создана")
            
            # Генерация правильных хешей паролей
            print("\n3. Генерация паролей...")
            passwords = {
                'Admin': 'KorokNET',
                'user1': 'password123',
                'user2': 'password456'
            }
            
            hashes = {}
            for user, password in passwords.items():
                hashed = generate_password_hash(password)
                hashes[user] = hashed
                print(f"   ✅ {user}: {password} -> хеш создан")
            
            # Заполняем данными
            print("\n4. Заполнение данными...")
            
            # Курсы
            cursor.executemany('''
                INSERT INTO courses (name, description) VALUES (%s, %s)
            ''', [
                ('Основы алгоритмизации и программирования', 'Курс по основам алгоритмов и программирования'),
                ('Основы веб-дизайна', 'Курс по основам дизайна веб-приложений'),
                ('Основы проектирования баз данных', 'Курс по проектированию и разработке баз данных')
            ])
            print("   ✅ Курсы добавлены")
            
            # Пользователи
            cursor.executemany('''
                INSERT INTO users (login, password_hash, full_name, phone, email) 
                VALUES (%s, %s, %s, %s, %s)
            ''', [
                ('Admin', hashes['Admin'], 'Администратор Системы', '8(999)123-45-67', 'admin@korokki-est.ru'),
                ('user1', hashes['user1'], 'Иванов Иван Иванович', '8(911)111-11-11', 'ivanov@example.com'),
                ('user2', hashes['user2'], 'Петров Петр Петрович', '8(922)222-22-22', 'petrov@example.com')
            ])
            print("   ✅ Пользователи добавлены")
            
            # Заявки
            cursor.executemany('''
                INSERT INTO applications (user_id, course_id, desired_start_date, payment_method, status) 
                VALUES (%s, %s, %s, %s, %s)
            ''', [
                (2, 1, '2024-09-01', 'cash', 'new'),
                (3, 2, '2024-10-01', 'bank_transfer', 'in_progress'),
                (2, 3, '2024-11-01', 'cash', 'completed')
            ])
            print("   ✅ Заявки добавлены")
            
            # Отзывы
            cursor.execute('''
                INSERT INTO reviews (user_id, application_id, rating, comment) 
                VALUES (%s, %s, %s, %s)
            ''', (2, 3, 5, 'Отличный курс! Рекомендую всем.'))
            print("   ✅ Отзывы добавлены")
            
            # История статусов
            cursor.executemany('''
                INSERT INTO application_status_history (application_id, old_status, new_status, changed_by) 
                VALUES (%s, %s, %s, %s)
            ''', [
                (2, 'new', 'in_progress', 'Admin'),
                (2, 'in_progress', 'completed', 'Admin')
            ])
            print("   ✅ История статусов добавлена")
            
            connection.commit()
            
            print("\n" + "=" * 60)
            print("БАЗА ДАННЫХ УСПЕШНО ПЕРЕСОЗДАНА!")
            print("=" * 60)
            print("\nТестовые учетные записи:")
            print("1. Администратор:")
            print("   Логин: Admin")
            print("   Пароль: KorokNET")
            print("\n2. Пользователь 1:")
            print("   Логин: user1")
            print("   Пароль: password123")
            print("\n3. Пользователь 2:")
            print("   Логин: user2")
            print("   Пароль: password456")
            print("\nДля запуска приложения выполните:")
            print("python3 app.py")
            print("\nИли используйте скрипт запуска:")
            print("./start_project.sh")
            print("=" * 60)
            
    except pymysql.Error as e:
        print(f"\n❌ Ошибка MySQL: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        return False
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
    
    return True

if __name__ == '__main__':
    recreate_database()