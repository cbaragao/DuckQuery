"""Global configuration flags for DuckQuery."""

_normalize_columns: bool = True


def set_normalize_columns(enabled: bool) -> None:
    """Toggle automatic stripping of numeric column-name suffixes.

    When enabled (the default), run_query strips DuckDB/pandas _1, _2 suffixes
    from result columns using cols.normalize_suffixes.

    Args:
        enabled: True to normalize (default), False to preserve raw names.
    """
    global _normalize_columns
    _normalize_columns = enabled


def get_normalize_columns() -> bool:
    """Return the current normalize_columns setting."""
    return _normalize_columns
