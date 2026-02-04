# DuckQuery — API Reference (Canonical M verbs)

This stub lists canonical, M-style public API verbs (PascalCase) that DuckQuery will expose. Each function follows the `Module.Verb` pattern and returns a `Table` unless otherwise noted.

Core modules
- `Table` — table-level transforms
- `Value` — scalar/list operations
- `Query` — higher-level query composition / execution helpers

Table verbs
- `Table.SelectRows(table, condition)` -> Table
  - Filter rows by a boolean `condition` expression. Mirrors `Table.SelectRows` in Power Query.

- `Table.SelectColumns(table, columns)` -> Table
  - Project a subset of columns or reorder.

- `Table.AddColumn(table, newColumnName, expression)` -> Table
  - Add a computed column using an expression based on existing columns.

- `Table.RenameColumns(table, mapping)` -> Table
  - Rename columns using a mapping list of (oldName, newName).

- `Table.Group(table, keyColumns, aggregates)` -> Table
  - Group by key columns and compute aggregates (COUNT, SUM, AVG, etc.).

- `Table.Join(table1, table2, joinKind, condition)` -> Table
  - Perform SQL-style joins (Inner, Left, Right, Full) with an `ON` condition.

  - Pivot attribute/value pairs into columns; supports aggregate functions or "Don't aggregate" flow.
 `Table.Pivot(table, attributeColumn, valueColumn, aggregate, values=None)` -> Table

- `Table.Unpivot(table, columnsToUnpivot)` -> Table

- `Table.Buffer(table)` -> Table
  - Materialize the table (force registration/materialization in DuckDB) for non-foldable steps.

Query & utility verbs
- `Query.Run(ast_or_sql)` -> Table
  - Execute a composed AST or raw SQL against DuckDB and return a DataFrame.

- `Query.Explain(ast_or_sql)` -> str
  - Return generated SQL and folding decisions for debugging.

Identifier & validation helpers
- `Ident.Quote(name)` -> str
  - Safely quote identifier names for SQL emission.

- `Validate.Basic(expr)` -> None | raises
  - Validate M-like expressions for SQL-foldability; raise on unsupported constructs.

Notes & links
- This API is canonical and M-first. No aliases or dplyr-style names are provided.
- Refer to Power Query docs for semantics and edge-cases:
  - Query folding: https://learn.microsoft.com/en-us/power-query/query-folding-basics
  - Table functions: https://learn.microsoft.com/en-us/powerquery-m/table-functions
  - Pivot/Unpivot: https://learn.microsoft.com/en-us/power-query/pivot-columns and https://learn.microsoft.com/en-us/power-query/unpivot-column

Next steps
- Fill in function signatures in code, implement one function at a time (see `.github/PROJECT_PLAN.md` atomized checklist), and add unit tests that compare to pandas where applicable.
