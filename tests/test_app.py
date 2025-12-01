import pytest
from app import app, db
from models import User, Course
from flask import url_for

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            
            # Создание тестовых данных
            course = Course(name='Тестовый курс', description='Описание')
            db.session.add(course)
            db.session.commit()
            
        yield client

def test_index_page(client):
    """Тест главной страницы"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Корочки.есть' in response.data

def test_registration_page(client):
    """Тест страницы регистрации"""
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Регистрация' in response.data

def test_login_page(client):
    """Тест страницы входа"""
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Вход в систему' in response.data

def test_admin_login_page(client):
    """Тест страницы входа администратора"""
    response = client.get('/admin/login')
    assert response.status_code == 200
    assert b'администратора' in response.data

def test_user_registration(client):
    """Тест регистрации пользователя"""
    data = {
        'login': 'testuser',
        'password': 'testpassword123',
        'confirm_password': 'testpassword123',
        'full_name': 'Тестовый Пользователь',
        'phone': '8(999)888-77-66',
        'email': 'test@example.com'
    }
    
    response = client.post('/register', data=data, follow_redirects=True)
    assert response.status_code == 200
    
    # Проверяем, что пользователь создан
    with app.app_context():
        user = User.query.filter_by(login='testuser').first()
        assert user is not None
        assert user.email == 'test@example.com'

def test_duplicate_registration(client):
    """Тест регистрации с существующим логином"""
    # Первая регистрация
    data1 = {
        'login': 'duplicate',
        'password': 'password123',
        'confirm_password': 'password123',
        'full_name': 'Первый Пользователь',
        'phone': '8(111)222-33-44',
        'email': 'first@example.com'
    }
    client.post('/register', data=data1)
    
    # Вторая регистрация с тем же логином
    data2 = {
        'login': 'duplicate',
        'password': 'password456',
        'confirm_password': 'password456',
        'full_name': 'Второй Пользователь',
        'phone': '8(555)666-77-88',
        'email': 'second@example.com'
    }
    
    response = client.post('/register', data=data2, follow_redirects=True)
    assert b'уже существует' in response.data

def test_invalid_registration_data(client):
    """Тест регистрации с невалидными данными"""
    # Короткий пароль
    data = {
        'login': 'shortpass',
        'password': '123',
        'confirm_password': '123',
        'full_name': 'Тест Короткий',
        'phone': '8(999)888-77-66',
        'email': 'short@example.com'
    }
    
    response = client.post('/register', data=data)
    assert b'минимум 8 символов' in response.data
    
    # Неправильный формат телефона
    data['password'] = 'validpassword123'
    data['confirm_password'] = 'validpassword123'
    data['phone'] = 'invalid-phone'
    
    response = client.post('/register', data=data)
    assert b'Формат телефона' in response.data

def test_create_application(client):
    """Тест создания заявки (требует аутентификации)"""
    # Сначала регистрируем и логиним пользователя
    reg_data = {
        'login': 'apptest',
        'password': 'apptest123',
        'confirm_password': 'apptest123',
        'full_name': 'Тест Заявки',
        'phone': '8(999)111-22-33',
        'email': 'apptest@example.com'
    }
    client.post('/register', data=reg_data)
    
    # Логин
    login_data = {
        'login': 'apptest',
        'password': 'apptest123'
    }
    client.post('/login', data=login_data, follow_redirects=True)
    
    # Создание заявки
    app_data = {
        'course_name': 'Тестовый курс',
        'desired_start_date': '01.01.2024',
        'payment_method': 'cash'
    }
    
    response = client.post('/create_application', data=app_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'успешно создана' in response.data

if __name__ == '__main__':
    pytest.main([__file__, '-v'])