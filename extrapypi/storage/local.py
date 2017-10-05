"""
LocalStorage
------------

Simple local storage that create directories for packages and
put releases files in it
"""
import os
import re

from .base import BaseStorage


class LocalStorage(BaseStorage):
    NAME = 'LocalStorage'

    def __init__(self, packages_root=None):
        if packages_root is None:
            raise RuntimeError("Cannot use LocalStorage without PACKAGES_ROOT set")
        self.packages_root = packages_root

    def get_files(self, package, release=None):
        """Get all files associated to a package

        If release is not None, it will filter files on release version,
        based on a regex
        """
        path = os.path.join(self.packages_root, package.name)
        if not os.path.isdir(path):
            return None

        files = os.listdir(path)
        if release is not None:
            regex = '{}-(?P<version>[0-9\.]*)'.format(package.name)
            regex = re.compile(regex)
            v = release.version
            files = [f for f in files if regex.match(f).group('version') == v]
        return files

    def get_file(self, package, file, release=None):
        """Get a single file from filesystem
        """
        return os.path.join(self.packages_root, package.name, file)
