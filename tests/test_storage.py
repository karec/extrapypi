import pytest

from extrapypi.models import Package
from extrapypi.storage import LocalStorage
from extrapypi.storage.base import BaseStorage


def test_base_storage():
    """Dummy test, will only test if runtime error
    are correctly returned
    """
    bs = BaseStorage(test=1, other=2)
    assert bs.test == 1
    assert bs.other == 2

    with pytest.raises(NotImplementedError):
        bs.get_files(None, None)

    with pytest.raises(NotImplementedError):
        bs.get_file(None, None)

    with pytest.raises(NotImplementedError):
        bs.create_package(None)

    with pytest.raises(NotImplementedError):
        bs.create_release(None, None)

    with pytest.raises(NotImplementedError):
        bs.delete_release(None, None)

    with pytest.raises(NotImplementedError):
        bs.delete_package(None)


def test_local_storage(app, db, tmpdir, releases, werkzeug_file):
    """Test local storage"""
    with pytest.raises(RuntimeError):
        ls = LocalStorage()

    package = db.session.query(Package).first()

    ls = LocalStorage(packages_root=str(tmpdir))
    assert ls.create_package(package) is True

    r = tmpdir.join(package.name, package.name + "-0.1.tar.gz")
    r.write("test-release")

    assert isinstance(ls.get_files(package), list)
    assert len(ls.get_files(package)) == 1
    assert ls.get_files(package)[0] == package.name + "-0.1.tar.gz"
    assert ls.create_release(package, werkzeug_file) is True
    assert len(ls.get_files(package, package.releases[0])) == 1

    f = ls.get_file(package, package.name + "-0.1.tar.gz")
    with open(f, 'r') as f:
        assert f.read() == "test-release"

    assert ls.delete_release(package, '0.1') is True
    assert ls.delete_package(package) is True

    # test with bad package
    package.name = "baddir"
    ls = LocalStorage(packages_root="bad/dir/location")
    assert ls.get_files(package) is None
    assert ls.create_package(package) is False
    assert ls.create_release(package, werkzeug_file) is False
    assert ls.delete_release(package, '0.1') is False
    assert ls.delete_package(package) is False

    f = ls.get_files(package)
    assert f is None
