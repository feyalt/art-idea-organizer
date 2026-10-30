
"""Shared pytest fixtures."""

import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def app():
    """Create an isolated application for each test."""
    class TestConfig:
        TESTING = True
        SECRET_KEY = "test-key"
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Provide a test client for HTTP requests."""
    return app.test_client()

