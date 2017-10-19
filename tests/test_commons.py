import os
import pytest
from flask import Flask
from flask_principal import Permission

from extrapypi.app import configure_app
from extrapypi.commons.filters import tohtml
from extrapypi.commons.login import user_loader
from extrapypi.commons.packages import get_store, create_package


def test_get_store_errors():
    with pytest.raises(AttributeError):
        get_store('BadStore', {})


def test_create_package_errors(app, client, badstore, monkeypatch):
    def pass_permission(obj):
        return True
    monkeypatch.setattr(Permission, 'test', pass_permission)
    with pytest.raises(RuntimeError):
        create_package("test", "test", badstore)


def test_tohtml():
    assert tohtml("*test*") == "<p><em>test</em></p>\n"


def test_user_loader(admin_user):
    assert user_loader(admin_user.id).username == admin_user.username


def test_config(tmpdir, monkeypatch):
    app = Flask(__name__)

    # config with testing
    configure_app(app, testing=True, config=None)
    assert app.config['WTF_CSRF_ENABLED'] is False

    # config with direct link
    f = tmpdir.join("test")
    f.write("MYCONFIG = True")
    configure_app(app, testing=False, config=str(f))
    assert app.config['MYCONFIG'] is True

    # config with env variable
    f = tmpdir.join("byenv")
    f.write("MYENV = True")

    def env_conf(key, default):
        return str(f)

    monkeypatch.setattr(os.environ, 'get', env_conf)
    configure_app(app, False, None)
    assert app.config['MYENV'] is True
