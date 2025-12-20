# routes.py
from flask import render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy import or_
import re

from app import app
from models import db, User, BookCard, AdminAction
from forms import RegistrationForm, LoginForm, BookCardForm, AdminActionForm
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
        
        # Проверка формата логина (кириллица и цифры)
        if not re.match(r'^[а-яА-ЯёЁ0-9]+$', form.login.data):
            flash('Логин должен содержать только кириллицу и цифры', 'danger')
            return render_template('register.html', form=form)
        
        # Проверка формата телефона
        if not re.match(Config.PHONE_PATTERN, form.phone.data):
            flash('Формат телефона: +7(XXX)-XXX-XX-XX', 'danger')
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
            return redirect(url_for('my_cards'))
        else:
            flash('Неверный логин или пароль', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы', 'info')
    return redirect(url_for('index'))

@app.route('/my_cards')
@login_required
def my_cards():
    # Активные карточки
    active_cards = BookCard.query.filter_by(
        user_id=current_user.id,
        status=BookCard.status.in_(['pending', 'approved'])
    ).order_by(BookCard.created_at.desc()).all()
    
    # Архивные карточки (отклоненные или удаленные)
    archived_cards = BookCard.query.filter_by(
        user_id=current_user.id,
        status=BookCard.status.in_(['rejected', 'archived'])
    ).order_by(BookCard.updated_at.desc()).all()
    
    return render_template('my_cards.html', 
                         active_cards=active_cards,
                         archived_cards=archived_cards)

@app.route('/create_card', methods=['GET', 'POST'])
@login_required
def create_card():
    form = BookCardForm()
    
    if form.validate_on_submit():
        # Создаем карточку книги
        card = BookCard(
            user_id=current_user.id,
            author=form.author.data,
            title=form.title.data,
            card_type=form.card_type.data,
            publisher=form.publisher.data if form.publisher.data else None,
            year=form.year.data if form.year.data else None,
            binding=form.binding.data if form.binding.data else None,
            condition=form.condition.data if form.condition.data else None,
            status='pending'
        )
        
        db.session.add(card)
        db.session.commit()
        
        flash('Карточка успешно создана и отправлена на модерацию!', 'success')
        return redirect(url_for('my_cards'))
    
    return render_template('create_card.html', form=form)

@app.route('/delete_card/<int:card_id>', methods=['POST'])
@login_required
def delete_card(card_id):
    card = BookCard.query.get_or_404(card_id)
    
    # Проверяем, что карточка принадлежит пользователю
    if card.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Доступ запрещен'}), 403
    
    # Архивируем карточку вместо удаления
    card.status = 'archived'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Карточка перемещена в архив'})

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    form = LoginForm()
    
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
    
    # Все карточки на модерации
    pending_cards = BookCard.query.filter_by(status='pending')\
        .order_by(BookCard.created_at.desc()).all()
    
    # Одобренные карточки
    approved_cards = BookCard.query.filter_by(status='approved')\
        .order_by(BookCard.updated_at.desc()).limit(20).all()
    
    return render_template('admin.html', 
                         pending_cards=pending_cards,
                         approved_cards=approved_cards)

@app.route('/admin/card/<int:card_id>', methods=['GET', 'POST'])
def admin_card_detail(card_id):
    if not session.get('is_admin'):
        return redirect(url_for('admin_login'))
    
    card = BookCard.query.get_or_404(card_id)
    form = AdminActionForm()
    
    if form.validate_on_submit():
        # Сохраняем старое состояние
        old_status = card.status
        
        if form.action.data == 'approve':
            card.status = 'approved'
            card.rejection_reason = None
            action_type = 'approve'
            reason = None
            flash_message = 'Карточка одобрена и опубликована'
        else:
            card.status = 'rejected'
            card.rejection_reason = form.reason.data
            action_type = 'reject'
            reason = form.reason.data
            flash_message = 'Карточка отклонена'
        
        # Логируем действие администратора
        action = AdminAction(
            card_id=card_id,
            admin_login=session.get('admin_login', 'admin'),
            action=action_type,
            reason=reason
        )
        
        db.session.add(action)
        db.session.commit()
        
        flash(flash_message, 'success')
        return redirect(url_for('admin_panel'))
    
    return render_template('admin_card_detail.html', card=card, form=form)

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