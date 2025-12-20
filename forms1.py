# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Regexp, Optional
import re

class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[
        DataRequired(message='Логин обязателен'),
        Length(min=6, message='Логин должен содержать минимум 6 символов'),
        Regexp(r'^[а-яА-ЯёЁ0-9]+$', message='Логин должен содержать только кириллицу и цифры')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Пароль обязателен'),
        Length(min=6, message='Пароль должен содержать минимум 6 символов')
    ])
    confirm_password = PasswordField('Подтверждение пароля', validators=[
        DataRequired(message='Подтверждение пароля обязательно')
    ])
    full_name = StringField('ФИО', validators=[
        DataRequired(message='ФИО обязательно'),
        Regexp(r'^[А-Яа-яЁё\s]+$', message='ФИО должно содержать только кириллические символы и пробелы')
    ])
    phone = StringField('Телефон', validators=[
        DataRequired(message='Телефон обязателен'),
        Regexp(r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$', message='Формат: +7(XXX)-XXX-XX-XX')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email обязателен'),
        Email(message='Неверный формат email')
    ])
    submit = SubmitField('Зарегистрироваться')
    
    def validate_confirm_password(self, field):
        if self.password.data != field.data:
            raise ValidationError('Пароли не совпадают')

class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class BookCardForm(FlaskForm):
    author = StringField('Автор книги', validators=[
        DataRequired(message='Автор обязателен'),
        Length(max=200, message='Максимум 200 символов')
    ])
    title = StringField('Название книги', validators=[
        DataRequired(message='Название обязательно'),
        Length(max=200, message='Максимум 200 символов')
    ])
    card_type = RadioField('Тип карточки', choices=[
        ('share', 'Готов поделиться'),
        ('want', 'Хочу в свою библиотеку')
    ], validators=[DataRequired(message='Выберите тип карточки')])
    
    # Необязательные поля
    publisher = StringField('Издательство', validators=[
        Optional(),
        Length(max=200, message='Максимум 200 символов')
    ])
    year = IntegerField('Год издания', validators=[Optional()])
    binding = StringField('Переплет', validators=[
        Optional(),
        Length(max=50, message='Максимум 50 символов')
    ])
    condition = StringField('Состояние книги', validators=[
        Optional(),
        Length(max=100, message='Максимум 100 символов')
    ])
    
    submit = SubmitField('Отправить на рассмотрение')

class AdminActionForm(FlaskForm):
    action = RadioField('Действие', choices=[
        ('approve', 'Опубликовать карточку'),
        ('reject', 'Отклонить публикацию')
    ], validators=[DataRequired()])
    reason = TextAreaField('Причина отклонения', validators=[
        Optional(),
        Length(max=500, message='Максимум 500 символов')
    ])
    submit = SubmitField('Выполнить действие')
    
    def validate_reason(self, field):
        if self.action.data == 'reject' and not field.data:
            raise ValidationError('Укажите причину отклонения при отказе')