import pytest

from extrapypi.app import create_app


@pytest.fixture
def app():
    return create_app(testing=True)
