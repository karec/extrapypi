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
@click.option('--pip-user', default='pip', help="installer username")
@click.option('--pip-pwd', default='pip', help="installer password")
def init(user, password, pip_user, pip_pwd):
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

    pip_pwd = custom_app_context.hash(pip_pwd)
    pip_usr = models.User(
        username=pip_user,
        email="email@admin.com",
        password_hash=pip_pwd,
        role="installer"
    )

    db.session.add(pip_usr)
    db.session.add(user)
    db.session.commit()
    click.echo("User %s created" % user.username)
    click.echo("User %s created" % pip_usr.username)


@cli.command("start")
@click.option('--filename', default='config.cfg', help="config file name")
def init_config(filename):
    """create sample config file"""
    from pkg_resources import resource_string
    default_config = resource_string(
        "extrapypi",
        "data/default_config.cfg"
    ).decode("utf-8")

    with open(filename, 'w') as f:
        f.write(default_config)


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
