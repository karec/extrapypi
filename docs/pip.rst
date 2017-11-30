Configuring pip to work with extrapypi
======================================


Uploading packages
------------------

extrapypi is compliant with setuptools / twine, you just need to update your ``.pypirc``


.. code-block:: text

   [distutils]
   index-servers =
       local

   [local]
   username=myuser
   password=mypassword
   repository=https://myextrapypiurl/simple/


That's it, you can now upload packages to your extrapypi instance

Using setuptools

.. code-block:: shell

   python setup.py bdist_wheel upload -r local


Or twine

.. code-block:: shell

   twine upload -r local dist/extra_pypi-0.1-py3.5.egg


Installing packages
-------------------

Two choices here :

Using CLI argument when calling pip

.. code-block:: shell

   pip install extrapypi --extra-index-url https://user:password@myextrapypiurl/simple/

Or update your ``pip.conf`` file

.. code-block:: shell

   [global]
   extra-index-url = https://user:password@myextrapypiurl/simple/
