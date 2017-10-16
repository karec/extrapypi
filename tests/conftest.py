import os
import shutil
import pytest
from base64 import b64encode
from passlib.apps import custom_app_context
from werkzeug.datastructures import FileStorage

from extrapypi.app import create_app
from extrapypi.extensions import db as _db
from extrapypi.models import Package, User, Release


@pytest.fixture
def app(tmpdir):
    app = create_app(testing=True)
    app.config['STORAGE'] = 'LocalStorage'
    app.config['STORAGE_PARAMS'] = {
        'packages_root': str(tmpdir)
    }
    return app


@pytest.fixture
def db(app):

    _db.app = app
    _db.create_all()

    yield _db

    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User.query.filter_by(username='admin').first()

    if user is None:
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
def users(db):
    users = []
    for i in range(0, 10):
        u = User(
            username="user_%d" % i,
            email="user_%d@mail.com" % i,
            password_hash=custom_app_context.hash('admin')
        )
        users.append(u)

    db.session.add_all(users)
    db.session.commit()

    return users


@pytest.fixture
def user(db):
    u = User(
        username="test-user",
        email="user_test@mail.com",
        password_hash=custom_app_context.hash('admin')
    )
    db.session.add(u)
    db.session.commit()
    return u


@pytest.fixture
def werkzeug_file(tmpdir):
    release = tmpdir.mkdir('uploads').join('testupload-0.1.tar.gz')
    release.write("test-upload")

    f = FileStorage(
        stream=release.open('rb'),
        filename="test-0.1.tar.gz"
    )
    return f


@pytest.fixture
def packages(db, admin_user, app):
    package_test = Package(name="test-package")
    package_other = Package(name="other-package")

    package_test.maintainers.append(admin_user)
    package_other.maintainers.append(admin_user)

    db.session.add_all([package_test, package_other])
    db.session.commit()

    packages = [package_test, package_other]
    return packages


@pytest.fixture
def packages_dirs(db, admin_user, app):
    pdir = app.config['STORAGE_PARAMS']['packages_root']

    package_test = Package(name="test-package")
    os.mkdir(os.path.join(pdir, 'test-package'))

    package_other = Package(name="other-package")
    os.mkdir(os.path.join(pdir, 'other-package'))

    package_test.maintainers.append(admin_user)
    package_other.maintainers.append(admin_user)

    db.session.add_all([package_test, package_other])
    db.session.commit()

    packages = [package_test, package_other]
    yield packages

    shutil.rmtree(os.path.join(pdir, 'test-package'))
    shutil.rmtree(os.path.join(pdir, 'other-package'))


@pytest.fixture
def releases(db, packages, tmpdir):
    for p in packages:
        r = Release(
            description="test",
            download_url="http://test",
            home_page="http://test",
            version="0.1",
            keywords="test,other",
            md5_digest="badmd5"
        )
        r.package = p
        db.session.add(r)

    db.session.commit()


@pytest.fixture
def releases_dirs(app, db, packages_dirs, tmpdir):
    pdir = app.config['STORAGE_PARAMS']['packages_root']
    for p in packages_dirs:
        r = Release(
            description="test",
            download_url="http://test",
            home_page="http://test",
            version="0.1",
            keywords="test,other",
            md5_digest="badmd5"
        )
        r.package = p
        with open(os.path.join(pdir, p.name, p.name + '-0.1.tar.gz'), 'w') as f:
            f.write("insidepackage")
        db.session.add(r)

    db.session.commit()
