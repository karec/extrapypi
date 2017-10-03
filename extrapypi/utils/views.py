"""Utils views
"""
from flask import Blueprint


blueprint = Blueprint('utils', __name__)


@blueprint.route('/ping', methods=['GET'])
def ping():
    """Simple view used to monitor extrapypi server"""
    return "pong", 200
