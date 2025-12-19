from flask import Flask, render_template
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

# Создаем таблицы при запуске приложения
with app.app_context():
    db.create_all()

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

# Импорт маршрутов
from routes import *

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)