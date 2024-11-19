"""Tests for the users module in the database package."""

# pylint: disable=redefined-outer-name unused-argument unused-import

import database as db

from .test_main import test_db


def test_insert_user(test_db: None) -> None:
    """Test the insert_user function."""
    user = db.User(
        x_user_id="1234567890",
        x_username="loreviq",
    )
    db.insert_user(user)
    assert True


def test_select_users(test_db: None) -> None:
    """Test the select_users function."""
    user1 = db.User(
        x_user_id="1234567890",
        x_username="loreviq",
    )
    user2 = db.User(
        x_user_id="0987654321",
        x_username="loreviq2",
    )
    db.insert_user(user1)
    db.insert_user(user2)
    users = db.select_users()
    assert len(users) == 2
    query = db.User(x_username="loreviq")
    users = db.select_users(query)
    assert len(users) == 1
    options = db.QueryOptions(limit=1)
    users = db.select_users(options=options)
    assert len(users) == 1
