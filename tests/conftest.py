import pytest
from base64 import b64encode
from passlib.apps import custom_app_context

from extrapypi.app import create_app
from extrapypi.models import Package, User
from extrapypi.extensions import db as _db


@pytest.fixture
def app():
    return create_app(testing=True)


@pytest.fixture
def db(app):

    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username="admin",
        email="email@admin.com",
        password_hash=custom_app_context.hash('admin')
    )
    db.session.add(user)
    db.session.commit()

    return user


@pytest.fixture
def admin_headers(admin_user):
    credentials = "{}:{}".format(admin_user.username, 'admin').encode('ascii')
    encoded = b64encode(credentials)
    return {
        'Authorization': b'Basic ' + encoded,
    }


@pytest.fixture
def packages(db, admin_user):
    package_test = Package(name="test-package")
    package_other = Package(name="other-package")

    package_test.maintainers.append(admin_user)
    package_other.maintainers.append(admin_user)

    db.session.add_all([package_test, package_other])
    db.session.commit()


@pytest.fixture
def test_releases(packages):
    pass
