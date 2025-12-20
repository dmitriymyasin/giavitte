# app.py
from flask import Flask, send_from_directory
from flask_login import LoginManager
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Добавляем кастомный фильтр nl2br
@app.template_filter('nl2br')
def nl2br_filter(s):
    if s:
        return s.replace('\n', '<br>\n')
    return s

# Инициализация расширений
from models import db
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'
login_manager.login_message_category = 'info'

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_config():
    return dict(config=Config)

# Роут для отдачи статических файлов (опционально)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Импорт маршрутов
from routes import *

if __name__ == '__main__':
    # Проверяем существование статических директорий
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)