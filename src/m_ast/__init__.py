"""Minimal AST package for DuckQuery (M-like transforms).

This package will host tiny AST node classes used to compose transforms before
emitting SQL. Keep nodes minimal and data-focused.
"""

from .nodes import (
    SelectRows,
    SelectColumns,
    AddColumn,
    RenameColumns,
    Group,
    Join,
    Pivot,
    Unpivot,
    Buffer,
)

__all__ = [
    "SelectRows",
    "SelectColumns",
    "AddColumn",
    "RenameColumns",
    "Group",
    "Join",
    "Pivot",
    "Unpivot",
    "Buffer",
    "explain_step",
]


def explain_step(step) -> str:
    """Return a short description string for an AST node step.

    Args:
        step: An AST node instance (SelectRows, SelectColumns, etc.)

    Returns:
        A human-readable description of the transformation step.

    Examples:
        >>> from m_ast.nodes import SelectRows
        >>> explain_step(SelectRows(table="employees", condition="age >= 30"))
        'SelectRows: filter by age >= 30'
    """
    class_name = step.__class__.__name__

    if isinstance(step, SelectRows):
        return f"SelectRows: filter by {step.condition}"
    elif isinstance(step, SelectColumns):
        cols = ", ".join(step.columns)
        return f"SelectColumns: project [{cols}]"
    elif isinstance(step, AddColumn):
        return f"AddColumn: add {step.new_column} = {step.expression}"
    elif isinstance(step, RenameColumns):
        renames = ", ".join(f"{old}->{new}" for old, new in step.mapping.items())
        return f"RenameColumns: {renames}"
    elif isinstance(step, Group):
        keys = ", ".join(step.keys)
        aggs = ", ".join(f"{name}={expr}" for name, expr in step.aggs.items())
        return f"Group: by [{keys}] with {aggs}"
    elif isinstance(step, Join):
        on_desc = ", ".join(f"{left}={right}" for left, right in step.on.items())
        return f"Join: {step.kind} join on {on_desc}"
    elif isinstance(step, Pivot):
        return f"Pivot: {step.pivot_column} -> columns, values from {step.value_column}"
    elif isinstance(step, Unpivot):
        cols = ", ".join(step.columns)
        return f"Unpivot: [{cols}] -> {step.attribute_column}, {step.value_column}"
    elif isinstance(step, Buffer):
        return "Buffer: materialize table (prevent query folding)"
    else:
        return f"{class_name}: unknown step type"
