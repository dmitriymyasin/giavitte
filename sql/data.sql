USE `vitte`;

-- Заполнение таблицы курсов
INSERT INTO `courses` (`name`, `description`) VALUES
('Основы алгоритмизации и программирования', 'Курс по основам алгоритмов и программирования'),
('Основы веб-дизайна', 'Курс по основам дизайна веб-приложений'),
('Основы проектирования баз данных', 'Курс по проектированию и разработке баз данных');

-- Создание пользователя администратора (логин: Admin, пароль: KorokNET)
-- Пароль хранится в зашифрованном виде (bcrypt hash для 'KorokNET')
-- Хэш: $2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW
INSERT INTO `users` (`login`, `password_hash`, `full_name`, `phone`, `email`) VALUES
('Admin', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Администратор Системы', '8(999)123-45-67', 'admin@korokki-est.ru');

-- Тестовые пользователи
INSERT INTO `users` (`login`, `password_hash`, `full_name`, `phone`, `email`) VALUES
('user1', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Иванов Иван Иванович', '8(911)111-11-11', 'ivanov@example.com'),
('user2', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Петров Петр Петрович', '8(922)222-22-22', 'petrov@example.com');

-- Тестовые заявки
INSERT INTO `applications` (`user_id`, `course_id`, `desired_start_date`, `payment_method`, `status`) VALUES
(2, 1, '2024-09-01', 'cash', 'new'),
(3, 2, '2024-10-01', 'bank_transfer', 'in_progress'),
(2, 3, '2024-11-01', 'cash', 'completed');

-- Тестовый отзыв
INSERT INTO `reviews` (`user_id`, `application_id`, `rating`, `comment`) VALUES
(2, 1, 5, 'Отличный курс! Рекомендую всем.');

-- История изменения статусов (пример)
INSERT INTO `application_status_history` (`application_id`, `old_status`, `new_status`, `changed_by`) VALUES
(3, 'new', 'in_progress', 'Admin'),
(3, 'in_progress', 'completed', 'Admin');