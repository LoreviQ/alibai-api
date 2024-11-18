"""Miscellaneous database functions."""

from sqlalchemy import Engine, create_engine
from .metadata import metadata

# Default connection string is a sqlite database stored in memory.
# Change this to your database connection string.
CONN_STRING = "sqlite+pysqlite:///:memory:"
ECHO = True
ENGINE = create_engine(
    CONN_STRING,
    echo=ECHO,
)


def create_db(engine: Engine | None = None) -> None:
    """Create the database."""
    if not engine:
        engine = ENGINE
    metadata.create_all(ENGINE)
