"""Database operations for users."""

from typing import Any, List

from sqlalchemy.engine import Row

from .main import generic_insert, generic_select
from .metadata import QueryOptions, User, users_table


def _row_to_user(row: Row[Any]) -> User:
    return User(
        id=row.id,
        x_user_id=row.x_user_id,
        x_username=row.x_username,
        created_at=row.created_at,
    )


def insert_user(user: User) -> int:
    """Insert a user into the database."""
    return generic_insert(users_table, user)


def select_users(
    user_query: User = User(), options: QueryOptions = QueryOptions()
) -> List[User]:
    """Select users from the database, filtering by the given query and options."""
    return generic_select(users_table, user_query, options, _row_to_user)
