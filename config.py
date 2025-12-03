import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'mysql+pymysql://root:HfgFGty217GF@localhost/vitte')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_LOGIN = os.getenv('ADMIN_LOGIN', 'Admin')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'KorokNET')
    
    # Настройки для валидации
    MIN_LOGIN_LENGTH = 6
    MIN_PASSWORD_LENGTH = 8
    PHONE_PATTERN = r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$'