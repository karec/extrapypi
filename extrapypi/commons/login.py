"""Module handling all Flask-Login logic and handlers
"""
from passlib.apps import custom_app_context

from extrapypi.models import User


def user_loader(user_id):
    return User.query.get(user_id)


def load_user_from_request(request):
    if request.authorization is None:
        return None
    username = request.authorization.get('username')
    password = request.authorization.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not custom_app_context.verify(password, user.password_hash):
        return None
    return user
