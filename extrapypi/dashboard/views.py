"""Views for dashboard
"""
import logging
from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, render_template, abort, current_app as app

from extrapypi.models import Package
from extrapypi.commons.packages import get_store


log = logging.getLogger("extrapypi")


blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@blueprint.route('/', methods=['GET'])
def index():
    """Dashboard index, listing packages
    """
    packages = Package.query.all()
    return render_template("dashboard/index.html", packages=packages)


@blueprint.route('/<string:package>/', methods=['GET'])
def package(package):
    """Package detail view
    """
    try:
        p = Package.query.filter_by(name=package).one()
    except NoResultFound:
        abort(404)

    release = p.latest_release
    store = get_store(app.config['STORAGE'], app.config['STORAGE_PARAMS'])
    files = store.get_files(p, release)
    return render_template("dashboard/package_detail.html",
                           release=release,
                           files=files,
                           releases=p.releases)
