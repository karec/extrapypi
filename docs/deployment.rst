Deployment
==========

You can run extrapypi with run command, but since it uses flask debug server, it's not suited for production.

But we provide a wsgi entry point to make it easier to run extrapypi using python wsgi server like gunicorn or uwsgi.

Gunicorn
--------

Simple example using gunicorn

.. code-block:: shell

   EXTRAPYPI_CONFIG=/path/to/myconfig.cfg gunicorn extrapypi.wsgi:app


Uwsgi
-----

.. code-block:: shell

   EXTRAPYPI_CONFIG=/path/to/myconfig.cfg uwsgi --http 0.0.0.0:8000 --module extrapypi.wsgi:app

