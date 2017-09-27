"""
Extrapypi app
=============

Used to create application. This can be imported for wsgi file for uwsgi or gunicorn.

By default, application will look for a EXTRAPYPI_CONFIG env variable to load configuration file,
but you can also pass a config parameter.
The configuration files are loaded in the following order :

* Load default configuration
* If testing is set to True, load config_test.py and nothing else
* If config parameter is not None, use it and don't load env variable config file
* If config parameter is None, try to load env variable

You can create a wsgi file like this for running gunicorn or uwsgi :

.. code-block:: python

    from extrapypi.app import create_app

    application = create_app()
"""
import os
from flask import Flask

from extrapypi import views


def create_app(testing=False, config=None):
    """Main application factory
    """
    app = Flask('extra-pypi')

    configure_app(app, testing, config)
    register_views(app)

    return app


def configure_app(app, testing, config):
    """Set configuration for application"""
    app.config.from_object('extrapypi.config')

    env_config = os.environ.get('EXTRAPYPI_CONFIG', None)

    if testing is True:
        app.config.from_object('extrapypi.test_config')
    elif config is not None:
        app.config.from_pyfile(config)
    elif env_config is not None:
        app.config.from_pyfile(config)


def register_views(app):
    """Register all views for application"""
    app.add_url_rule('/ping', 'ping', views.ping, methods=['GET'])

    app.add_url_rule('/simple/', 'simple', views.simple, methods=['GET', 'POST'])
    app.add_url_rule(
        '/simple/<string:package>/',
        'package-view',
        views.package_view,
        methods=['GET']
    )
    app.add_url_rule(
        '/simple/<string:package>/<path:archive>',
        'download-package',
        views.download_package,
        methods=['GET']
    )
