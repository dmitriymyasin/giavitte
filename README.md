# Портал "Корочки.есть"

Информационная система для записи на онлайн курсы дополнительного профессионального образования.

## Требования

- Python 3.8 или выше
- MySQL 5.7 или выше
- Git (для скачивания проекта)

## Установка и запуск

### Быстрый запуск (автоматический)

#### Скачивание bootstrap
curl -o static/css/bootstrap.min.css https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
curl -o static/js/bootstrap.bundle.min.js https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js

```bash
# Сделайте скрипт исполняемым
chmod +x run.sh

# Запустите проект
./run.sh