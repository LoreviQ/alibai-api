"""Tests for the main module in the database package."""

# pylint: disable=redefined-outer-name unused-argument

import pytest

import database as db


@pytest.fixture
def test_db(monkeypatch) -> None:
    """Create the database."""
    db.create_db()


def test_create_db() -> None:
    """Test the create_db function."""

    db.create_db()
    assert True
