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
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    applications = db.relationship('Application', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    applications = db.relationship('Application', backref='course', lazy=True, cascade='all, delete-orphan')

class Application(db.Model):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    desired_start_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # Для SQLite используем String вместо Enum
    status = db.Column(db.String(20), default='new', index=True)  # Для SQLite используем String вместо Enum
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    review = db.relationship('Review', backref='application', uselist=False, lazy=True, cascade='all, delete-orphan')
    status_history = db.relationship('ApplicationStatusHistory', backref='application', lazy=True, cascade='all, delete-orphan')
    
    __table_args__ = (
        db.CheckConstraint("payment_method IN ('cash', 'bank_transfer')", name='check_payment_method'),
        db.CheckConstraint("status IN ('new', 'in_progress', 'completed')", name='check_status'),
    )

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False, unique=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.CheckConstraint('rating >= 1 AND rating <= 5', name='check_rating_range'),
    )

class ApplicationStatusHistory(db.Model):
    __tablename__ = 'application_status_history'
    
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False, index=True)
    old_status = db.Column(db.String(20))  # Для SQLite используем String вместо Enum
    new_status = db.Column(db.String(20), nullable=False)  # Для SQLite используем String вместо Enum
    changed_by = db.Column(db.String(50), default='Admin')
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        db.CheckConstraint("old_status IN ('new', 'in_progress', 'completed')", name='check_old_status'),
        db.CheckConstraint("new_status IN ('new', 'in_progress', 'completed')", name='check_new_status'),
    )

class ReviewStats(db.Model):
    """Статистика отзывов для курсов"""
    __tablename__ = 'review_stats'
    
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    total_reviews = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float, default=0.0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    course = db.relationship('Course', backref=db.backref('stats', uselist=False))