"""Views for dashboard
"""
import logging
from passlib.apps import custom_app_context
from sqlalchemy.orm.exc import NoResultFound
from flask_login import login_required, login_user, logout_user
from flask import Blueprint, render_template, abort, request,\
    current_app as app, flash, redirect, url_for

from extrapypi.extensions import csrf, db
from extrapypi.commons.packages import get_store
from extrapypi.models import Package, Release, User
from extrapypi.forms.user import UserForm, UserCreateForm, LoginForm


log = logging.getLogger("extrapypi")


blueprint = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@blueprint.route('/', methods=['GET'])
@login_required
def index():
    """Dashboard index, listing packages
    """
    packages = Package.query.all()
    return render_template("dashboard/index.html", packages=packages)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    """Login view

    Will redirect to dashboard index if login is successful
    """
    form = LoginForm(request.form)

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data

        user = User.query.filter_by(username=username).first()
        if not user or not custom_app_context.verify(pwd, user.password_hash):
            flash("Bad user / password", 'alert-danger')
            return render_template("login.html", form=form)
        login_user(user, remember=form.remember.data)
        return redirect(url_for('dashboard.index'))

    return render_template("login.html", form=form)


@blueprint.route('/logout', methods=['GET'])
def logout():
    """Logout view

    Will redirect to login view
    """
    logout_user()
    return redirect(url_for('dashboard.login'))


@blueprint.route('/search/', methods=['POST'])
@login_required
@csrf.exempt
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


@blueprint.route('/<string:package>/<int:release_id>', methods=['GET'])
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


@blueprint.route('/users/create', methods=['GET', 'POST'])
def create_user():
    """Create a new user
    """
    form = UserCreateForm(request.form)
    form.role.choices = [(r, r) for r in User.ROLES]

    if form.validate_on_submit():
        u = User(
            username=form.username.data,
            email=form.email.data,
            is_active=form.is_active.data,
            role=form.role.data
        )
        u.password_hash = custom_app_context.hash(form.password.data)

        db.session.add(u)
        db.session.commit()

        flash("User created")
        return redirect(url_for('dashboard.users_list'))
    return render_template("dashboard/user_create.html", form=form)


@blueprint.route('/users/<int:user_id>', methods=['GET', 'POST'])
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(request.form, obj=user)
    form.role.choices = [(r, r) for r in User.ROLES]

    if form.validate_on_submit():
        flash("User updated")
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for('dashboard.users_list'))

    return render_template("dashboard/user_detail.html", form=form, user=user)


@blueprint.route('/users/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted")
    return redirect(url_for('dashboard.users_list'))
