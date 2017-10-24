"""Module handling all Flask-Login logic and handlers
"""
from flask import current_app as app
from passlib.apps import custom_app_context
from flask_principal import (
    identity_loaded,
    RoleNeed,
    UserNeed,
    Identity,
    identity_changed
)

from extrapypi.models import User


def user_loader(user_id):
    """Default user handler, from Flask-Login documentation
    """
    return User.query.get(user_id)


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    """Load rights for flask-principal

    Handle only role need and user need
    """
    user = User.query.get(identity.id)
    identity.user = user

    identity.provides.add(UserNeed(user.id))
    if user.role:
        identity.provides.add(RoleNeed(user.role))


def load_user_from_request(request):
    """Used to identify a request from pip or twine
    when downloading / uploading packages and releases
    """
    if request.authorization is None:
        return None
    username = request.authorization.get('username')
    password = request.authorization.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not custom_app_context.verify(password, user.password_hash):
        return None

    identity_changed.send(
        app._get_current_object(),
        identity=Identity(user.id)
    )

    return user
