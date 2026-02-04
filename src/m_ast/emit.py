from .nodes import SelectColumns


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
