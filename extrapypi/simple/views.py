"""Views for handling simple index like original pypi
"""
import logging
from flask_login import login_required
from sqlalchemy.orm.exc import NoResultFound
from flask_principal import PermissionDenied
from flask import (
    request,
    render_template,
    Blueprint,
    abort,
    send_file,
    current_app
)

from extrapypi.models import Package
from extrapypi.commons.permissions import installer_permission
from extrapypi.commons.packages import create_release, get_store

log = logging.getLogger("extrapypi")


blueprint = Blueprint('simple', __name__, url_prefix='/simple')


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
@installer_permission.require()
def simple():
    """Simple view index used to list or upload packages

    Used to list packages. Simple index is generated on the fly based
    on SQL data
    """
    if request.method == 'POST':
        action = request.form.get(':action')
        log.info(dict(request.form))
        if action != 'file_upload':
            abort(400, "method not supported")

        log.info("uploading new release")
        try:
            create_release(request.form, current_app.config, request.files)
            return "OK", 200
        except PermissionDenied:
            log.error("Not enough permissions")
            abort(401)
        except Exception:
            log.exception("Cannot upload release")
            abort(400)

    packages = Package.query.all()
    return render_template('simple/simple.html', packages=packages)


@blueprint.route('/<string:package>/', methods=['GET'])
@login_required
@installer_permission.require()
def package_view(package):
    """List all files avaible for a package
    """
    store = get_store(
        current_app.config['STORAGE'],
        current_app.config['STORAGE_PARAMS']
    )
    try:
        package_obj = Package.query.filter_by(name=package).one()
    except NoResultFound:
        abort(404, "package %s does not exists" % package)

    files = store.get_files(package_obj)
    return render_template("simple/package.html",
                           files=files, package=package_obj)


@blueprint.route('/<string:package>/<path:source>', methods=['GET'])
@login_required
@installer_permission.require()
def download_package(package, source):
    """Return a package file from storage
    """
    store = get_store(
        current_app.config['STORAGE'],
        current_app.config['STORAGE_PARAMS']
    )

    try:
        package_obj = Package.query.filter_by(name=package).one()
    except NoResultFound:
        abort(404, "package %s does not exists" % package)

    return send_file(store.get_file(package_obj, source))
