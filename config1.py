# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-for-book-exchange')
    
    # Используем SQLite для простоты
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', f'sqlite:///{os.path.join(basedir, "bookexchange.db")}')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Админские учетные данные
    ADMIN_LOGIN = 'admin'
    ADMIN_PASSWORD = 'bookworm'
    
    # Настройки валидации
    MIN_LOGIN_LENGTH = 6
    MIN_PASSWORD_LENGTH = 6
    PHONE_PATTERN = r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$'