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

    app = create_app()

Or add any extra code if needed
"""
import os
import logging.config
from flask import Flask

from extrapypi.commons import login, filters
from extrapypi import simple, utils, dashboard, user
from extrapypi.extensions import db, login_manager, csrf, principal


def create_app(testing=False, config=None):
    """Main application factory
    """

    # the following line ensure that we search templates
    # based on the app file, not working_directory
    tmpl_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'templates'
    )
    static_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'static'
    )

    app = Flask(
        'extra-pypi',
        template_folder=tmpl_path,
        static_folder=static_path
    )
    configure_app(app, testing, config)
    configure_logging(app)
    configure_extensions(app)
    register_blueprints(app)
    register_filters(app)

    return app


def configure_extensions(app):
    """Init all extensions

    For login manager, we also register callbacks here
    """
    db.init_app(app)
    csrf.init_app(app)

    login_manager.init_app(app)
    login_manager.user_loader(login.user_loader)
    login_manager.request_loader(login.load_user_from_request)

    principal.init_app(app)


def register_filters(app):
    """Register additionnal jinja2 filters"""
    app.jinja_env.filters['tohtml'] = filters.tohtml


def configure_app(app, testing, config):
    """Set configuration for application

    Configuration will be loaded in the following order:

    * test_config if testing is True
    * else if config parameter is not None we load it
    * else if env variable for config is set we use it
    """
    app.config.from_object('extrapypi.config')

    env_config = os.environ.get('EXTRAPYPI_CONFIG', None)

    if testing is True:
        app.config.from_object('extrapypi.test_config')
    elif config is not None:
        app.config.from_pyfile(config)
    elif env_config is not None:
        app.config.from_pyfile(env_config)


def register_blueprints(app):
    """Register all views for application"""
    app.register_blueprint(simple.views.blueprint)
    csrf.exempt(simple.views.blueprint)

    app.register_blueprint(utils.views.blueprint)

    if app.config['DASHBOARD'] is True:
        app.register_blueprint(dashboard.views.blueprint)
        app.register_blueprint(user.views.blueprint)


def configure_logging(app):
    """Configure loggers"""
    logging.config.dictConfig(app.config['LOGGING_CONFIG'])
