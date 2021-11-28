import pytest

from app import app
from chalice.test import Client

from chalicelib.config import Config

@pytest.fixture
def client():
    Config.TESTING_MODE = True
    with Client(app) as client:
        yield client
