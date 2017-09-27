from flask import Flask


def create_app(config=None, testing=False):

    app = Flask('extra-pypi')

    return app
