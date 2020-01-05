from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *

from app import app
from app.models import *

app.jinja_env.globals['bootstrap_is_hidden_field'] = lambda field: isinstance(field, HiddenField)


class ConfigForm(FlaskForm):
    language = SelectField('Выберите язык программирования:', choices=[('python', 'Python 3'), ('cpp', 'C++')])
    code = TextAreaField('editor')
    data = TextAreaField('data')
    last_exception = TextAreaField('last_exception')
    submit = SubmitField('Начать игру')


class AddBotForm(FlaskForm):
    submit = SubmitField('Добавить бота в текущую игру')


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')

    @staticmethod
    def validate_username(_, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Логин уже занят')
