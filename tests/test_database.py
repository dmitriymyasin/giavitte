import pytest
from app import app, db
from models import User, Course, Application, Review
import bcrypt

@pytest.fixture
def app_context():
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app

def test_user_creation():
    """Тест создания пользователя"""
    user = User(
        login='testuser',
        full_name='Тестовый Пользователь',
        phone='8(999)888-77-66',
        email='test@example.com'
    )
    user.set_password('testpassword')
    
    assert user.login == 'testuser'
    assert user.check_password('testpassword')
    assert not user.check_password('wrongpassword')
    assert user.email == 'test@example.com'

def test_course_creation():
    """Тест создания курса"""
    course = Course(
        name='Тестовый курс',
        description='Описание тестового курса'
    )
    
    assert course.name == 'Тестовый курс'
    assert course.description == 'Описание тестового курса'

def test_application_creation(app_context):
    """Тест создания заявки"""
    with app_context:
        # Создаем пользователя
        user = User(
            login='appuser',
            full_name='Пользователь Заявки',
            phone='8(111)222-33-44',
            email='app@example.com'
        )
        user.set_password('password')
        db.session.add(user)
        
        # Создаем курс
        course = Course(name='Курс для заявки', description='Описание')
        db.session.add(course)
        db.session.commit()
        
        # Создаем заявку
        application = Application(
            user_id=user.id,
            course_id=course.id,
            desired_start_date='2024-01-01',
            payment_method='cash',
            status='new'
        )
        
        db.session.add(application)
        db.session.commit()
        
        # Проверяем
        saved_app = Application.query.first()
        assert saved_app.user_id == user.id
        assert saved_app.course_id == course.id
        assert saved_app.payment_method == 'cash'
        assert saved_app.status == 'new'

def test_review_creation(app_context):
    """Тест создания отзыва"""
    with app_context:
        # Создаем пользователя
        user = User(
            login='reviewuser',
            full_name='Пользователь Отзыва',
            phone='8(555)666-77-88',
            email='review@example.com'
        )
        user.set_password('password')
        db.session.add(user)
        
        # Создаем курс
        course = Course(name='Курс для отзыва', description='Описание')
        db.session.add(course)
        
        # Создаем заявку
        application = Application(
            user_id=user.id,
            course_id=course.id,
            desired_start_date='2024-01-01',
            payment_method='bank_transfer',
            status='completed'
        )
        db.session.add(application)
        db.session.commit()
        
        # Создаем отзыв
        review = Review(
            user_id=user.id,
            application_id=application.id,
            rating=5,
            comment='Отличный курс!'
        )
        db.session.add(review)
        db.session.commit()
        
        # Проверяем
        saved_review = Review.query.first()
        assert saved_review.user_id == user.id
        assert saved_review.application_id == application.id
        assert saved_review.rating == 5
        assert saved_review.comment == 'Отличный курс!'

def test_user_relationships(app_context):
    """Тест связей между таблицами"""
    with app_context:
        # Создаем пользователя
        user = User(
            login='reluser',
            full_name='Тест Связей',
            phone='8(777)888-99-00',
            email='rel@example.com'
        )
        user.set_password('password')
        db.session.add(user)
        
        # Создаем курс
        course = Course(name='Курс Связей', description='Описание')
        db.session.add(course)
        db.session.commit()
        
        # Создаем несколько заявок
        for i in range(3):
            application = Application(
                user_id=user.id,
                course_id=course.id,
                desired_start_date=f'2024-0{i+1}-01',
                payment_method='cash',
                status='new'
            )
            db.session.add(application)
        
        db.session.commit()
        
        # Проверяем связи
        assert len(user.applications) == 3
        assert user.applications[0].course.name == 'Курс Связей'
        assert course.applications[0].user.login == 'reluser'

def test_password_hashing():
    """Тест хеширования паролей"""
    password = 'MySecurePassword123'
    user = User()
    user.set_password(password)
    
    # Проверяем, что пароль корректно проверяется
    assert user.check_password(password)
    assert not user.check_password('WrongPassword')
    
    # Проверяем, что хеши разные для разных соли
    user2 = User()
    user2.set_password(password)
    assert user.password_hash != user2.password_hash

if __name__ == '__main__':
    pytest.main([__file__, '-v'])