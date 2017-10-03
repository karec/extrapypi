"""Packages utils.

This module export packages logic outside of the views
"""
from extrapypi.extensions import db
from extrapypi.models import Package


def create_package(data):
    """Create a package for a given release
    if the package don't exists already

    :param dict data: request data to use to create package
    """


def register_release(data, config):
    """Register and save a new release

    Since pypi itself don't support pre-registration anymore, we don't

    :param dict data: request data for registering package
    :param dict config: current app config
    """
