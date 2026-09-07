"""
Pytest configuration and client fixtures for API test automation.
"""
import pytest
import sys
from pathlib import Path

# Add project directory to PYTHONPATH
sys.path.insert(0, str(Path(__file__).parent.parent / "api"))
from app import app as flask_app


@pytest.fixture
def app():
    flask_app.config.update({
        "TESTING": True,
    })
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()
