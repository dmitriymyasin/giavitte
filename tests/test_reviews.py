import unittest
import json
from app import app, db
from models import User, Course, Application, Review
from werkzeug.security import generate_password_hash

class ReviewTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # Создаем тестовые данные
            user = User(
                login='testuser',
                password_hash=generate_password_hash('password123'),
                full_name='Тестовый Пользователь',
                phone='8(999)111-22-33',
                email='test@example.com'
            )
            db.session.add(user)
            
            course = Course(
                name='Тестовый курс',
                description='Описание тестового курса'
            )
            db.session.add(course)
            
            db.session.commit()
            
            application = Application(
                user_id=user.id,
                course_id=course.id,
                desired_start_date='2024-12-01',
                payment_method='cash',
                status='completed'
            )
            db.session.add(application)
            db.session.commit()
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_create_review(self):
        with app.app_context():
            # Логинимся
            self.app.post('/login', data={
                'login': 'testuser',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Создаем отзыв
            response = self.app.post('/add_review/1', data={
                'rating': 5,
                'comment': 'Отличный курс!',
                'submit': 'true'
            }, follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Отзыв успешно добавлен', response.data)
    
    def test_view_all_reviews(self):
        response = self.app.get('/reviews')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Отзывы о курсах', response.data)
    
    def test_api_stats(self):
        response = self.app.get('/api/course/1/reviews/stats')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['course_id'], 1)

if __name__ == '__main__':
    unittest.main()