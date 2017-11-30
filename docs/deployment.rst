Deployment
==========

You can run extrapypi with run command, but since it uses flask debug server, it's not suited for production.

But we provide a wsgi entry point to make it easier to run extrapypi using python wsgi server like gunicorn or uwsgi.

Gunicorn
--------

Simple example using gunicorn

.. code-block:: shell

   EXTRAPYPI_CONFIG=/path/to/myconfig.cfg gunicorn extrapypi.wsgi:app


Full example using systemd and nginx (based on http://docs.gunicorn.org/en/stable/deploy.html#systemd)

**/etc/systemd/system/extrapypi.service**

.. code-block:: text

   [Unit]
   Description=extrapypi daemon
   Requires=extrapypi.socket
   After=network.target

   [Service]
   Environment=EXTRAPYPI_CONFIG=/path/to/myconfig.cfg
   PIDFile=/run/gunicorn/pid
   User=myuser
   Group=myuser
   RuntimeDirectory=gunicorn
   ExecStart=/path/to/gunicorn --pid /run/gunicorn/pid   \
          --bind unix:/run/gunicorn/socket extrapypi.wsgi:app
          ExecReload=/bin/kill -s HUP $MAINPID
          ExecStop=/bin/kill -s TERM $MAINPID
          PrivateTmp=true

[Install]
WantedBy=multi-user.target

**/etc/systemd/system/extrapypi.socket**

.. code-block:: text

   [Unit]
   Description=extrapypi socket

   [Socket]
   ListenStream=/run/gunicorn/socket

   [Install]
   WantedBy=sockets.target

Next, enable and start the socket and service

.. code-block:: shell

   systemctl enable extrapypi.socket
   systemctl start extrapypi.service


Last step is to configure nginx as a reverse proxy, basic configuration will look like this


.. code-block:: text

   ...
   http {
     server {
         listen          8000;
         server_name     127.0.0.1;
         location / {
             proxy_pass http://unix:/run/gunicorn/socket;
         }
     }
   }
   ...

Uwsgi
-----

Simple example using uwsgi

.. code-block:: shell

   EXTRAPYPI_CONFIG=/path/to/myconfig.cfg uwsgi --http 0.0.0.0:8000 --module extrapypi.wsgi:app

Full example using systemd and nginx (based on http://uwsgi-docs.readthedocs.io/en/latest/Systemd.html)

**/etc/systemd/system/extrapypi.socket**

.. code-block:: text

   [Unit]
   Description=Socket for extrapypi

   [Socket]
   ListenStream=/var/run/uwsgi/extrapypi.socket
   SocketUser=myuser
   SocketGroup=myuser
   SocketMode=0660

   [Install]
   WantedBy=sockets.target


**/etc/systemd/system/extrapypi.service**

.. code-block:: text

   [Unit]
   Description=%i uWSGI app
   After=syslog.target

   [Service]
   ExecStart=/path/to/uwsgi \
                --socket /var/run/uwsgi/extrapypi.socket \
                --module extrapypi.wsgi:app
   User=myuser
   Group=myuser
   Restart=on-failure
   KillSignal=SIGQUIT
   Type=notify
   StandardError=syslog
   NotifyAccess=all


.. note::

   you can also add your own ini file for uwsgi configuration


Next, enable and start the socket and service

.. code-block:: shell

   systemctl enable extrapypi.socket
   systemctl start extrapypi.service


Last step is to configure nginx as a reverse proxy, basic configuration will look like this


.. code-block:: text

   ...
   http {
     server {
         listen          8000;
         server_name     127.0.0.1;
         location / {
           uwsgi_pass unix:///var/run/uwsgi/extrapypi.socket;
           include uwsgi_params;
        }
     }
   }
   ...


Monitoring
----------

To make it simpler for you to check if extrapypi server is running with your monitoring tools, we provide a simple endpoint
``/ping`` that will always return ``pong`` with status code ``200``.
You must call this endpoint with ``GET`` http verb
