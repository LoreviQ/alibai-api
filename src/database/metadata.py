"""SQLAlchemy metadata."""

from datetime import datetime, timezone
from typing import TypedDict

from sqlalchemy import Column, DateTime, ForeignKey, Integer, MetaData, String, Table
from typing_extensions import NotRequired

metadata = MetaData()


class User(TypedDict):
    """User object."""

    id: NotRequired[int]
    x_user_id: NotRequired[str]
    x_username: NotRequired[str]
    created_at: NotRequired[datetime]


users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("x_user_id", String, unique=True),
    Column("x_username", String),
    Column("created_at", DateTime, default=datetime.now(timezone.utc)),
)


class OAuthToken(TypedDict):
    """OAuth token object."""

    id: NotRequired[int]
    user_id: NotRequired[int]
    access_token: NotRequired[str]
    refresh_token: NotRequired[str]
    expires_at: NotRequired[datetime]
    created_at: NotRequired[datetime]
    updated_at: NotRequired[datetime]


oauth_tokens_table = Table(
    "oauth_tokens",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    Column("access_token", String, nullable=False),
    Column("refresh_token", String),
    Column("expires_at", DateTime, nullable=False),
    Column("created_at", DateTime, default=datetime.now(timezone.utc)),
    Column(
        "updated_at",
        DateTime,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    ),
)


class QueryOptions(TypedDict, total=False):
    """Type for query options"""

    limit: NotRequired[int]
    offset: NotRequired[int]
    orderby: NotRequired[str]
    order: NotRequired[str]
