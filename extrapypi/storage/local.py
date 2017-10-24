"""
LocalStorage
------------

Simple local storage that create directories for packages and
put releases files in it.
"""
import os
import re
import shutil

from .base import BaseStorage


class LocalStorage(BaseStorage):
    NAME = 'LocalStorage'

    def __init__(self, packages_root=None):
        if packages_root is None:
            raise RuntimeError("Cannot use LocalStorage without PACKAGES_ROOT set")
        self.packages_root = packages_root

    def delete_package(self, package):
        """Delete entire package directory
        """
        path = os.path.join(
            self.packages_root,
            package.name
        )
        try:
            shutil.rmtree(path)
            return True
        except Exception:
            return False

    def delete_release(self, package, version):
        """Delete all files matching specified version
        """
        path = os.path.join(self.packages_root, package.name)
        if not os.path.isdir(path):
            return False

        files = os.listdir(path)
        regex = '{}-(?P<version>[0-9\.]*)[\.-].*'.format(package.name)
        r = re.compile(regex)
        files = filter(
            lambda f: r.match(f) and r.match(f).group('version') == version,
            files
        )
        files = list(files)
        for f in files:
            os.remove(os.path.join(path, f))
        return True

    def create_package(self, package):
        """Create new directory for a given package
        """
        path = os.path.join(
            self.packages_root,
            package.name
        )
        try:
            os.mkdir(path)
            return True
        except OSError:
            return False

    def create_release(self, package, release_file):
        """Copy release file inside package directory

        If package directory does not exists, it will create it before
        """
        package_path = os.path.join(
            self.packages_root,
            package.name
        )
        if not os.path.isdir(package_path):
            if not self.create_package(package):
                return False
        release_path = os.path.join(package_path, release_file.filename)
        release_file.save(release_path)
        return True

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
            regex = '{}-(?P<version>[0-9\.]*)[\.-].*'.format(package.name)
            r = re.compile(regex)
            v = release.version
            files = filter(
                lambda f: r.match(f) and r.match(f).group('version') == v,
                files
            )
            files = list(files)
        return files

    def get_file(self, package, file, release=None):
        """Get a single file from filesystem
        """
        return os.path.join(self.packages_root, package.name, file)
