"""Database operations for OAuth tokens."""

from typing import Any, List

from sqlalchemy import update
from sqlalchemy.engine import Row

from .main import ENGINE, generic_insert, generic_select
from .metadata import OAuthToken, QueryOptions, oauth_tokens_table


def _row_to_token(row: Row[Any]) -> OAuthToken:
    return OAuthToken(
        id=row.id,
        user_id=row.user_id,
        access_token=row.access_token,
        refresh_token=row.refresh_token,
        expires_at=row.expires_at,
        created_at=row.created_at,
        updated_at=row.updated_at,
    )


def insert_oauth_token(token: OAuthToken) -> int:
    """Insert a token into the database."""
    return generic_insert(oauth_tokens_table, token)


def select_oauth_token(
    token_query: OAuthToken = OAuthToken(), options: QueryOptions = QueryOptions()
) -> List[OAuthToken]:
    """Select tokens from the database, filtering by the given query and options."""
    return generic_select(oauth_tokens_table, token_query, options, _row_to_token)


def update_or_insert_oauth_token(token: OAuthToken) -> int:
    """
    Updates an existing token if it exists,
    or inserts a new one if it doesn't exist.
    Returns the ID of the updated or inserted token.
    """
    existing_token = select_oauth_token(OAuthToken(user_id=token.user_id))
    if existing_token:
        token_id = existing_token[0]["id"]
        stmt = (
            update(oauth_tokens_table)
            .where(oauth_tokens_table.c.id == token_id)
            .values(token)
        )
        with ENGINE.begin() as conn:
            conn.execute(stmt)
        return token_id
    return generic_insert(oauth_tokens_table, token)
