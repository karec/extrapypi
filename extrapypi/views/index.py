"""Views for handling simple index like original pypi
"""
from flask import request


def simple():
    if request.method == 'POST':
        pass
    return "test-package<br />other-package"


def package_view(package):
    return "test-package-0.1.tar.gz"


def download_package(package, archive):
    return "ok"
