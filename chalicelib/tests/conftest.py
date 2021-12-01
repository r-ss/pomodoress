import pytest

from app import app
from chalice.test import Client

from chalicelib.config import config

@pytest.fixture
def client():
    
    config.TESTING_MODE = True
    config.AWS_SSM_ENABLED = False
    config.AWS_LOGGING_ENABLED = False
    config.TELEGRAM_ENABLED = False

    with Client(app) as client:
        yield client
