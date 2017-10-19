# extrapypi

[![Build Status](https://travis-ci.org/karec/extrapypi.svg?branch=master)](https://travis-ci.org/karec/extrapypi)
[![Coverage Status](https://coveralls.io/repos/github/karec/extrapypi/badge.svg?branch=master)](https://coveralls.io/github/karec/extrapypi?branch=master)

External pypi server with web ui and basics permissions management

extrapypi don't mirror official pypi packages, and will not. It's just not build with 
this goal in mind.
extrapypi is just here to provide you an extra index to upload and install private packages
simply.


* [Installation](#installation)
* [Deployment](#deployment)
* [Usage](#usage)


## Features

* Upload packages from twine / setuptools
* Install packages with pip using only extra-index option
* Basics permissions management using roles (currently admin, developer, installer, builder)
* Easy deployment / installation using the WSGI server you want
* MySQL, PostgresSQL and SQLite support
* Extensible storage system
* CLI tools to help you deploy / init / test extrapypi
* Basic dashboard to visualize packages and users
* Codebase aim to be simple and hackable

## Roadmap

Features that we want to implement for future releases :

* interface for pip search
* prefix management

## Installation

You can install extrapypi with pip

```bash
pip install extrapypi
```

For mysql 

```bash
pip install extrapypi[mysql]
```

For postgresql

```bash
pip install extrapypi[postgres]
```

Or from source 

```bash
python setup.py install
```

## Deployment

First thing, you will need to create a configuration file for your extrapypi. We provide 
a cli command to generate a sample :

```bash
extrapypi start --filename myconfig.cfg
```

This command will create a file named `myconfig.cfg` in your current directory with the following content 

```python
"""Sample configuration
"""

# Database connexion string
SQLALCHEMY_DATABASE_URI = "sqlite:///extrapypi.db"

# Update this secret key for production !
SECRET_KEY = "changeit"

# Storage settings
# You need to update at least packages_root setting
STORAGE_PARAMS = {
    'packages_root': "/path/to/my/packages"
}

```

Once you've updated your configuration, you will need to init database 

```bash
EXTRAPYPI_CONFIG=/path/to/myconfig.cfg extrapypi init
```

Note that you can also export `EXTRAPYPI_CONFIG` variable

This will create tables and two users : 

* an admin with login and password set to `admin`
* an install with login and password set to `pip`

You can check full `init` usage in documentation.


Here we are, you can now run extrapypi

For testing purpose 

```bash
EXTRAPYPI_CONFIG=/path/to/myconfig.cfg extrapypi run
```

With gunicorn

```bash
EXTRAPYPI_CONFIG=/path/to/myconfig.cfg gunicorn extrapypi.wsgi:app
```

with uwsgi

```bash
EXTRAPYPI_CONFIG=/path/to/myconfig.cfg uwsgi --http 0.0.0.0:8000 --module extrapypi.wsgi:app
```

Once done, you can access the dashboard at the following address :

`http://mydomainorip:8000/dashboard`

You can see full examples for deploying extrapypi in production in the documentation


**WARNING** since extrapypi use basic auth, we strongly advise to run it behind a reverse proxy (like nginx) and use 
https

## Usage


### Uploading packages

extrapypi is compliant with setuptools / twine, you just need to update your `.pypirc` like this

```
[distutils]
index-servers =
    local

[local]
username=admin
password=admin
repository=http://127.0.0.1:5000/simple/
```

And then you can run

```bash
python setup.py bdist_wheel upload -r local
```

Or using twine

```bash
twine upload -r local dist/extra_pypi-0.1-py3.5.egg
```

### Installing packages with pip

extrapypi is built to be used as an extra index, so you can simply run :

```bash
pip install extrapypi --extra-index-url http://user:password@mypypiurl.org/simple/ 
```

or directly updating your `pip.conf` file 

```bash
[global]
extra-index-url = http://user:password@mypypiurl.org/simple/
```


## Development

Install main package

```
python setup.py install
```

Then you can use included cli to setup your env

```
extrapypi init
extrapypi run
```

### Running server

extrapypi use flask cli, `extrapypi` command is only a hook to `extrapypi.manage` that include several commands 
but anything present in flask script can be used for extrapypi too.

For exemple you can start application using `flask run` with debug on like this :

```
FLASK_DEBUG=1 flask run
```

### Running test


First install tox

```
pip install tox
```

Then you can just run 

```
tox -e sqlite
```

You can also run tox in all envs if needed
