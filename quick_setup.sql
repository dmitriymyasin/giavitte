-- Быстрая настройка базы данных для проекта "Корочки.есть"

-- Создание базы данных
CREATE DATABASE IF NOT EXISTS `vitte` 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `vitte`;

-- Создание таблиц
SOURCE sql/schema.sql;

-- Заполнение данных
SOURCE sql/data.sql;

-- Создание триггеров
SOURCE sql/triggers.sql;

-- Создание пользователей для доступа
CREATE USER IF NOT EXISTS 'korochki_user'@'localhost' IDENTIFIED BY 'korochki_pass_2024';
GRANT ALL PRIVILEGES ON `vitte`.* TO 'korochki_user'@'localhost';
FLUSH PRIVILEGES;

-- Проверка созданных таблиц
SHOW TABLES;

-- Проверка данных
SELECT 'Курсы:' AS '';
SELECT * FROM courses;

SELECT 'Пользователи:' AS '';
SELECT id, login, full_name, email FROM users;

SELECT 'Заявки:' AS '';
SELECT a.id, u.login, c.name, a.status 
FROM applications a
JOIN users u ON a.user_id = u.id
JOIN courses c ON a.course_id = c.id;

print_info "База данных успешно настроена!"