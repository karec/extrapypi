"""Views for dashboard
"""
import logging
from flask import Blueprint, render_template

from extrapypi.models import Package


log = logging.getLogger("extrapypi")


blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@blueprint.route('/', methods=['GET'])
def index():
    """Dashboard index, listing packages
    """
    packages = Package.query.all()
    return render_template("dashboard/index.html", packages=packages)
