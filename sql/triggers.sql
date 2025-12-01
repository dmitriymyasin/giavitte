USE `vitte`;

DELIMITER //

-- Триггер для автоматической записи истории изменения статусов
CREATE TRIGGER `log_status_change`
AFTER UPDATE ON `applications`
FOR EACH ROW
BEGIN
    IF OLD.status != NEW.status THEN
        INSERT INTO `application_status_history` 
        (`application_id`, `old_status`, `new_status`, `changed_by`)
        VALUES (NEW.id, OLD.status, NEW.status, 'Admin');
    END IF;
END//

DELIMITER ;

-- Представление для удобного просмотра заявок
CREATE VIEW `application_details` AS
SELECT 
    a.id,
    a.user_id,
    u.login AS user_login,
    u.full_name AS user_name,
    u.email AS user_email,
    a.course_id,
    c.name AS course_name,
    a.desired_start_date,
    a.payment_method,
    a.status,
    a.created_at,
    a.updated_at,
    r.rating,
    r.comment AS review_comment
FROM `applications` a
LEFT JOIN `users` u ON a.user_id = u.id
LEFT JOIN `courses` c ON a.course_id = c.id
LEFT JOIN `reviews` r ON a.id = r.application_id;