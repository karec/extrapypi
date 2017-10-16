import os
import click
from flask.cli import FlaskGroup
from extrapypi.app import create_app
from flask_migrate import MigrateCommand
from passlib.apps import custom_app_context


def create_pypi(info):
    return create_app(
        config=os.environ.get('EXTRAPYPI_CONFIG', None)
    )


@click.group(cls=FlaskGroup, create_app=create_pypi)
def cli():
    """CLI for extra-pypi"""


@cli.command("init")
@click.option('--user', default='admin', help="first user to create")
@click.option('--password', default='admin', help="user password")
def init(user, password):
    """Init database and create an admin user"""
    from extrapypi.extensions import db
    from extrapypi import models
    click.echo("Creating database...")
    db.create_all()
    click.echo("Database created")

    click.echo("Creating user %s" % user)
    pwd = custom_app_context.hash(password)
    user = models.User(
        username=user,
        email="email@admin.com",
        password_hash=pwd,
        role='admin'
    )
    db.session.add(user)
    db.session.commit()
    click.echo("User created")


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
