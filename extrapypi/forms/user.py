from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from wtforms import StringField, BooleanField


class UserForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired()])
    is_active = BooleanField('active')
