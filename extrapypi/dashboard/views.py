"""Views for dashboard
"""
import logging
from sqlalchemy.orm.exc import NoResultFound
from flask import Blueprint, render_template, abort, request,\
    current_app as app, flash

from extrapypi.forms.user import UserForm
from extrapypi.commons.packages import get_store
from extrapypi.models import Package, Release, User


log = logging.getLogger("extrapypi")


blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@blueprint.route('/', methods=['GET'])
def index():
    """Dashboard index, listing packages
    """
    packages = Package.query.all()
    return render_template("dashboard/index.html", packages=packages)


@blueprint.route('/search/', methods=['POST'])
def search():
    """Search page
    """
    name = request.form.get('search')
    packages = Package.query.filter(Package.name.ilike('%{}%'.format(name)))
    packages = packages.all()
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
    files = store.get_files(p, release) or []
    releases = [r for r in p.releases if r != release]
    return render_template("dashboard/package_detail.html",
                           release=release,
                           files=files,
                           releases=releases)


@blueprint.route('/<string:package>/<int:release_id>/', methods=['GET'])
def release(package, release_id):
    """Specific release view
    """
    try:
        package = Package.query.filter_by(name=package).one()
        release = Release.query.filter(
            Release.id == release_id,
            Release.package_id == package.id
        ).one()
    except NoResultFound:
        abort(404)

    store = get_store(app.config['STORAGE'], app.config['STORAGE_PARAMS'])
    files = store.get_files(package, release) or []
    releases = [r for r in package.releases if r != release]
    return render_template("dashboard/package_detail.html",
                           release=release,
                           files=files,
                           releases=releases)


@blueprint.route('/users/', methods=['GET'])
def users_list():
    """List user in dashboard
    """
    users = User.query.all()
    return render_template("dashboard/users.html", users=users)


@blueprint.route('/users/<int:user_id>', methods=['GET', 'POST'])
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(request.form, obj=user)
    if request.method == 'POST' and form.validate():
        print(dir(form))
        flash("User updated")
        return "ok"
    return render_template("dashboard/user_detail.html", form=form, user=user)
