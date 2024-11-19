"""Tests for the main module in the routes package."""

# pylint: disable=redefined-outer-name unused-argument unused-import

from flask.testing import FlaskClient

from .fixtures import app, client


def test_healthz(client: FlaskClient) -> None:
    """Test the healthz route."""
    response = client.get("/healthz")
    assert response.status_code == 200
