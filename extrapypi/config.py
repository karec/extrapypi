"""
Extrapypi configuration
=======================

All settings present here can be override with your own configuration file using
the EXTRAPYPI_CONFIG env variable.

If the env variable is not set, default settings will be used.


This file is a pure python file, that's mean that you can also include python code in here,
for example for packages location

.. warning::

    For security reasons you should at least change the secret key


.. note::

    If you use anything else than sqlite, you must install correct database drivers
    like psycopg2 or pymysql for example. Since we use SQLAlchemy you can use any compliant database, but
    we only test sqlite, mysql and postgresql


.. note::

    You can also override all settings of flask extensions used by extra-pypi even if there are not
    here


For quickstart you can generate a sample configuration file using ``start`` command like this

.. code-block:: shell

    extrapypi start --filename myconfig.cfg


Generated file will have the following content

.. code-block:: python

    # Database connexion string
    SQLALCHEMY_DATABASE_URI = "sqlite:///extrapypi.db"

    # Update this secret key for production !
    SECRET_KEY = "changeit"

    # Storage settings
    # You need to update at least packages_root setting
    STORAGE_PARAMS = {
        'packages_root': "/path/to/my/packages"
    }



Configuration options


================== ==============================================================================
NAME               Description
================== ==============================================================================
BASE_DIR           Base directory, by default used by SQLALCHEMY_URI and PACKAGES_ROOT
SQLALCHEMY_URI     SQLAlchemy connexion string
DEBUG              Enable debug mode
STATIC_URL         Url for static files
SECRET_KEY         Secret key used for the application, you must update this
STORAGE            Storage class name to use
STORAGE_PARAMS     Storage class parameters, see specific storages documentation for more details
DASHBOARD          You can disable dashboard if you set it to FALSE
LOGGING_CONFIG     Logger configuration, using standard python dict config
================== ==============================================================================

Defaut logging config look like this

.. code-block:: python

   LOGGING_CONFIG = {
    'version': 1,
    'root': {
        'level': 'NOTSET',
        'handlers': ['default'],
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s: %(levelname)s / %(name)s] %(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'extrapypi': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False,
        },
        'alembic.runtime.migration': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    }
  }

"""
import os

# Base settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = "sqlite:///{}/extrapypi.db".format(BASE_DIR)
SQLALCHEMY_TRACK_MODIFICATIONS = False


# Flask settings
DEBUG = True
STATIC_URL = '/static/'
SECRET_KEY = 'changeit'


# Storage settings
STORAGE = 'LocalStorage'
STORAGE_PARAMS = {
    'packages_root': "{}/packages".format(BASE_DIR)
}

WTF_CSRF_ENABLED = True
WTF_CSRF_FIELD_NAME = 'csrf_token'

DASHBOARD = True


# Logging
LOGGING_CONFIG = {
    'version': 1,
    'root': {
        'level': 'NOTSET',
        'handlers': ['default'],
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s: %(levelname)s / %(name)s] %(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'extrapypi': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False,
        },
        'alembic.runtime.migration': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
    }
}
