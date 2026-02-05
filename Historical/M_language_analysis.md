# M Language (Power Query) — Analysis & High-Priority Items for DuckQuery

Summary

- The M language (Power Query / Power BI) is a functional, case-insensitive language designed for data transformation. Key concepts useful for `DuckQuery`:
  - Query Folding: pushing transformations back to the data source as composable steps to execute server-side.
  - Step-based transformations: `let` blocks with named steps composing a pipeline.
  - Table-centric primitives: `Table.SelectRows`, `Table.AddColumn`, `Table.Group`, `Table.Join`, `Table.Buffer`, `Table.TransformColumns`.
  - Lazy evaluation and pure functions encourage composability and predictable semantics.

High-priority items to include in DuckQuery

1. Query-Folding-aware planner
   - Aim: translate a chain of M-like transformations into a single DuckDB SQL statement where possible.
   - Start with a subset: filtering (`Table.SelectRows`), projection (`Table.SelectColumns`), joins (`Table.Join`), aggregations (`Table.Group`) and order/limit.

2. Step/`let` representation and named intermediate results
   - Provide an abstraction for naming steps; allow users to inspect generated SQL per step.
   - Support optional `Table.Buffer` semantics by forcing materialization into a temporary registered table.

3. Mapping M primitives to DuckDB SQL
   - `Table.SelectRows` -> WHERE
   - `Table.SelectColumns` -> SELECT columns
   - `Table.AddColumn` -> SELECT with expression AS col
   - `Table.RenameColumns` -> AS/column aliasing in SELECT
   - `Table.Join` -> JOIN clauses with ON
   - `Table.Group` -> GROUP BY + aggregate functions

4. Preserve pandas-compatible semantics where tests expect them
   - Quantile interpolation, NA handling, sort-stable behavior.

5. Safe identifier handling and folding heuristics
   - Quote identifiers properly; detect reserved keywords.
   - Provide fallbacks: if an operation cannot fold to SQL, materialize the current step into DuckDB temporary table.

6. Developer ergonomics
   - Provide `explain()` to show generated SQL and folding decisions per step.
   - Add debugging hooks to show which steps were folded vs materialized.

Roadmap suggestion (first 90 days)

- Week 1-2: Implement a small AST for M-like steps and mapping for selection/filter/group/join.
- Week 3: Query folding engine that emits DuckDB SQL for foldable chains and materializes non-foldable steps.
- Week 4: Add `explain()` and tests for folding behavior with varied inputs.

Notes

- Focus on a pragmatic subset. Full M language coverage is large; begin with commonly-used table primitives and expand.
- Documentation and examples are crucial: show M-like script and the generated SQL side-by-side.
