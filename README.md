# extrapypi

[![Build Status](https://travis-ci.org/karec/extrapypi.svg?branch=master)](https://travis-ci.org/karec/extrapypi)
[![Coverage Status](https://coveralls.io/repos/github/karec/extrapypi/badge.svg?branch=master)](https://coveralls.io/github/karec/extrapypi?branch=master)

External pypi server with web ui and basics permissions management

extrapypi don't mirror official pypi packages, and will not. It's just not build with 
this goal in mind.
extrapypi is just here to provide you an extra index to upload and install private packages
simply.


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

## Deployement




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
tox
```
