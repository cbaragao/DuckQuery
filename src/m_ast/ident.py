"""Identifier quoting and reserved word detection for SQL emission."""

# Common SQL reserved words (DuckDB / ANSI SQL subset)
_RESERVED_WORDS: frozenset[str] = frozenset(
    {
        "all",
        "alter",
        "and",
        "as",
        "asc",
        "between",
        "by",
        "case",
        "cast",
        "column",
        "create",
        "cross",
        "delete",
        "desc",
        "distinct",
        "drop",
        "else",
        "end",
        "except",
        "exists",
        "false",
        "from",
        "full",
        "group",
        "having",
        "in",
        "inner",
        "insert",
        "intersect",
        "into",
        "is",
        "join",
        "left",
        "like",
        "limit",
        "not",
        "null",
        "offset",
        "on",
        "or",
        "order",
        "outer",
        "right",
        "select",
        "set",
        "table",
        "then",
        "true",
        "union",
        "update",
        "using",
        "values",
        "when",
        "where",
        "with",
    }
)


def is_reserved(name: str) -> bool:
    """Return True if *name* is a common SQL reserved word (case-insensitive).

    Example:
        is_reserved("select") -> True
        is_reserved("SELECT") -> True
        is_reserved("my_column") -> False
    """
    return name.lower() in _RESERVED_WORDS


def quote(name: str) -> str:
    """Safely quote an identifier for SQL.

    - Wraps the identifier in double quotes
    - Escapes any existing double quotes by doubling them
    - Returns the quoted identifier

    Example:
        quote("column") -> '"column"'
        quote('my"column') -> '"my""column"'
    """
    if not name:
        raise ValueError("Identifier name cannot be empty")

    # Escape any existing double quotes by doubling them
    escaped = name.replace('"', '""')
    return f'"{escaped}"'
