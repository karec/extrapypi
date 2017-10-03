import pytest

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
def packages(db):
    user = User(
        username="admin",
        email="email@admin",
        password_hash="badhash"
    )

    package_test = Package(name="test-package")
    package_other = Package(name="other-package")

    package_test.maintainers.append(user)
    package_other.maintainers.append(user)

    db.session.add_all([user, package_test, package_other])
    db.session.commit()


@pytest.fixture
def test_releases(packages):
    pass
