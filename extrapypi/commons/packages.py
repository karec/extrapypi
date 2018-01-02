"""Packages utils.

This module export packages logic outside of the views
"""
import logging

import six
from flask_login import current_user
from sqlalchemy.orm.exc import NoResultFound

from extrapypi import storage
from extrapypi.extensions import db
from extrapypi.models import Package, Release
from extrapypi.storage.base import BaseStorage
from extrapypi.commons.permissions import dev_permission, maintainer_permission

log = logging.getLogger("extrapypi")


def get_store(name, params):
    """Utility function to get correct storage class based
    on its name

    :param str name: name of the storage
    :param dict params: storage params from application config
    :return: Correct storage class instance, passing params to constructor
    :rtype: BaseStorage
    :raises: AttributeError
    """
    storage_classes = [getattr(storage, c) for c in storage.__all__]
    storage_classes = list(filter(lambda x: issubclass(x, BaseStorage),
                                  storage_classes))

    store = next((c for c in storage_classes if c.NAME == name), None)
    if store is None:
        log.error("Storage {} does not exists".format(name))
        raise AttributeError("Storage {} does not exists".format(name))
    return store(**params)


def create_package(name, summary, store):
    """Create a package for a given release
    if the package don't exists already

    .. note::
        Maintainer and installer cannot create packages

    :param dict data: request data to use to create package
    :param extrapypi.storage.BaseStorage storage: storage object to use
    :raises: PermissionDenied
    """
    dev_permission.test()
    p = Package(
        name=name,
        summary=summary
    )

    if store.create_package(p) is False:
        log.error(
            "Cannot create storage for package {0.name} using {1.NAME}"
            .format(p, store)
        )
        raise RuntimeError("Storage missconfigured")

    db.session.add(p)
    db.session.commit()
    return p


def create_release(data, config, files):
    """Register and save a new release

    Since pypi itself don't support pre-registration anymore, we don't

    .. note::

        Installers cannot create a new release

    If a release with same version number and package exists, we return it
    :param dict data: request data for registering package
    :param dict config: current app config
    :raises: PermissionDenied
    """
    maintainer_permission.test()

    store = get_store(config.get('STORAGE'), config.get('STORAGE_PARAMS'))

    try:
        package = Package.query.filter_by(name=data['name']).one()
    except NoResultFound:
        package = create_package(data['name'], data['summary'], store)

    if current_user not in package.maintainers:
        package.maintainers.append(current_user)

    release = Release.query.filter_by(version=data['version'], package=package)\
                           .first()
    if release is None:
        release = Release(
            description=data.get('description', 'UNKNOWN'),
            download_url=data.get('download_url', 'UNKNOW'),
            home_page=data.get('home_page', 'UNKNOWN'),
            version=data['version'],
            keywords=data.get('keywords'),
            package=package
        )

    try:
        for name, f in six.iteritems(files):
            store.create_release(package, f)
        db.session.add(release)
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise
    return release


def create_release_from_source(metadata, user):
    """Create a new release from a raw file. Used for import of existing packages into database

    .. warning::

        This function does not check any permissions since it's never called from web ui

    If a release already exists, it does nothing

    :param dict metadata: metadata of the package
    :param extrapypi.models.User user: user to use as maintainer
    """
    try:
        package = Package.query.filter_by(name=metadata['name']).one()
    except NoResultFound:
        package = Package(
            name=metadata['name'],
            summary=metadata.get('summary', 'UNKNOWN')
        )
        db.session.add(package)

    release = Release.query.filter_by(version=metadata['version'], package=package)\
                           .first()

    if release is None:
        release = Release(
            description=metadata.get('description', 'UNKNOWN'),
            download_url=metadata.get('download_url', 'UNKNOW'),
            home_page=metadata.get('home_page', 'UNKNOWN'),
            version=metadata['version'],
            keywords=metadata.get('keywords'),
            package=package
        )
        db.session.add(release)

    if user not in package.maintainers:
        package.maintainers.append(user)

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return release
