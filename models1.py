# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи
    cards = db.relationship('BookCard', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)

class BookCard(db.Model):
    __tablename__ = 'book_cards'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Обязательные поля
    author = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    card_type = db.Column(db.Enum('share', 'want'), nullable=False)  # share - готов поделиться, want - хочу в библиотеку
    
    # Дополнительные поля (не обязательные)
    publisher = db.Column(db.String(200))
    year = db.Column(db.Integer)
    binding = db.Column(db.String(50))  # переплет
    condition = db.Column(db.String(100))  # состояние книги
    
    # Статус карточки
    status = db.Column(db.Enum('pending', 'approved', 'rejected', 'archived'), default='pending', index=True)
    
    # Для отклоненных карточек
    rejection_reason = db.Column(db.Text)
    
    # Дата и время
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Индексы для быстрого поиска
    __table_args__ = (
        db.Index('idx_author_title', 'author', 'title'),
        db.Index('idx_status_user', 'status', 'user_id'),
    )

class AdminAction(db.Model):
    __tablename__ = 'admin_actions'
    
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('book_cards.id'), nullable=False)
    admin_login = db.Column(db.String(50), nullable=False)
    action = db.Column(db.Enum('approve', 'reject'), nullable=False)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Связь
    card = db.relationship('BookCard', backref='actions')