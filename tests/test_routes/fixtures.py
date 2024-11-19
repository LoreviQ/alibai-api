"""This file contains the fixtures for the routes package testing."""

# pylint: disable=redefined-outer-name unused-argument unused-import


from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from main import initialize_app


@pytest.fixture
def app() -> Generator[Flask, None, None]:
    """Initialize the flask app."""
    app = initialize_app()
    yield app


@pytest.fixture
def client(app: Flask) -> Generator[FlaskClient, None, None]:
    """Create a test client."""
    with app.test_client() as client:
        yield client
