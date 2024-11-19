"""Tests for the tokens module in the database package."""

# pylint: disable=redefined-outer-name unused-argument unused-import

from datetime import datetime, timedelta, timezone
from typing import List

import database as db

from .fixtures import users
from .test_main import test_db


def test_insert_oauth_token(users: List[db.User]) -> None:
    """Test the insert_oauth_token function."""
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=3600)
    token = db.OAuthToken(
        user_id=users[0]["id"],
        access_token="1234567890",
        refresh_token="0987654321",
        expires_at=expires_at,
    )
    db.insert_oauth_token(token)
    assert True


def test_select_oauth_token(users: List[db.User]) -> None:
    """Test the select_oauth_token function."""
    expires_at = datetime.now(timezone.utc) + timedelta(seconds=3600)
    token1 = db.OAuthToken(
        user_id=users[0]["id"],
        access_token="1234567890",
        refresh_token="0987654321",
        expires_at=expires_at,
    )
    token2 = db.OAuthToken(
        user_id=users[1]["id"],
        access_token="0987654321",
        refresh_token="1234567890",
        expires_at=expires_at,
    )
    db.insert_oauth_token(token1)
    db.insert_oauth_token(token2)
    tokens = db.select_oauth_token()
    assert len(tokens) == 2
    query = db.OAuthToken(access_token="1234567890")
    tokens = db.select_oauth_token(query)
    assert len(tokens) == 1
    options = db.QueryOptions(limit=1)
    tokens = db.select_oauth_token(options=options)
    assert len(tokens) == 1
