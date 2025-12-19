#!/usr/bin/env python3
"""
Полное пересоздание базы данных с правильными паролями для SQLite с использованием SQLAlchemy
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from werkzeug.security import generate_password_hash
from datetime import datetime
from app import app
from models import db, User, Course, Application, Review, ApplicationStatusHistory, ReviewStats

def recreate_database():
    print("=" * 60)
    print("Пересоздание базы данных 'Корочки.есть' (SQLite + SQLAlchemy)")
    print("=" * 60)
    
    with app.app_context():
        # Удаляем старую базу данных если она существует
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_path = os.path.join(basedir, 'vitte.db')
        
        print(f"📂 Путь к базе данных: {db_path}")
        
        # Удаляем все таблицы и создаем заново
        print("\n1. Создание таблиц...")
        db.drop_all()
        db.create_all()
        print("   ✅ Таблицы созданы")
        
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
        courses = [
            Course(
                name='Основы алгоритмизации и программирования',
                description='Курс по основам алгоритмов и программирования на Python и C++. Изучаем базовые структуры данных, алгоритмы сортировки и поиска, принципы ООП. Подходит для начинающих программистов.'
            ),
            Course(
                name='Основы веб-дизайна',
                description='Курс по основам дизайна веб-приложений. Изучаем HTML, CSS, основы UX/UI, адаптивную верстку, работу с Figma и Adobe XD. Научитесь создавать современные интерфейсы.'
            ),
            Course(
                name='Основы проектирования баз данных',
                description='Курс по проектированию и разработке баз данных. Изучаем SQL, нормализацию, проектирование ER-диаграмм, оптимизацию запросов, работу с MySQL и PostgreSQL.'
            ),
            Course(
                name='Машинное обучение для начинающих',
                description='Введение в машинное обучение на Python. Изучаем библиотеки scikit-learn, pandas, основы нейронных сетей, работу с данными и построение моделей.'
            ),
            Course(
                name='Разработка мобильных приложений',
                description='Курс по разработке мобильных приложений на React Native. Создаем кроссплатформенные приложения для iOS и Android с нуля.'
            )
        ]
        
        for course in courses:
            db.session.add(course)
        db.session.commit()
        print("   ✅ Курсы добавлены")
        
        # Пользователи
        users = [
            User(
                login='Admin',
                password_hash=hashes['Admin'],
                full_name='Администратор Системы',
                phone='8(999)123-45-67',
                email='admin@korokki-est.ru'
            ),
            User(
                login='user1',
                password_hash=hashes['user1'],
                full_name='Иванов Иван Иванович',
                phone='8(911)111-11-11',
                email='ivanov@example.com'
            ),
            User(
                login='user2',
                password_hash=hashes['user2'],
                full_name='Петров Петр Петрович',
                phone='8(922)222-22-22',
                email='petrov@example.com'
            ),
            User(
                login='user3',
                password_hash=hashes['user3'],
                full_name='Сидорова Анна Сергеевна',
                phone='8(933)333-33-33',
                email='sidorova@example.com'
            ),
            User(
                login='user4',
                password_hash=hashes['user4'],
                full_name='Кузнецова Мария Дмитриевна',
                phone='8(944)444-44-44',
                email='kuznetsova@example.com'
            ),
            User(
                login='user5',
                password_hash=hashes['user5'],
                full_name='Смирнов Алексей Владимирович',
                phone='8(955)555-55-55',
                email='smirnov@example.com'
            )
        ]
        
        for user in users:
            db.session.add(user)
        db.session.commit()
        print("   ✅ Пользователи добавлены")
        
        # Заявки
        print("\n4. Добавление заявок...")
        applications = [
            # user1
            Application(
                user_id=2,
                course_id=1,
                desired_start_date=datetime(2024, 9, 1).date(),
                payment_method='cash',
                status='completed'
            ),
            Application(
                user_id=2,
                course_id=2,
                desired_start_date=datetime(2024, 10, 15).date(),
                payment_method='bank_transfer',
                status='completed'
            ),
            Application(
                user_id=2,
                course_id=3,
                desired_start_date=datetime(2024, 11, 1).date(),
                payment_method='cash',
                status='in_progress'
            ),
            # user2
            Application(
                user_id=3,
                course_id=1,
                desired_start_date=datetime(2024, 9, 10).date(),
                payment_method='bank_transfer',
                status='completed'
            ),
            Application(
                user_id=3,
                course_id=4,
                desired_start_date=datetime(2024, 10, 20).date(),
                payment_method='cash',
                status='completed'
            ),
            Application(
                user_id=3,
                course_id=5,
                desired_start_date=datetime(2024, 12, 1).date(),
                payment_method='bank_transfer',
                status='new'
            ),
            # user3
            Application(
                user_id=4,
                course_id=2,
                desired_start_date=datetime(2024, 8, 15).date(),
                payment_method='cash',
                status='completed'
            ),
            Application(
                user_id=4,
                course_id=3,
                desired_start_date=datetime(2024, 9, 20).date(),
                payment_method='bank_transfer',
                status='completed'
            ),
            Application(
                user_id=4,
                course_id=5,
                desired_start_date=datetime(2025, 1, 10).date(),
                payment_method='cash',
                status='in_progress'
            ),
            # user4
            Application(
                user_id=5,
                course_id=1,
                desired_start_date=datetime(2024, 7, 1).date(),
                payment_method='bank_transfer',
                status='completed'
            ),
            Application(
                user_id=5,
                course_id=4,
                desired_start_date=datetime(2024, 8, 10).date(),
                payment_method='cash',
                status='completed'
            ),
            # user5
            Application(
                user_id=6,
                course_id=2,
                desired_start_date=datetime(2024, 9, 5).date(),
                payment_method='cash',
                status='completed'
            ),
            Application(
                user_id=6,
                course_id=3,
                desired_start_date=datetime(2024, 10, 10).date(),
                payment_method='bank_transfer',
                status='completed'
            )
        ]
        
        for application in applications:
            db.session.add(application)
        db.session.commit()
        print("   ✅ Заявки добавлены")
        
        # Отзывы
        print("\n5. Добавление отзывов...")
        reviews = [
            # user1
            Review(
                user_id=2,
                application_id=1,
                rating=5,
                comment='Отличный курс для начинающих! Преподаватель объясняет сложные темы простым языком. Особенно понравились практические задания. Рекомендую всем, кто хочет начать программировать.',
                created_at=datetime(2024, 9, 30, 14, 30, 0)
            ),
            Review(
                user_id=2,
                application_id=2,
                rating=4,
                comment='Хороший курс по веб-дизайну. Много полезной информации по современным тенденциям. Не хватило больше практики по адаптивной верстке.',
                created_at=datetime(2024, 11, 5, 10, 15, 0)
            ),
            # user2
            Review(
                user_id=3,
                application_id=4,
                rating=5,
                comment='Лучший курс по программированию, который я проходил! Все структурировано, от простого к сложному. Домашние задания помогают закрепить материал. Спасибо преподавателю!',
                created_at=datetime(2024, 10, 1, 16, 45, 0)
            ),
            Review(
                user_id=3,
                application_id=5,
                rating=4,
                comment='Интересный курс по машинному обучению. Хорошо подобран материал для начинающих. Хотелось бы больше реальных проектов и работы с большими данными.',
                created_at=datetime(2024, 11, 25, 9, 20, 0)
            ),
            # user3
            Review(
                user_id=4,
                application_id=7,
                rating=3,
                comment='Курс неплохой, но есть недочеты. Некоторые темы рассмотрены поверхностно. Хорошая теоретическая база, но практики маловато.',
                created_at=datetime(2024, 9, 10, 11, 30, 0)
            ),
            Review(
                user_id=4,
                application_id=8,
                rating=5,
                comment='Отличный курс по базам данных! Все очень подробно: от теории до сложных запросов. Научился проектировать нормализованные базы и оптимизировать запросы. Рекомендую!',
                created_at=datetime(2024, 10, 25, 15, 10, 0)
            ),
            # user4
            Review(
                user_id=5,
                application_id=10,
                rating=5,
                comment='Супер курс! Прошел его с нуля, теперь пишу программы на Python. Преподаватель всегда на связи, помогает с вопросами. Материал актуальный и полезный.',
                created_at=datetime(2024, 8, 30, 13, 45, 0)
            ),
            Review(
                user_id=5,
                application_id=11,
                rating=4,
                comment='Понравился курс по машинному обучению. Много практических примеров. Из минусов - некоторые библиотеки устарели, нужно обновлять материалы.',
                created_at=datetime(2024, 9, 15, 17, 20, 0)
            ),
            # user5
            Review(
                user_id=6,
                application_id=12,
                rating=5,
                comment='Прекрасный курс по веб-дизайну! Научилась создавать современные интерфейсы, работать с Figma. Теперь могу работать веб-дизайнером. Спасибо!',
                created_at=datetime(2024, 10, 5, 14, 0, 0)
            ),
            Review(
                user_id=6,
                application_id=13,
                rating=4,
                comment='Хороший курс по базам данных. Получил много полезных знаний по SQL и проектированию. Есть небольшие замечания по организации материала, но в целом рекомендую.',
                created_at=datetime(2024, 11, 15, 10, 30, 0)
            )
        ]
        
        for review in reviews:
            db.session.add(review)
        db.session.commit()
        print("   ✅ Отзывы добавлены")
        
        # История статусов
        print("\n6. Добавление истории статусов...")
        
        # Для завершенных заявок
        completed_app_ids = [1, 2, 4, 5, 7, 8, 10, 11, 12, 13]
        for app_id in completed_app_ids:
            db.session.add(ApplicationStatusHistory(
                application_id=app_id,
                old_status='new',
                new_status='in_progress',
                changed_by='Admin'
            ))
            db.session.add(ApplicationStatusHistory(
                application_id=app_id,
                old_status='in_progress',
                new_status='completed',
                changed_by='Admin'
            ))
        
        # Для заявок в процессе
        in_progress_app_ids = [3, 9]
        for app_id in in_progress_app_ids:
            db.session.add(ApplicationStatusHistory(
                application_id=app_id,
                old_status='new',
                new_status='in_progress',
                changed_by='Admin'
            ))
        
        db.session.commit()
        print("   ✅ История статусов добавлена")
        
        # Вычисляем статистику отзывов
        print("\n7. Расчет статистики отзывов...")
        
        # Получаем все курсы
        courses = Course.query.all()
        for course in courses:
            # Находим все отзывы для этого курса
            reviews_for_course = Review.query.join(Application).filter(
                Application.course_id == course.id
            ).all()
            
            total_reviews = len(reviews_for_course)
            if total_reviews > 0:
                avg_rating = sum(r.rating for r in reviews_for_course) / total_reviews
            else:
                avg_rating = 0.0
            
            # Создаем или обновляем статистику
            stats = ReviewStats.query.filter_by(course_id=course.id).first()
            if not stats:
                stats = ReviewStats(course_id=course.id)
            
            stats.total_reviews = total_reviews
            stats.average_rating = avg_rating
            db.session.add(stats)
        
        db.session.commit()
        print("   ✅ Статистика отзывов рассчитана")
        
        # Выводим итоговую статистику
        print("\n" + "=" * 60)
        print("📊 ИТОГОВАЯ СТАТИСТИКА БАЗЫ ДАННЫХ:")
        print("=" * 60)
        
        users_count = User.query.count()
        courses_count = Course.query.count()
        apps_count = Application.query.count()
        reviews_count = Review.query.count()
        history_count = ApplicationStatusHistory.query.count()
        
        print(f"   👥 Пользователей: {users_count}")
        print(f"   📚 Курсов: {courses_count}")
        print(f"   📝 Заявок: {apps_count}")
        print(f"   ⭐ Отзывов: {reviews_count}")
        print(f"   📋 Записей истории: {history_count}")
        
        # Статистика по курсам
        print("\n   📈 РЕЙТИНГ КУРСОВ:")
        courses_with_stats = Course.query.outerjoin(ReviewStats).order_by(
            db.desc(ReviewStats.average_rating), Course.name
        ).all()
        
        for course in courses_with_stats:
            stats = course.stats
            avg_rating = stats.average_rating if stats else 0
            total_reviews = stats.total_reviews if stats else 0
            
            stars = "★" * int(round(avg_rating))
            empty_stars = "☆" * (5 - int(round(avg_rating))) if avg_rating > 0 else "☆☆☆☆☆"
            reviews_text = f"({total_reviews} отзывов)" if total_reviews > 0 else "(нет отзывов)"
            print(f"      📖 {course.name}")
            print(f"          {avg_rating:.1f}/5 {stars}{empty_stars} {reviews_text}")
        
        print("\n" + "=" * 60)
        print("✅ БАЗА ДАННЫХ SQLite УСПЕШНО СОЗДАНА!")
        print("=" * 60)
        
        print("\n🔑 ТЕСТОВЫЕ УЧЕТНЫЕ ЗАПИСИ:")
        print("   👑 Администратор: Логин: Admin | Пароль: KorokNET")
        print("\n   👤 Обычные пользователи:")
        print("      1. Логин: user1 | Пароль: password123")
        print("      2. Логин: user2 | Пароль: password456")
        print("      3. Логин: user3 | Пароль: password789")
        print("      4. Логин: user4 | Пароль: password012")
        print("      5. Логин: user5 | Пароль: password345")
        
        print("\n🚀 ДЛЯ ЗАПУСКА ПРИЛОЖЕНИЯ:")
        print("   1. Запустите скрипт: ./run.sh")
        print("   2. Или выполните: python3 app.py")
        
        print("\n🌐 СЕРВЕР БУДЕТ ДОСТУПЕН ПО АДРЕСУ:")
        print("   http://localhost:5000")
        
        print("\n" + "=" * 60)
    
    return True

if __name__ == '__main__':
    recreate_database()