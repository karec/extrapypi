"""Views for handling simple index like original pypi
"""
from flask import request


def simple():
    """Simple view index used only on GET requests

    Used to list packages
    """
    if request.method == 'POST':
        print("debug")
        print(dict(request.form))
    return "test-package<br />other-package"


def package_view(package):
    return "test-package-0.1.tar.gz"


def download_package(package, archive):
    return "ok"
