import os

from extrapypi.app import create_app

app = create_app(config=os.environ.get('EXTRAPYPI_CONFIG'))
