import os
import pytest
from app import app

def test_static_files():
    """Тест наличия статических файлов"""
    static_dir = 'static'
    
    # Проверяем существование директорий
    assert os.path.exists(static_dir)
    assert os.path.exists(os.path.join(static_dir, 'css'))
    assert os.path.exists(os.path.join(static_dir, 'js'))
    assert os.path.exists(os.path.join(static_dir, 'img'))
    
    # Проверяем наличие основных файлов
    assert os.path.exists(os.path.join(static_dir, 'css', 'bootstrap.min.css'))
    assert os.path.exists(os.path.join(static_dir, 'css', 'style.css'))
    assert os.path.exists(os.path.join(static_dir, 'js', 'bootstrap.bundle.min.js'))
    assert os.path.exists(os.path.join(static_dir, 'js', 'validation.js'))
    assert os.path.exists(os.path.join(static_dir, 'js', 'slider.js'))

def test_templates():
    """Тест наличия шаблонов"""
    templates_dir = 'templates'
    
    # Проверяем существование директории
    assert os.path.exists(templates_dir)
    
    # Проверяем наличие основных шаблонов
    required_templates = [
        'base.html',
        'index.html',
        'login.html',
        'register.html',
        'profile.html',
        'create_application.html',
        'admin.html',
        '404.html',
        '500.html'
    ]
    
    for template in required_templates:
        assert os.path.exists(os.path.join(templates_dir, template))

def test_config_files():
    """Тест наличия конфигурационных файлов"""
    required_files = [
        'requirements.txt',
        'config.py',
        '.env',
        'run.sh'
    ]
    
    for file in required_files:
        assert os.path.exists(file)

def test_sql_files():
    """Тест наличия SQL файлов"""
    sql_dir = 'sql'
    
    if os.path.exists(sql_dir):
        required_sql_files = [
            'schema.sql',
            'data.sql',
            'triggers.sql'
        ]
        
        for sql_file in required_sql_files:
            assert os.path.exists(os.path.join(sql_dir, sql_file))

def test_application_structure():
    """Тест структуры приложения"""
    # Проверяем наличие основных модулей Python
    required_py_files = [
        'app.py',
        'models.py',
        'routes.py',
        'forms.py',
        'init_database.py'
    ]
    
    for py_file in required_py_files:
        assert os.path.exists(py_file)

def test_static_content(client):
    """Тест доступности статических файлов через веб-сервер"""
    with app.test_client() as client:
        # Проверяем CSS файлы
        response = client.get('/static/css/style.css')
        assert response.status_code == 200
        assert 'text/css' in response.content_type
        
        # Проверяем JS файлы
        response = client.get('/static/js/validation.js')
        assert response.status_code == 200
        assert 'application/javascript' in response.content_type

if __name__ == '__main__':
    pytest.main([__file__, '-v'])