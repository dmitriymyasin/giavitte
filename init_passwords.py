#!/usr/bin/env python3
"""
Скрипт для генерации хешей паролей
"""

from werkzeug.security import generate_password_hash

def main():
    print("Генератор хешей паролей")
    print("=" * 50)
    
    # Пароли из задания
    passwords = {
        'Admin': 'KorokNET',
        'user1': 'password123',
        'user2': 'password456'
    }
    
    print("Сгенерированные хеши паролей (werkzeug):")
    print("-" * 50)
    
    for username, password in passwords.items():
        hashed = generate_password_hash(password)
        print(f"Пользователь: {username}")
        print(f"Пароль: {password}")
        print(f"Хеш: {hashed}")
        print("-" * 50)

if __name__ == '__main__':
    main()