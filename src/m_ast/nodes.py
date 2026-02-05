from dataclasses import dataclass
from typing import Any
from typing import List, Dict


@dataclass
class SelectRows:
    """AST node representing a Table.SelectRows operation.

    Fields:
    - table: a table identifier or previous AST node
    - condition: an M-like condition string (e.g. "age >= 30")
    """

    table: Any
    condition: str

    def __repr__(self) -> str:
        tbl = getattr(self.table, "__name__", None) or repr(self.table)
        return f"SelectRows(table={tbl}, condition={self.condition!r})"


@dataclass
class SelectColumns:
    """AST node representing a Table.SelectColumns operation.

    Fields:
    - table: a table identifier or previous AST node
    - columns: list of column names to project
    """

    table: Any
    columns: List[str]

    def __repr__(self) -> str:
        tbl = getattr(self.table, "__name__", None) or repr(self.table)
        cols = ", ".join(self.columns)
        return f"SelectColumns(table={tbl}, columns=[{cols}])"


@dataclass
class AddColumn:
    """AST node representing a Table.AddColumn operation.

    Fields:
    - table: a table identifier or previous AST node
    - new_column: name of the new column to create
    - expression: an expression string describing how to compute the column
    """

    table: Any
    new_column: str
    expression: str

    def __repr__(self) -> str:
        tbl = getattr(self.table, "__name__", None) or repr(self.table)
        return (
            f"AddColumn(table={tbl}, new_column={self.new_column!r}, "
            f"expression={self.expression!r})"
        )


@dataclass
class RenameColumns:
    """AST node representing a Table.RenameColumns operation.

    Fields:
    - table: a table identifier or previous AST node
    - mapping: dict mapping existing column names to new names
    """

    table: Any
    mapping: Dict[str, str]

    def __repr__(self) -> str:
        tbl = getattr(self.table, "__name__", None) or repr(self.table)
        return f"RenameColumns(table={tbl}, mapping={self.mapping})"


@dataclass
class Group:
    """AST node representing a Table.Group operation.

    Fields:
    - table: a table identifier or previous AST node
    - keys: list of column names to group by
        - aggs: dict mapping output column name to aggregation expression.
            Example: {'count': 'COUNT(id)'}
    """

    table: Any
    keys: List[str]
    aggs: Dict[str, str]

    def __repr__(self) -> str:
        tbl = getattr(self.table, "__name__", None) or repr(self.table)
        keys = ", ".join(self.keys)
        return f"Group(table={tbl}, keys=[{keys}], aggs={self.aggs})"


@dataclass
class Join:
    """AST node representing a Table.Join operation.

    Fields:
    - left: left table identifier or previous AST node
    - right: right table identifier or AST node
    - on: dict mapping left->right column names for the join condition
    - kind: join type e.g. 'inner', 'left', 'right', 'full'
    """

    left: Any
    right: Any
    on: Dict[str, str]
    kind: str = "inner"

    def __repr__(self) -> str:
        left = getattr(self.left, "__name__", None) or repr(self.left)
        right = getattr(self.right, "__name__", None) or repr(self.right)
        return f"Join(left={left}, right={right}, on={self.on}, " f"kind={self.kind!r})"


@dataclass
class Pivot:
    """AST node representing a Table.Pivot operation.

    Fields:
    - table: a table identifier or previous AST node
    - pivot_column: the column whose values become new columns
    - value_column: the column providing values for the pivoted columns
    - agg: aggregation expression (e.g. 'SUM') or string describing aggregation
    - values: optional list of values to pivot into columns
    """

    table: Any
    pivot_column: str
    value_column: str
    agg: str
    values: List[str] | None = None

    def __repr__(self) -> str:
        tbl = getattr(self.table, "__name__", None) or repr(self.table)
        vals = ", ".join(self.values) if self.values else "None"
        return (
            f"Pivot(table={tbl}, pivot_column={self.pivot_column!r}, "
            f"value_column={self.value_column!r}, agg={self.agg!r}, values={vals})"
        )


@dataclass
class Unpivot:
    """AST node representing a Table.Unpivot operation.

    Fields:
    - table: a table identifier or previous AST node
    - columns: list of column names to unpivot into attribute/value rows
    - attribute_column: name of the output attribute column (e.g. 'attribute')
    - value_column: name of the output value column (e.g. 'value')
    """

    table: Any
    columns: List[str]
    attribute_column: str
    value_column: str

    def __repr__(self) -> str:
        tbl = getattr(self.table, "__name__", None) or repr(self.table)
        cols = ", ".join(self.columns)
        return (
            f"Unpivot(table={tbl}, columns=[{cols}], "
            f"attribute_column={self.attribute_column!r}, "
            f"value_column={self.value_column!r})"
        )


@dataclass
class Buffer:
    """AST node representing a Table.Buffer operation.

    Fields:
    - table: a table identifier or previous AST node

    Buffer forces materialization of the table into DuckDB,
    preventing further query folding for upstream operations.
    This matches M's Table.Buffer semantics.
    """

    table: Any

    def __repr__(self) -> str:
        tbl = getattr(self.table, "__name__", None) or repr(self.table)
        return f"Buffer(table={tbl})"
