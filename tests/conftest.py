import pytest
import typing
from fastapi.testclient import TestClient
from app.main import app as target_app


@pytest.fixture(scope="session")
def client():
    with TestClient(app=target_app) as client:
        yield client
