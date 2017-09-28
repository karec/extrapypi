# extrapypi

External pypi server with web ui and basics permissions management


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
