"""Views for handling simple index like original pypi
"""
import logging
from flask_login import login_required
from flask import (
    request,
    render_template,
    Blueprint,
    abort,
    send_file,
    current_app
)

from extrapypi.models import Package
from extrapypi.storage import LocalStorage

log = logging.getLogger("extrapypi")


blueprint = Blueprint('simple', __name__, url_prefix='/simple')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def simple():
    """Simple view index used only on GET requests

    Used to list packages
    """
    if request.method == 'POST':
        action = request.form.get(':action')
        if action == 'register':
            abort(410, "old style pre-register not supported")
        elif action == 'file_upload':
            log.info("registering new release")
            pass
        else:
            abort(400, "action not supported")
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


@blueprint.route('/<string:package>/<path:source>', methods=['GET'])
def download_package(package, source):
    storage = LocalStorage(packages_root=current_app.config['PACKAGES_ROOT'])
    return send_file(storage.get_file(package, source))
