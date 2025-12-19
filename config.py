import os
from dotenv import load_dotenv
import sys

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # Используем SQLite вместо MySQL
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', f'sqlite:///{os.path.join(basedir, "vitte.db")}')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_LOGIN = os.getenv('ADMIN_LOGIN', 'Admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'KorokNET')
    
    # Настройки для валидации
    MIN_LOGIN_LENGTH = 6
    MIN_PASSWORD_LENGTH = 8
    PHONE_PATTERN = r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$'