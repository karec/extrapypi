"""Default configuration for extra-pypi

All settings present here can be override with your own configuration file using
the EXTRAPYPI_CONFIG env variable.

If the env variable is not set, default settings will be used.


.. note::

    If you use anything else than sqlite, you must install correct database drivers.
    For conveniance, extra-pypi come with two meta packages extra-pypi[mysql] and extra-pypi[postgres]


Configuration options


================== ===========================
NAME               Description
================== ===========================
SQLALCHEMY_URI     SQLAlchemy connexion string
================== ===========================
"""

# SQLAlchemy settings
SQLALCHEMY_URI = "sqlite:///:memory:"


# Logging
