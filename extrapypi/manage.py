import os
import click
from flask.cli import FlaskGroup
from flask_migrate import MigrateCommand


def create_pypi(info):
    from extrapypi.app import create_app
    return create_app(
        config=os.environ.get('EXTRAPYPI_CONFIG', None)
    )


@click.group(cls=FlaskGroup, create_app=create_pypi)
def cli():
    """CLI for extra-pypi"""


@cli.command("init")
def init():
    """Init database and create an admin user"""


@cli.command("create-user")
@click.argument("username", nargs=1)
@click.argument("password", nargs=1)
def create_user():
    """Create a new user"""


@cli.command()
def db():
    """Flask-migrate commands"""
    MigrateCommand()


@cli.command("init-config")
def init_config():
    """Sample configuration file for extra-pypi"""


@cli.command("wsgi-file")
def init_wsgi_file():
    """Sample wsgi file for extra-pypi"""


@cli.command("get-static")
def collect_static():
    """Get static files location"""


if __name__ == "__main__":
    cli()
