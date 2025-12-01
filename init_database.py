from flask import Flask
from config import Config
from models import db, User, Course, Application, Review, ApplicationStatusHistory
from datetime import datetime, date

# Создаем временное приложение для инициализации БД
temp_app = Flask(__name__)
temp_app.config.from_object(Config)

db.init_app(temp_app)

def init_database():
    with temp_app.app_context():
        # Создаем все таблицы
        db.create_all()
        
        # Проверяем, есть ли уже данные
        if Course.query.count() == 0:
            print("Начальная настройка базы данных...")
            
            # Добавляем курсы
            courses = [
                Course(name='Основы алгоритмизации и программирования', 
                       description='Курс по основам алгоритмов и программирования'),
                Course(name='Основы веб-дизайна', 
                       description='Курс по основам дизайна веб-приложений'),
                Course(name='Основы проектирования баз данных', 
                       description='Курс по проектированию и разработке баз данных')
            ]
            
            for course in courses:
                db.session.add(course)
            
            # Создаем администратора
            admin = User(
                login='Admin',
                full_name='Администратор Системы',
                phone='8(999)123-45-67',
                email='admin@korokki-est.ru'
            )
            admin.set_password('KorokNET')
            db.session.add(admin)
            
            # Создаем тестовых пользователей
            test_users = [
                {'login': 'user1', 'password': 'password123', 'full_name': 'Иванов Иван Иванович', 
                 'phone': '8(911)111-11-11', 'email': 'ivanov@example.com'},
                {'login': 'user2', 'password': 'password456', 'full_name': 'Петров Петр Петрович',
                 'phone': '8(922)222-22-22', 'email': 'petrov@example.com'}
            ]
            
            for user_data in test_users:
                user = User(
                    login=user_data['login'],
                    full_name=user_data['full_name'],
                    phone=user_data['phone'],
                    email=user_data['email']
                )
                user.set_password(user_data['password'])
                db.session.add(user)
            
            db.session.commit()
            print("Базовые пользователи созданы")
            
            # Создаем тестовые заявки
            user1 = User.query.filter_by(login='user1').first()
            user2 = User.query.filter_by(login='user2').first()
            course1 = Course.query.filter_by(name='Основы алгоритмизации и программирования').first()
            course2 = Course.query.filter_by(name='Основы веб-дизайна').first()
            course3 = Course.query.filter_by(name='Основы проектирования баз данных').first()
            
            applications = [
                Application(user_id=user1.id, course_id=course1.id, 
                          desired_start_date=date(2024, 9, 1), 
                          payment_method='cash', status='new'),
                Application(user_id=user2.id, course_id=course2.id,
                          desired_start_date=date(2024, 10, 1),
                          payment_method='bank_transfer', status='in_progress'),
                Application(user_id=user1.id, course_id=course3.id,
                          desired_start_date=date(2024, 11, 1),
                          payment_method='cash', status='completed')
            ]
            
            for app in applications:
                db.session.add(app)
            
            db.session.commit()
            print("Тестовые заявки созданы")
            
            # Создаем тестовый отзыв
            application3 = Application.query.filter_by(user_id=user1.id, course_id=course3.id).first()
            if application3:
                review = Review(
                    user_id=user1.id,
                    application_id=application3.id,
                    rating=5,
                    comment='Отличный курс! Рекомендую всем.'
                )
                db.session.add(review)
            
            # Создаем историю изменения статусов
            for app in Application.query.all():
                if app.status != 'new':
                    history = ApplicationStatusHistory(
                        application_id=app.id,
                        old_status='new',
                        new_status=app.status,
                        changed_by='Admin'
                    )
                    db.session.add(history)
            
            db.session.commit()
            print("Тестовые данные добавлены")
            
            print("\n" + "="*50)
            print("База данных успешно инициализирована!")
            print("="*50)
            print("\nТестовые учетные записи:")
            print("1. Администратор:")
            print("   Логин: Admin")
            print("   Пароль: KorokNET")
            print("\n2. Тестовые пользователи:")
            print("   Логин: user1, Пароль: password123")
            print("   Логин: user2, Пароль: password456")
            print("\n3. Тестовые заявки уже созданы:")
            print("   - user1: 2 заявки (1 новая, 1 завершена)")
            print("   - user2: 1 заявка (в процессе)")
            print("\nПриложение доступно по адресу: http://localhost:5000")
            print("="*50)
        else:
            print("База данных уже содержит данные. Пропускаем инициализацию.")

if __name__ == '__main__':
    init_database()