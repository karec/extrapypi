"""Views for handling simple index like original pypi
"""
import logging
from flask import request

log = logging.getLogger("extrapypi")


def simple():
    """Simple view index used only on GET requests

    Used to list packages
    """
    if request.method == 'POST':
        log.info("debug")
        log.info(request.form.getlist('classifiers'))
    return "test-package<br />other-package"


def package_view(package):
    return "test-package-0.1.tar.gz"


def download_package(package, archive):
    return "ok"
