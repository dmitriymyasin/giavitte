from flask import render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import or_
import re

from app import app
from models import db, User, Course, Application, Review, ApplicationStatusHistory
from forms import RegistrationForm, LoginForm, ApplicationForm, ReviewForm, AdminLoginForm
from config import Config

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Проверяем уникальность логина и email
        existing_user = User.query.filter(
            or_(User.login == form.login.data, User.email == form.email.data)
        ).first()
        
        if existing_user:
            if existing_user.login == form.login.data:
                flash('Пользователь с таким логином уже существует', 'danger')
            else:
                flash('Пользователь с таким email уже существует', 'danger')
            return render_template('register.html', form=form)
        
        # Проверка формата логина
        if not re.match(r'^[a-zA-Z0-9]+$', form.login.data):
            flash('Логин должен содержать только латинские буквы и цифры', 'danger')
            return render_template('register.html', form=form)
        
        # Проверка формата ФИО
        if not re.match(r'^[А-Яа-яЁё\s]+$', form.full_name.data):
            flash('ФИО должно содержать только кириллические символы и пробелы', 'danger')
            return render_template('register.html', form=form)
        
        # Проверка формата телефона
        if not re.match(r'^8\(\d{3}\)\d{3}-\d{2}-\d{2}$', form.phone.data):
            flash('Формат телефона: 8(XXX)XXX-XX-XX', 'danger')
            return render_template('register.html', form=form)
        
        # Создаем нового пользователя
        user = User(
            login=form.login.data,
            full_name=form.full_name.data,
            phone=form.phone.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешно завершена! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Неверный логин или пароль', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.created_at.desc()).all()
    return render_template('profile.html', applications=applications)

@app.route('/create_application', methods=['GET', 'POST'])
@login_required
def create_application():
    form = ApplicationForm()
    
    if form.validate_on_submit():
        # Находим курс по имени
        course = Course.query.filter_by(name=form.course_name.data).first()
        if not course:
            flash('Выбранный курс не найден', 'danger')
            return render_template('create_application.html', form=form)
        
        # Преобразуем дату
        try:
            start_date = datetime.strptime(form.desired_start_date.data, '%d.%m.%Y').date()
        except ValueError:
            flash('Неверный формат даты. Используйте ДД.ММ.ГГГГ', 'danger')
            return render_template('create_application.html', form=form)
        
        # Создаем заявку
        application = Application(
            user_id=current_user.id,
            course_id=course.id,
            desired_start_date=start_date,
            payment_method=form.payment_method.data,
            status='new'
        )
        
        db.session.add(application)
        db.session.commit()
        
        flash('Заявка успешно создана!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('create_application.html', form=form)

@app.route('/add_review/<int:application_id>', methods=['GET', 'POST'])
@login_required
def add_review(application_id):
    application = Application.query.get_or_404(application_id)
    
    # Проверяем, что заявка принадлежит пользователю и завершена
    if application.user_id != current_user.id:
        flash('Доступ запрещен', 'danger')
        return redirect(url_for('profile'))
    
    if application.status != 'completed':
        flash('Отзыв можно оставить только после завершения курса', 'warning')
        return redirect(url_for('profile'))
    
    if application.review:
        flash('Вы уже оставили отзыв для этой заявки', 'info')
        return redirect(url_for('profile'))
    
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(
            user_id=current_user.id,
            application_id=application_id,
            rating=int(form.rating.data),
            comment=form.comment.data
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Отзыв успешно добавлен!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('add_review.html', form=form, application=application)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()
    
    if form.validate_on_submit():
        if (form.login.data == Config.ADMIN_LOGIN and 
            form.password.data == Config.ADMIN_PASSWORD):
            session['is_admin'] = True
            flash('Вы вошли как администратор', 'success')
            return redirect(url_for('admin_panel'))
        else:
            flash('Неверные учетные данные администратора', 'danger')
    
    return render_template('admin_login.html', form=form)

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    flash('Вы вышли из панели администратора', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_panel():
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    applications = Application.query.order_by(Application.created_at.desc()).all()
    return render_template('admin.html', applications=applications)

@app.route('/admin/update_status/<int:application_id>', methods=['POST'])
def update_application_status(application_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Доступ запрещен'}), 403
    
    application = Application.query.get_or_404(application_id)
    new_status = request.json.get('status')
    
    if new_status not in ['new', 'in_progress', 'completed']:
        return jsonify({'success': False, 'message': 'Неверный статус'}), 400
    
    old_status = application.status
    application.status = new_status
    
    # Логируем изменение статуса
    history = ApplicationStatusHistory(
        application_id=application_id,
        old_status=old_status,
        new_status=new_status,
        changed_by='Admin'
    )
    
    db.session.add(history)
    db.session.commit()
    
    return jsonify({'success': True, 'new_status': new_status})

@app.route('/admin/get_history/<int:application_id>', methods=['GET'])
def get_application_history(application_id):
    if not session.get('is_admin'):
        return jsonify({'success': False, 'message': 'Доступ запрещен'}), 403
    
    history = ApplicationStatusHistory.query.filter_by(
        application_id=application_id
    ).order_by(ApplicationStatusHistory.changed_at.desc()).all()
    
    history_data = []
    for h in history:
        history_data.append({
            'old_status': h.old_status,
            'new_status': h.new_status,
            'changed_by': h.changed_by,
            'changed_at': h.changed_at.isoformat()
        })
    
    return jsonify({'success': True, 'history': history_data})

@app.route('/check_login')
def check_login():
    login = request.args.get('login', '')
    if not login:
        return jsonify({'available': False})
    
    user = User.query.filter_by(login=login).first()
    return jsonify({'available': user is None})

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500