import pytest

from app import app
from chalice.test import Client

from chalicelib.config import Config

@pytest.fixture
def client():
    
    Config.TESTING_MODE = True
    Config.AWS_SSM_ENABLED = False
    Config.TELEGRAM_ENABLED = False

    with Client(app) as client:
        yield client
