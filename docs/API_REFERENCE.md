# DuckQuery — API Reference

This document describes the canonical M-style API and the implemented SQL emit functions in DuckQuery.

## AST Nodes (m_ast.nodes)

AST nodes represent M-like transformation operations. All nodes are dataclasses with `__repr__` methods.

### Implemented Nodes

- `SelectRows(table, condition)` — Filter rows by a boolean condition expression
- `SelectColumns(table, columns)` — Project a subset of columns
- `AddColumn(table, new_column, expression)` — Add a computed column
- `RenameColumns(table, rename_map)` — Rename columns using a mapping dict
- `Group(table, keys, aggs)` — Group by key columns with aggregates
- `Join(left, right, on, kind)` — Join tables (supports inner/left/right/full)
- `Pivot(table, pivot_column, value_column, agg, values)` — Pivot attribute/value pairs
- `Unpivot(table, columns, attribute_col, value_col)` — Unpivot columns to rows
- `Buffer(table)` — Force table materialization (prevents further query folding)

## AST Utilities (m_ast)

### explain_step(step)

Returns a human-readable description string for an AST transformation step.

```python
from m_ast import explain_step, SelectRows

step = SelectRows(table="users", condition="age >= 30")
print(explain_step(step))
# Output: "SelectRows: filter by age >= 30"
```

## SQL Emit Functions (m_ast.emit)

Low-level SQL fragment generators for building queries.

### select_clause(columns)

Emit a SQL SELECT fragment for a list of column names.

- Returns `SELECT *` if columns list is empty
- Column names are double-quoted

```python
from m_ast.emit import select_clause

select_clause(["name", "age"])  # Returns: 'SELECT "name", "age"'
select_clause([])  # Returns: 'SELECT *'
```

### from_clause(table_name)

Emit a SQL FROM fragment for a table name.

- Table name is double-quoted
- Raises ValueError if table_name is empty

```python
from m_ast.emit import from_clause

from_clause("users")  # Returns: 'FROM "users"'
```

### where_clause(conditions)

Emit a SQL WHERE fragment for simple conditions.

- Returns empty string if conditions list is empty
- Conditions are joined with AND

```python
from m_ast.emit import where_clause

where_clause(['"age" >= 30', '"city" = \'NYC\''])
# Returns: 'WHERE "age" >= 30 AND "city" = \'NYC\''
```

### join_clause(join)

Emit a SQL JOIN clause for a Join AST node.

- Supports join kinds: inner, left, right, full
- ON conditions are built from the join.on dict mapping

```python
from m_ast.emit import join_clause
from m_ast.nodes import Join

join = Join(left="users", right="orders", on={"id": "user_id"}, kind="inner")
join_clause(join)  # Returns: 'INNER JOIN "orders" ON "id" = "user_id"'
```

### group_by_clause(columns)

Emit a SQL GROUP BY fragment for column names.

- Returns empty string if columns list is empty
- Column names are double-quoted

```python
from m_ast.emit import group_by_clause

group_by_clause(["region", "category"])
# Returns: 'GROUP BY "region", "category"'
```

### aggregate_fn(name, arg)

Map aggregate function names to SQL syntax.

- Supports: SUM, COUNT, AVG, MIN, MAX
- Case-insensitive
- Handles COUNT(*) as special case (no quoting)
- Raises ValueError for unsupported functions

```python
from m_ast.emit import aggregate_fn

aggregate_fn("SUM", "amount")  # Returns: 'SUM("amount")'
aggregate_fn("COUNT", "*")     # Returns: 'COUNT(*)'
aggregate_fn("avg", "price")   # Returns: 'AVG("price")'
```

### order_by_clause(orderings)

Emit a SQL ORDER BY fragment for column/direction pairs.

- Each ordering is a tuple of (column_name, direction)
- Direction must be ASC or DESC (case-insensitive)
- Returns empty string if orderings list is empty
- Raises ValueError for invalid directions

```python
from m_ast.emit import order_by_clause

order_by_clause([("name", "ASC"), ("age", "DESC")])
# Returns: 'ORDER BY "name" ASC, "age" DESC'
```

## Development Status

See [PROJECT_PLAN.md](../.github/PROJECT_PLAN.md) for the atomized task checklist and implementation status.

## References

- Query folding basics: [Query folding overview](https://learn.microsoft.com/en-us/power-query/query-folding-basics)
- Table functions: [Table functions](https://learn.microsoft.com/en-us/powerquery-m/table-functions)
- Pivot/Unpivot: [Pivot columns](https://learn.microsoft.com/en-us/power-query/pivot-columns) and [Unpivot columns](https://learn.microsoft.com/en-us/power-query/unpivot-column)
