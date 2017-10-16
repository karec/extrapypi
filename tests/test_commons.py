import pytest

from extrapypi.commons.login import user_loader
from extrapypi.commons.packages import get_store, create_package


def test_get_store_errors():
    with pytest.raises(AttributeError):
        get_store('BadStore', {})


def test_create_package_errors(badstore):
    assert create_package("test", "test", badstore) is None


def test_user_loader(admin_user):
    assert user_loader(admin_user.id).username == admin_user.username
