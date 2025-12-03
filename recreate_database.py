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
            
            # Таблица статистики отзывов
            cursor.execute('''
                CREATE TABLE review_stats (
                    course_id INT PRIMARY KEY,
                    total_reviews INT DEFAULT 0,
                    average_rating FLOAT DEFAULT 0.0,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            ''')
            print("   ✅ Таблица 'review_stats' создана")
            
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
            print("\n4. Заполнение данными...")
            
            # Курсы с описаниями
            cursor.executemany('''
                INSERT INTO courses (name, description) VALUES (%s, %s)
            ''', [
                ('Основы алгоритмизации и программирования', 'Курс по основам алгоритмов и программирования на Python и C++. Изучаем базовые структуры данных, алгоритмы сортировки и поиска, принципы ООП. Подходит для начинающих программистов.'),
                ('Основы веб-дизайна', 'Курс по основам дизайна веб-приложений. Изучаем HTML, CSS, основы UX/UI, адаптивную верстку, работу с Figma и Adobe XD. Научитесь создавать современные интерфейсы.'),
                ('Основы проектирования баз данных', 'Курс по проектированию и разработке баз данных. Изучаем SQL, нормализацию, проектирование ER-диаграмм, оптимизацию запросов, работу с MySQL и PostgreSQL.'),
                ('Машинное обучение для начинающих', 'Введение в машинное обучение на Python. Изучаем библиотеки scikit-learn, pandas, основы нейронных сетей, работу с данными и построение моделей.'),
                ('Разработка мобильных приложений', 'Курс по разработке мобильных приложений на React Native. Создаем кроссплатформенные приложения для iOS и Android с нуля.')
            ])
            print("   ✅ Курсы добавлены")
            
            # Пользователи
            cursor.executemany('''
                INSERT INTO users (login, password_hash, full_name, phone, email) 
                VALUES (%s, %s, %s, %s, %s)
            ''', [
                ('Admin', hashes['Admin'], 'Администратор Системы', '8(999)123-45-67', 'admin@korokki-est.ru'),
                ('user1', hashes['user1'], 'Иванов Иван Иванович', '8(911)111-11-11', 'ivanov@example.com'),
                ('user2', hashes['user2'], 'Петров Петр Петрович', '8(922)222-22-22', 'petrov@example.com'),
                ('user3', hashes['user3'], 'Сидорова Анна Сергеевна', '8(933)333-33-33', 'sidorova@example.com'),
                ('user4', hashes['user4'], 'Кузнецова Мария Дмитриевна', '8(944)444-44-44', 'kuznetsova@example.com'),
                ('user5', hashes['user5'], 'Смирнов Алексей Владимирович', '8(955)555-55-55', 'smirnov@example.com')
            ])
            print("   ✅ Пользователи добавлены")
            
            # Заявки - добавляем по одной, чтобы получить их ID
            print("\n5. Добавление заявок...")
            applications_data = [
                # user1 - заявка 1
                (2, 1, '2024-09-01', 'cash', 'completed'),
                # user1 - заявка 2
                (2, 2, '2024-10-15', 'bank_transfer', 'completed'),
                # user1 - заявка 3
                (2, 3, '2024-11-01', 'cash', 'in_progress'),
                # user2 - заявка 4
                (3, 1, '2024-09-10', 'bank_transfer', 'completed'),
                # user2 - заявка 5
                (3, 4, '2024-10-20', 'cash', 'completed'),
                # user2 - заявка 6
                (3, 5, '2024-12-01', 'bank_transfer', 'new'),
                # user3 - заявка 7
                (4, 2, '2024-08-15', 'cash', 'completed'),
                # user3 - заявка 8
                (4, 3, '2024-09-20', 'bank_transfer', 'completed'),
                # user3 - заявка 9
                (4, 5, '2025-01-10', 'cash', 'in_progress'),
                # user4 - заявка 10
                (5, 1, '2024-07-01', 'bank_transfer', 'completed'),
                # user4 - заявка 11
                (5, 4, '2024-08-10', 'cash', 'completed'),
                # user5 - заявка 12
                (6, 2, '2024-09-05', 'cash', 'completed'),
                # user5 - заявка 13
                (6, 3, '2024-10-10', 'bank_transfer', 'completed')
            ]
            
            application_ids = []
            for app_data in applications_data:
                cursor.execute('''
                    INSERT INTO applications (user_id, course_id, desired_start_date, payment_method, status) 
                    VALUES (%s, %s, %s, %s, %s)
                ''', app_data)
                application_ids.append(cursor.lastrowid)
            
            print(f"   ✅ Заявки добавлены (ID: {', '.join(map(str, application_ids))})")
            
            # Теперь добавляем отзывы с правильными application_id
            print("\n6. Добавление отзывов...")
            reviews_data = [
                # Отзывы user1 на заявку 1 (Основы алгоритмизации)
                (2, application_ids[0], 5, 'Отличный курс для начинающих! Преподаватель объясняет сложные темы простым языком. Особенно понравились практические задания. Рекомендую всем, кто хочет начать программировать.', '2024-09-30 14:30:00'),
                
                # Отзывы user1 на заявку 2 (Веб-дизайн)
                (2, application_ids[1], 4, 'Хороший курс по веб-дизайну. Много полезной информации по современным тенденциям. Не хватило больше практики по адаптивной верстке.', '2024-11-05 10:15:00'),
                
                # Отзывы user2 на заявку 4 (Основы алгоритмизации)
                (3, application_ids[3], 5, 'Лучший курс по программированию, который я проходил! Все структурировано, от простого к сложному. Домашние задания помогают закрепить материал. Спасибо преподавателю!', '2024-10-01 16:45:00'),
                
                # Отзывы user2 на заявку 5 (Машинное обучение)
                (3, application_ids[4], 4, 'Интересный курс по машинному обучению. Хорошо подобран материал для начинающих. Хотелось бы больше реальных проектов и работы с большими данными.', '2024-11-25 09:20:00'),
                
                # Отзывы user3 на заявку 7 (Веб-дизайн)
                (4, application_ids[6], 3, 'Курс неплохой, но есть недочеты. Некоторые темы рассмотрены поверхностно. Хорошая теоретическая база, но практики маловато.', '2024-09-10 11:30:00'),
                
                # Отзывы user3 на заявку 8 (Базы данных)
                (4, application_ids[7], 5, 'Отличный курс по базам данных! Все очень подробно: от теории до сложных запросов. Научился проектировать нормализованные базы и оптимизировать запросы. Рекомендую!', '2024-10-25 15:10:00'),
                
                # Отзывы user4 на заявку 10 (Основы алгоритмизации)
                (5, application_ids[9], 5, 'Супер курс! Прошел его с нуля, теперь пишу программы на Python. Преподаватель всегда на связи, помогает с вопросами. Материал актуальный и полезный.', '2024-08-30 13:45:00'),
                
                # Отзывы user4 на заявку 11 (Машинное обучение)
                (5, application_ids[10], 4, 'Понравился курс по машинному обучению. Много практических примеров. Из минусов - некоторые библиотеки устарели, нужно обновлять материалы.', '2024-09-15 17:20:00'),
                
                # Отзывы user5 на заявку 12 (Веб-дизайн)
                (6, application_ids[11], 5, 'Прекрасный курс по веб-дизайну! Научилась создавать современные интерфейсы, работать с Figma. Теперь могу работать веб-дизайнером. Спасибо!', '2024-10-05 14:00:00'),
                
                # Отзывы user5 на заявку 13 (Базы данных)
                (6, application_ids[12], 4, 'Хороший курс по базам данных. Получил много полезных знаний по SQL и проектированию. Есть небольшие замечания по организации материала, но в целом рекомендую.', '2024-11-15 10:30:00')
            ]
            
            for review_data in reviews_data:
                cursor.execute('''
                    INSERT INTO reviews (user_id, application_id, rating, comment, created_at) 
                    VALUES (%s, %s, %s, %s, %s)
                ''', review_data)
            
            print("   ✅ Отзывы добавлены")
            
            # История статусов
            print("\n7. Добавление истории статусов...")
            status_history_data = []
            
            # Для завершенных заявок добавляем полную историю
            completed_app_ids = [application_ids[0], application_ids[1], application_ids[3], application_ids[4],
                               application_ids[6], application_ids[7], application_ids[9], application_ids[10],
                               application_ids[11], application_ids[12]]
            
            for app_id in completed_app_ids:
                # Добавляем переход из new в in_progress
                status_history_data.append((app_id, 'new', 'in_progress', 'Admin'))
                # Добавляем переход из in_progress в completed
                status_history_data.append((app_id, 'in_progress', 'completed', 'Admin'))
            
            # Для заявок в процессе добавляем только первый переход
            in_progress_app_ids = [application_ids[2], application_ids[8]]
            for app_id in in_progress_app_ids:
                status_history_data.append((app_id, 'new', 'in_progress', 'Admin'))
            
            if status_history_data:
                cursor.executemany('''
                    INSERT INTO application_status_history (application_id, old_status, new_status, changed_by) 
                    VALUES (%s, %s, %s, %s)
                ''', status_history_data)
            
            print("   ✅ История статусов добавлена")
            
            # Вычисляем и вставляем статистику отзывов
            print("\n8. Расчет статистики отзывов...")
            
            # Получаем статистику по курсам
            cursor.execute('''
                SELECT 
                    c.id as course_id,
                    COUNT(r.id) as total_reviews,
                    AVG(r.rating) as average_rating
                FROM courses c
                LEFT JOIN applications a ON c.id = a.course_id
                LEFT JOIN reviews r ON a.id = r.application_id
                GROUP BY c.id
            ''')
            
            stats = cursor.fetchall()
            for stat in stats:
                if stat['total_reviews'] > 0:
                    cursor.execute('''
                        INSERT INTO review_stats (course_id, total_reviews, average_rating)
                        VALUES (%s, %s, %s)
                    ''', (stat['course_id'], stat['total_reviews'], float(stat['average_rating'])))
                else:
                    # Для курсов без отзывов добавляем нулевую статистику
                    cursor.execute('''
                        INSERT INTO review_stats (course_id, total_reviews, average_rating)
                        VALUES (%s, 0, 0.0)
                    ''', (stat['course_id'],))
            
            print("   ✅ Статистика отзывов рассчитана")
            
            connection.commit()
            
            # Выводим итоговую статистику
            print("\n" + "=" * 60)
            print("📊 ИТОГОВАЯ СТАТИСТИКА БАЗЫ ДАННЫХ:")
            print("=" * 60)
            
            cursor.execute("SELECT COUNT(*) as count FROM users")
            users_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM courses")
            courses_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM applications")
            apps_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM reviews")
            reviews_count = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM application_status_history")
            history_count = cursor.fetchone()['count']
            
            print(f"   👥 Пользователей: {users_count}")
            print(f"   📚 Курсов: {courses_count}")
            print(f"   📝 Заявок: {apps_count}")
            print(f"   ⭐ Отзывов: {reviews_count}")
            print(f"   📋 Записей истории: {history_count}")
            
            # Исправленный запрос без NULLS LAST
            cursor.execute('''
                SELECT 
                    c.name,
                    COALESCE(rs.total_reviews, 0) as total_reviews,
                    ROUND(COALESCE(rs.average_rating, 0), 1) as avg_rating
                FROM courses c
                LEFT JOIN review_stats rs ON c.id = rs.course_id
                ORDER BY rs.average_rating DESC, c.name ASC
            ''')
            course_stats = cursor.fetchall()
            
            print("\n   📈 РЕЙТИНГ КУРСОВ:")
            for stat in course_stats:
                avg_rating = stat['avg_rating'] if stat['avg_rating'] else 0
                stars = "★" * int(round(avg_rating))
                empty_stars = "☆" * (5 - int(round(avg_rating))) if avg_rating > 0 else "☆☆☆☆☆"
                reviews_text = f"({stat['total_reviews']} отзывов)" if stat['total_reviews'] > 0 else "(нет отзывов)"
                print(f"      📖 {stat['name']}")
                print(f"          {avg_rating}/5 {stars}{empty_stars} {reviews_text}")
            
            print("\n" + "=" * 60)
            print("✅ БАЗА ДАННЫХ УСПЕШНО ПЕРЕСОЗДАНА!")
            print("=" * 60)
            
            print("\n🔑 ТЕСТОВЫЕ УЧЕТНЫЕ ЗАПИСИ:")
            print("   👑 Администратор:")
            print("      Логин: Admin")
            print("      Пароль: KorokNET")
            
            print("\n   👤 Обычные пользователи:")
            test_users = [
                ("user1", "password123", "Иванов Иван Иванович"),
                ("user2", "password456", "Петров Петр Петрович"),
                ("user3", "password789", "Сидорова Анна Сергеевна"),
                ("user4", "password012", "Кузнецова Мария Дмитриевна"),
                ("user5", "password345", "Смирнов Алексей Владимирович")
            ]
            
            for i, (login, password, name) in enumerate(test_users, 1):
                print(f"   {i}. Логин: {login} | Пароль: {password} | ФИО: {name}")
            
            print("\n💡 ЧТО МОЖНО ПРОТЕСТИРОВАТЬ:")
            print("   • 📝 Регистрация и авторизация")
            print("   • 📋 Создание заявок на курсы")
            print("   • ⭐ Просмотр и добавление отзывов")
            print("   • 📊 Фильтрация отзывов по курсам и рейтингу")
            print("   • 👑 Вход в панель администратора")
            print("   • 🔄 Изменение статусов заявок")
            
            print("\n🚀 ДЛЯ ЗАПУСКА ПРИЛОЖЕНИЯ:")
            print("   1. Запустите скрипт: ./run.sh")
            print("   2. Или выполните: python3 app.py")
            print("\n🌐 СЕРВЕР БУДЕТ ДОСТУПЕН ПО АДРЕСУ:")
            print("   http://localhost:5000")
            
            print("\n📱 ТЕСТОВЫЕ ССЫЛКИ:")
            print("   • Главная: http://localhost:5000")
            print("   • Все отзывы: http://localhost:5000/reviews")
            print("   • Панель админа: http://localhost:5000/admin/login")
            print("   • Статистика API: http://localhost:5000/api/course/1/reviews/stats")
            
            print("\n" + "=" * 60)
            
    except pymysql.Error as e:
        print(f"\n❌ Ошибка MySQL: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        if 'connection' in locals() and connection.open:
            connection.close()
    
    return True

if __name__ == '__main__':
    recreate_database()