"""Contains a numwea of database fixtures generating the required data before tests"""

# pylint: disable=redefined-outer-name unused-argument unused-import

from typing import Generator, List

import pytest

import database as db

from .test_main import test_db


@pytest.fixture
def users(test_db: None) -> Generator[List[db.User], None, None]:
    """Creates a list of users for testing"""
    db.insert_user(
        db.User(
            x_user_id="1234567890",
            x_username="loreviq",
        )
    )
    db.insert_user(
        db.User(
            x_user_id="0987654321",
            x_username="loreviq2",
        )
    )
    yield db.select_users()
