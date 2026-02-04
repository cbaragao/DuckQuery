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
        return f"AddColumn(table={tbl}, new_column={self.new_column!r}, expression={self.expression!r})"


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
    - aggs: dict mapping output column name to aggregation expression (e.g. {'count': 'COUNT(id)'})
    """
    table: Any
    keys: List[str]
    aggs: Dict[str, str]

    def __repr__(self) -> str:
        tbl = getattr(self.table, "__name__", None) or repr(self.table)
        keys = ", ".join(self.keys)
        return f"Group(table={tbl}, keys=[{keys}], aggs={self.aggs})"
