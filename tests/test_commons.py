import pytest

from extrapypi.commons.packages import get_store, create_package


def test_get_store_errors():
    with pytest.raises(AttributeError):
        get_store('BadStore', {})


def test_create_package_errors(badstore):
    assert create_package("test", "test", badstore) is None
