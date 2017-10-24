"""
Base Storage
------------

BaseStorage define all methods needed by storages.
All storage must be inherited from ``BaseStorage`` and implement the following methods

* delete_package
* delete_release
* create_package
* create_release
* get_files
* get_file

Storages classes handle all packages and releases operation outside of the SQL database,
this include storage of packages sources, listing of files, removing deleted packages, etc.
"""
import six


class BaseStorage(object):
    """Base class for storage drivers, should be inherited by all sub-classes

    In the constructor, kwargs are used to pass settings to the driver.
    By default it will set an attribute for each item in kwargs
    """
    NAME = None

    def __init__(self, **kwargs):
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    def delete_package(self, package):
        """Must delete an entire package

        :param models.Package package: package to delete
        :return: True if deletion is successful or False
        :rtype: bool
        """
        raise NotImplementedError()

    def delete_release(self, package, version):
        """Must delete all files of a package version

        :param models.Package: package to delete
        :param str version: version to delete
        :return: True if deletion is successful or False
        :rtype: bool
        """
        raise NotImplementedError()

    def create_package(self, package):
        """Must create a new location for a package

        :param models.Package package: new package that need an emplacement
        :return: True if creation successful, else return False
        :rtype: bool
        """
        raise NotImplementedError()

    def create_release(self, package, release_file):
        """Must copy release_file to the correct location

        .. note::

            release_file will be a werkzeug.datastructures.FileStorage object

        :param models.Package package: package for the release
        :param FileStorage release_file: release file to save
        """
        raise NotImplementedError()

    def get_files(self, package, release=None):
        """Must return all files for a given package / release

        :param models.Package package: package object for which we want files
        :param models.Release release: for filter files returned based on release
        :return: list of all avaible files for this package or None if an error append
        :rtype: list
        """
        raise NotImplementedError()

    def get_file(self, package, file, release=None):
        """Must return a given file

        Returned value will be directly send to Flask.send_file
        in most cases, be sure that return format is compatible with this
        function

        :param models.Package package: package objet
        :param str file: file name to find
        """
        raise NotImplementedError()
