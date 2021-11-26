import pytest

from app import app
from chalice.test import Client


@pytest.fixture
def client():
    # config.TESTING_MODE = True
    with Client(app) as client:
        yield client
