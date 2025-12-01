#!/bin/bash

echo "========================================"
echo "   Запуск проекта 'Корочки.есть'"
echo "========================================"
echo ""

# Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "ОШИБКА: Python3 не найден. Установите Python 3.8 или выше."
    exit 1
fi

echo "✓ Python найден"

# Создание виртуального окружения
if [ ! -d "venv" ]; then
    echo "Создание виртуального окружения..."
    python3 -m venv venv
    echo "✓ Виртуальное окружение создано"
fi

# Активация виртуального окружения
echo "Активация виртуального окружения..."
source venv/bin/activate

# Установка зависимостей
echo "Установка зависимостей..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✓ Зависимости установлены"

# Проверка MySQL
echo "Проверка подключения к MySQL..."
if mysql -h localhost -u root -pHfgFGty217GF -e "SELECT 1;" 2>/dev/null; then
    echo "✓ Подключение к MySQL успешно"
    
    # Проверка базы данных
    if mysql -h localhost -u root -pHfgFGty217GF -e "USE vitte;" 2>/dev/null; then
        echo "✓ База данных 'vitte' существует"
    else
        echo "Создание базы данных 'vitte'..."
        mysql -h localhost -u root -pHfgFGty217GF -e "CREATE DATABASE IF NOT EXISTS vitte CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
        echo "✓ База данных создана"
    fi
else
    echo "ВНИМАНИЕ: Не удалось подключиться к MySQL"
    echo "Убедитесь, что MySQL запущен и пароль правильный: root:HfgFGty217GF"
    read -p "Продолжить без проверки БД? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Завершение работы..."
        exit 1
    fi
fi

# Инициализация базы данных
echo "Инициализация базы данных..."
python3 init_database.py

# Запуск приложения
echo ""
echo "========================================"
echo "   Запуск приложения..."
echo "========================================"
echo "Сервер будет доступен по адресу: http://localhost:5000"
echo "Для остановки нажмите Ctrl+C"
echo ""

export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000