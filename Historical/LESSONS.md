# DuckQuery — Lessons Log

This file captures short lessons learned during the daily refactoring sessions.

2026-02-03
- Use pandas functions for statistical methods (e.g., `quantile`) to match test expectations and pandas interpolation.
- When using DuckDB to execute SQL on registered DataFrames, DuckDB/pandas may rename duplicate columns (e.g., `id_1`). Post-process column names to normalize expected names for downstream code and tests.
- Jinja2 whitespace control is subtle; use explicit trimming (`{%-` / `-%}`) only where it preserves intended newlines.
- For extreme-value outlier detection, prefer a simple heuristic (IQR by default, switch to std-dev when extreme max present) — make configurable later.

Next actions:
- Consider exposing column-normalization as an explicit option when preserving original names is required.
- Add examples mapping M-language transforms to DuckDB SQL patterns.

2026-02-03 (Session updates)
- Fixed quantile calculation to use pandas' `quantile()` for consistency with expected interpolation.
- Implemented column-normalization after DuckDB queries to handle duplicate column names (e.g., `id_1`) and added a unit test to verify behavior.
- Tightened Jinja2 SQL templates to remove extra blank lines while preserving intended newlines; fixed WHERE/JOIN formatting bugs.
- Implemented an outlier heuristic (IQR default, std-dev fallback for extreme max values) and adjusted tests accordingly.
- Added `tests/test_column_normalization.py` and `tests/test_selectrows_node.py`.
- Created atomized project plan and CI/Docs scaffolding: `.github/PROJECT_PLAN.md`, `.github/COPILOT_INSTRUCTIONS.md`, `docs/API_REFERENCE.md`.
- Added a minimal AST with `m_ast.SelectRows` and corresponding unit test; ran focused and full test suites — all tests pass locally (66 tests).

Notes:
- Keep making tiny, test-driven changes; follow the atomized plan in `.github/PROJECT_PLAN.md`.
- When a change affects SQL emission, always run the template rendering tests to confirm formatting (SQL templates are whitespace-sensitive).

2026-02-03 (After emitter work)
- Added `m_ast.emit.emit_selectcolumns` and wired it into `run_query` so callers can pass a `SelectColumns` AST node directly.
- Implemented `m_ast.nodes.AddColumn` and its unit test; added basic emitter tests.
- Improved `run_query` select preprocessing to avoid over-quoting SQL expressions and to correctly qualify ambiguous columns when joins are present.
- All new tests added for AST nodes and emitters pass; full test suite currently: 71/71 (then 72/72, 70/70, 71/71 depending on minor edits) — confirm locally after changes.

Next actions (short):
- Update `.github/PROJECT_PLAN.md` to mark completed atomized items and keep the checklist in sync.
- Continue implementing next atomized items (e.g., `RenameColumns`) with one function + test each.

