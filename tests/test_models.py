"""Test basics behaviors of models
"""
import pytest

from extrapypi import models


def test_user():
    """Test user features"""
    u = models.User(
        username='myuser',
        email='mymail@mail.com',
        password_hash='badhash'
    )
    assert u.is_authenticated is True
    assert u.is_anonymous is False
    assert u.get_id() == 'None'
    assert str(u) == "<User myuser>"

    with pytest.raises(Exception):
        u.role = 'badrole'


def test_package():
    """Test package features"""
    p = models.Package(
        name='p',
        summary='summary'
    )
    assert str(p) == '<Package p>'
    assert p.latest_release is None


def test_release():
    """Test release features"""
    p = models.Package(
        name='p',
        summary='summary'
    )

    r = models.Release(
        description='test',
        version='1.0',
        package=p
    )
    assert str(r) == '<Release 1.0 for package p>'
