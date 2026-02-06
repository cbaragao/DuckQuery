from .nodes import SelectColumns, Join


def emit_selectcolumns(node: SelectColumns) -> str:
    """Emit a simple SQL SELECT clause for a SelectColumns AST node.

    This emitter is intentionally tiny: it quotes column names and leaves the
    table identifier as provided (string or previous AST node name).
    """
    if not isinstance(node, SelectColumns):
        raise TypeError("emit_selectcolumns expects a SelectColumns node")

    cols = ", ".join([f'"{c}"' for c in node.columns])
    table = (
        node.table
        if isinstance(node.table, str)
        else getattr(node.table, "__name__", repr(node.table))
    )
    return f"SELECT {cols} FROM {table}"


def select_clause(columns: list[str]) -> str:
    """Emit a SQL SELECT fragment for a list of column names.

    - If `columns` is empty, returns `SELECT *`.
    - Column names are double-quoted for safety.
    """
    if not columns:
        return "SELECT *"
    cols = ", ".join([f'"{c}"' for c in columns])
    return f"SELECT {cols}"


def from_clause(table_name: str) -> str:
    """Emit a SQL FROM fragment for a table name.

    The table name will be double-quoted. If `table_name` is empty or falsy,
    raises a ValueError.
    """
    if not table_name:
        raise ValueError("table_name must be a non-empty string")
    return f'FROM "{table_name}"'


def where_clause(conditions: list[str]) -> str:
    """Emit a SQL WHERE fragment for simple conditions.

    - If `conditions` is empty, returns an empty string.
    - Conditions are joined with AND.
    - Each condition is assumed to be a valid SQL expression.
    """
    if not conditions:
        return ""
    joined = " AND ".join(conditions)
    return f"WHERE {joined}"


def join_clause(join: Join) -> str:
    """Emit a SQL JOIN clause for a Join AST node.

    - Supports join kinds: 'inner', 'left', 'right', 'full'
    - The `on` dict maps left column names to right column names
    - Table names are extracted from the node or quoted if strings
    """
    if not isinstance(join, Join):
        raise TypeError("join_clause expects a Join node")

    # Extract table names
    right_table = (
        join.right
        if isinstance(join.right, str)
        else getattr(join.right, "__name__", repr(join.right))
    )

    # Build ON conditions
    on_parts = [
        f'"{left_col}" = "{right_col}"' for left_col, right_col in join.on.items()
    ]
    on_clause = " AND ".join(on_parts)

    # Map join kind to SQL syntax
    kind_map = {
        "inner": "INNER JOIN",
        "left": "LEFT JOIN",
        "right": "RIGHT JOIN",
        "full": "FULL OUTER JOIN",
    }
    join_type = kind_map.get(join.kind, "INNER JOIN")

    return f'{join_type} "{right_table}" ON {on_clause}'


def group_by_clause(columns: list[str]) -> str:
    """Emit a SQL GROUP BY fragment for a list of column names.

    - If `columns` is empty, returns an empty string.
    - Column names are double-quoted for safety.
    """
    if not columns:
        return ""
    cols = ", ".join([f'"{c}"' for c in columns])
    return f"GROUP BY {cols}"
