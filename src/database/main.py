"""Miscellaneous database functions."""

from typing import Any, Callable, List

from sqlalchemy import Engine, Table, create_engine, insert, select

from .metadata import QueryOptions, metadata

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
    print("Database created")


def generic_insert(table: Table, values: Any) -> int:
    """Insert a row into a table."""
    stmt = insert(table).values(values)
    with ENGINE.begin() as conn:
        result = conn.execute(stmt)
        return result.inserted_primary_key[0]


def generic_select(
    table: Table, query: Any, options: QueryOptions, converter: Callable
) -> List[Any]:
    """Select rows from a table."""
    conditions = []
    for key, value in query.items():
        conditions.append(getattr(table.c, key) == value)
    stmt = select(table).where(*conditions)
    if options.get("limit"):
        stmt = stmt.limit(options["limit"])
    if options.get("offset"):
        stmt = stmt.offset(options["offset"])
    if options.get("orderby"):
        if options.get("order") == "desc":
            stmt = stmt.order_by(getattr(table.c, options["orderby"]).desc())
        else:
            stmt = stmt.order_by(getattr(table.c, options["orderby"]).asc())
    with ENGINE.connect() as conn:
        result = conn.execute(stmt)
        return [converter(row) for row in result]
