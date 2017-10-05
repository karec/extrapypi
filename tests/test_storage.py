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


def test_local_storage(app, db, tmpdir, packages):
    """Test local storage"""
    with pytest.raises(RuntimeError):
        ls = LocalStorage()

    package = db.session.query(Package).first()
    r = tmpdir.mkdir(package.name).join(package.name + "-0.1.tar.gz")
    r.write("test-release")

    ls = LocalStorage(packages_root=str(tmpdir))
    assert isinstance(ls.get_files(package), list)
    assert len(ls.get_files(package)) == 1
    assert ls.get_files(package)[0] == package.name + "-0.1.tar.gz"

    f = ls.get_file(package, package.name + "-0.1.tar.gz")
    with open(f, 'r') as f:
        assert f.read() == "test-release"

    # test with bad package
    package.name = "baddir"
    assert ls.get_files(package) is None

    f = ls.get_files(package)
    assert f is None
