from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, Regexp

class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[
        DataRequired(message='Логин обязателен'),
        Length(min=6, message='Логин должен содержать минимум 6 символов')
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(message='Пароль обязателен'),
        Length(min=8, message='Пароль должен содержать минимум 8 символов')
    ])
    confirm_password = PasswordField('Подтверждение пароля', validators=[
        DataRequired(message='Подтверждение пароля обязательно')
    ])
    full_name = StringField('ФИО', validators=[
        DataRequired(message='ФИО обязательно')
    ])
    phone = StringField('Телефон', validators=[
        DataRequired(message='Телефон обязателен')
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

class ApplicationForm(FlaskForm):
    course_name = SelectField('Название курса', choices=[
        ('Основы алгоритмизации и программирования', 'Основы алгоритмизации и программирования'),
        ('Основы веб-дизайна', 'Основы веб-дизайна'),
        ('Основы проектирования баз данных', 'Основы проектирования баз данных')
    ], validators=[DataRequired()])
    desired_start_date = StringField('Желаемая дата начала обучения', validators=[
        DataRequired()
    ])
    payment_method = SelectField('Способ оплаты', choices=[
        ('cash', 'Наличными'),
        ('bank_transfer', 'Перевод по номеру телефона')
    ], validators=[DataRequired()])
    submit = SubmitField('Создать заявку')

class ReviewForm(FlaskForm):
    rating = SelectField('Оценка', choices=[
        (5, '5 - Отлично'),
        (4, '4 - Хорошо'),
        (3, '3 - Удовлетворительно'),
        (2, '2 - Плохо'),
        (1, '1 - Очень плохо')
    ], coerce=int, validators=[DataRequired()])
    comment = TextAreaField('Комментарий')
    submit = SubmitField('Добавить отзыв')

class AdminLoginForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')