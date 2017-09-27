"""
Extra-pypi configuration
========================

All settings present here can be override with your own configuration file using
the EXTRAPYPI_CONFIG env variable.

If the env variable is not set, default settings will be used.


This file is a pure python file, that's mean that you can also include python code in here,
for example for packages location

.. warning::

    For security reasons you should at least change the secret key


.. note::

    If you use anything else than sqlite, you must install correct database drivers.
    For conveniance, extra-pypi come with two meta packages extra-pypi[mysql] and extra-pypi[postgres]


.. note::

    You can also override all settings of flask extensions used by extra-pypi even if there are not
    here


Configuration options


================== ===========================
NAME               Description
================== ===========================
SQLALCHEMY_URI     SQLAlchemy connexion string
================== ===========================
STATIC_URL         Url for static files
================== ===========================
PACKAGES_ROOT      Location for packages upload
================== ===========================
"""
import os


# SQLAlchemy settings
SQLALCHEMY_URI = "sqlite:///:memory:"


# Flask settings
STATIC_URL = '/static/'


# Extra-pypi settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGES_ROOT = "{}/packages".format(BASE_DIR)


# Logging
