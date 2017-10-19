EXTRAPYPI
=========

External pypi server with web ui and basics permissions management

extrapypi don't mirror official pypi packages, and will not. It's just not build with this goal in mind. extrapypi is just here to provide you an extra index to upload and install private packages simply.

Features
--------

* Upload packages from twine / setuptools
* Install packages with pip using only extra-index option
* Basics permissions management using roles (currently admin, developer, installer, builder)
* Easy deployment / installation using the WSGI server you want
* MySQL, PostgresSQL and SQLite support
* Extensible storage system
* CLI tools to help you deploy / init / test extrapypi
* Basic dashboard to visualize packages and users
* Codebase aim to be simple and hackable

