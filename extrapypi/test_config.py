import os

SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB', 'sqlite:///:memory:')
WTF_CSRF_ENABLED = False
