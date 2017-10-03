"""Views for handling simple index like original pypi
"""
import pprint
import logging
from flask_login import login_required
from flask import request, render_template, Blueprint, abort, current_app

from extrapypi.models import Package

log = logging.getLogger("extrapypi")


blueprint = Blueprint('simple', __name__, url_prefix='/simple')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def simple():
    """Simple view index used only on GET requests

    Used to list packages
    """
    if request.method == 'POST':
        log.debug("New release")
        action = request.form.get(':action')
        if action == 'register':
            abort(410, "old style pre-register not supported")
        elif action == 'file_upload':
            pass
        else:
            abort(400, "action not supported")
        log.debug(pprint.pformat(dict(request.form)))
    else:
        packages = Package.query.all()
        return render_template('simple/simple.html', packages=packages)
        log.debug("install")
    return "test-package<br />other-package"


@blueprint.route('/<string:package>/', methods=['GET'])
def package_view(package):
    log.debug("trying to view package")
    log.debug(request)
    log.debug(request.args)
    return "extrapypi-0.1.tar.gz"


@blueprint.route('/<string:package>/<path:archive>', methods=['GET'])
def download_package(package, archive):
    return "ok"
