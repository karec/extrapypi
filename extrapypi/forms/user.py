"""WTForms forms class declaration for users
"""
from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, EqualTo
from wtforms import StringField, BooleanField, PasswordField, SelectField


class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    role = SelectField('role', choices=[])
    is_active = BooleanField('active')


class UserCreateForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    role = SelectField('role', choices=[])
    password = PasswordField('password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat password')
    is_active = BooleanField('active')


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember me')


class PasswordForm(FlaskForm):
    current = PasswordField('Current password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(),
        EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat password')
