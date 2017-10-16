"""Views for self-user management

TODO : before we can make it here, we need to implement permissions
"""
import logging
from flask import Blueprint

log = logging.getLogger("extrapypi")


blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/', methods=['GET', 'POST'])
def update_user():
    pass


@blueprint.route('/password', methods=['GET', 'POST'])
def update_password():
    pass
