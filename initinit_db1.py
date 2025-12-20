# init_db.py
#!/usr/bin/env python3
"""
Инициализация базы данных для портала "Буквоежка"
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, BookCard
from werkzeug.security import generate_password_hash

def init_database():
    print("=" * 60)
    print("Инициализация базы данных 'Буквоежка'")
    print("=" * 60)
    
    with app.app_context():
        # Создаем таблицы
        print("1. Создание таблиц...")
        db.create_all()
        print("   ✅ Таблицы созданы")
        
        # Проверяем, есть ли уже данные
        if User.query.first() is None:
            print("\n2. Заполнение начальными данными...")
            
            # Создаем тестового пользователя
            user1 = User(
                login='пользователь1',
                full_name='Иванов Иван Иванович',
                phone='+7(911)111-11-11',
                email='user1@example.com'
            )
            user1.set_password('password123')
            
            # Создаем администратора
            admin = User(
                login='admin',
                full_name='Администратор Системы',
                phone='+7(999)999-99-99',
                email='admin@bookworm.ru'
            )
            admin.set_password('bookworm')
            
            db.session.add_all([user1, admin])
            
            # Создаем тестовые карточки
            cards = [
                BookCard(
                    user_id=1,
                    author='Лев Толстой',
                    title='Война и мир',
                    card_type='share',
                    publisher='Эксмо',
                    year=2015,
                    binding='Твердый',
                    condition='Отличное',
                    status='approved'
                ),
                BookCard(
                    user_id=1,
                    author='Фёдор Достоевский',
                    title='Преступление и наказание',
                    card_type='want',
                    publisher='АСТ',
                    status='pending'
                ),
            ]
            
            db.session.add_all(cards)
            db.session.commit()
            
            print("   ✅ Тестовые данные добавлены")
        
        # Выводим статистику
        print("\n" + "=" * 60)
        print("📊 СТАТИСТИКА БАЗЫ ДАННЫХ:")
        print("=" * 60)
        
        users_count = User.query.count()
        cards_count = BookCard.query.count()
        pending_count = BookCard.query.filter_by(status='pending').count()
        approved_count = BookCard.query.filter_by(status='approved').count()
        
        print(f"   👥 Пользователей: {users_count}")
        print(f"   📚 Карточек книг: {cards_count}")
        print(f"   ⏳ На модерации: {pending_count}")
        print(f"   ✅ Одобрено: {approved_count}")
        
        print("\n🔑 ТЕСТОВЫЕ УЧЕТНЫЕ ЗАПИСИ:")
        print("   👑 Администратор:")
        print("      Логин: admin")
        print("      Пароль: bookworm")
        
        print("\n   👤 Обычный пользователь:")
        print("      Логин: пользователь1")
        print("      Пароль: password123")
        print("      Email: user1@example.com")
        
        print("\n" + "=" * 60)
        print("✅ БАЗА ДАННЫХ УСПЕШНО ПРОИНИЦИАЛИЗИРОВАНА!")
        print("=" * 60)

if __name__ == '__main__':
    init_database()