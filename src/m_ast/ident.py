"""Identifier quoting and reserved word detection for SQL emission."""


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
