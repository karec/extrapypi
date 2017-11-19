Installation
============

Using pip
---------

Recommanded way to install extrapypi is to use the latest version hosted on PyPI :

.. code-block:: shell

   pip install extrapypi


Additionally, we provide 2 meta packages, one for mysql and one for postgresql

.. code-block:: shell

   pip install extrapypi[mysql]
   pip install extrapypi[postgres]


This will only install ``pymysql`` for mysql or ``psycopg2`` for postgres.


Installing via git
------------------

Extrapypi is hosted at https://github.com/karec/extrapypi, you can install it like this


.. code-block:: shell

   git clone https://github.com/karec/extrapypi.git
   cd extrapypi
   python setup.py install


Or, for development

.. code-block:: shell

   pip install -e .


Starting and init extrapypi
---------------------------

Once installed, you will need to create a configuration file and create database, tables and users.
But don't worry, we provide commands in CLI tools to do that.

First thing we need : generate a configuration file

.. code-block:: shell

   extrapypi start --filename myconfig.py

This will generate a minimal configuration file, full documentation on configuration is avaible in the :doc:`configuration section <configuration>`.

Once configuration done, you can create database, tables and default users using init command

.. code-block:: shell

   EXTRAPYPI_CONFIG=/path/to/myconfig.cfg extrapypi init


It will create two users :

* User admin, with password admin and role admin
* User pip with password pip and role installer

After that you can start extrapypi using run command

.. code-block:: shell

   EXTRAPYPI_CONFIG=/path/to/myconfig.cfg extrapypi run
