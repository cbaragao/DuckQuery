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

2026-02-04

- Implemented `m_ast.nodes.Pivot` as an AST node with fields: `pivot_column`, `value_column`, `agg`, and optional `values` list. Added focused unit test and verified full-suite regression tests passed locally (76 tests).
- Follow the iterative workflow in `.github/PROJECT_PLAN.md` for future atomized items: focused test -> iterate -> full regression -> docs -> commit.

Typing and CI updates (2026-02-04)

- Added CI and linter configuration: `black`, `flake8`, `mypy`, and a GitHub Actions workflow.
- Ran `black` to format code; adjusted style and a few long f-strings.
- Tightened `mypy` config (`no_implicit_optional`, warnings) and fixed typing issues in `src/main.py`:
  - Annotated `registered_tables` and `self.value`.
  - Updated methods to return `List` consistently and used `Optional[float]` for `self.value`.
  - Handled `fetchone()` possibly returning `None` and guarded arithmetic when values are `None`.
  - Ran `mypy` until no issues remain locally.

Lessons learned:

- Running linters in a project with many third-party packages can surface issues in `site-packages`; always exclude virtualenv folders in linter configs (`exclude = .venv`).
- `mypy`'s `no_implicit_optional` is stricter but helps find real None-handling bugs; prefer to annotate optional returns explicitly.
- Use defensive coding when consuming DB results (e.g., `fetchone()` may return `None`).
- Add `pre-commit` to enforce formatting and catch issues before commits.

Additional lessons (2026-02-04 updates)

- When adding small, focused AST nodes (`RenameColumns`, `Group`, `Join`, `Pivot`, `Unpivot`), follow the one-feature/one-test loop: add node, add focused unit test, run focused test, run full suite, then update docs and the project plan. The `scripts/mark_project_plan.py` helper can be used to mark items automatically.
- Pre-commit `mypy` hooks can fail with "duplicate module" errors unless mypy can resolve the package base; set `MYPYPATH=src` or use `--explicit-package-bases`/`--namespace-packages` and ensure `pass_filenames: false` when invoking package-based checks.
- Running `pre-commit` in a repo may modify files (e.g., `black`) before commit; handle reformatting in the same workflow (hooks run automatically during `git commit`).
- Add a small CI job step that runs the project-plan marker after tests succeed on `master` to keep `.github/PROJECT_PLAN.md` in sync automatically.
- When scripts modify checklist files, preserve existing indentation — use a regex that keeps leading whitespace and only normalizes the hyphen and checkbox to avoid accidental formatting diffs.

2026-02-05

- Fixed a broken inline checklist token in `.github/PROJECT_PLAN.md` (preserved backticks and avoided splitting inline code across lines).
- Lessons: avoid breaking inline code or fenced tokens across lines; run `markdownlint` early; add `.markdownlintignore` to skip virtualenv/vendor files; prefer spaces over hard tabs in markdown; preserve indentation when auto-editing checklists.
- Implemented `m_ast.nodes.Buffer` AST node with focused unit tests. Buffer forces table materialization, preventing further query folding (matches M's `Table.Buffer` semantics). Full test suite: 83 passed.
- Implemented `ast.explain_step(step)` to return human-readable descriptions of AST transformation steps. Added 9 focused unit tests covering all node types. Full test suite: 92 passed.
- Fixed pre-commit config warnings: removed deprecated `env:` key from mypy hook (replaced with `additional_dependencies: []`) and removed deprecated `stages: [commit]` from markdownlint hook.
- Verified `sql.emit.from_clause(table_name)` implementation (already existed with 2 focused unit tests). Function emits FROM clause with quoted table names. Full test suite: 92 passed.
- Implemented `sql.emit.where_clause(conditions)` to emit WHERE fragment for simple conditions. Added 3 focused unit tests (single condition, multiple conditions AND-joined, empty list). Full test suite: 95 passed.
- Implemented `sql.emit.join_clause(join)` to emit SQL JOIN clauses for Join AST nodes. Supports inner/left/right/full joins with multiple ON conditions. Added 4 focused unit tests. Full test suite: 99 passed.
- Implemented `sql.emit.group_by_clause(columns)` to emit GROUP BY fragment. Added 3 focused unit tests (single column, multiple columns, empty list). Full test suite: 102 passed.
- Implemented `sql.emit.aggregate_fn(name, arg)` to map aggregate functions (SUM/COUNT/AVG/MIN/MAX) to SQL. Handles COUNT(*) special case and validates function names. Added 8 focused unit tests. Full test suite: 110 passed.
- Implemented `sql.emit.order_by_clause(orderings)` to emit ORDER BY fragment for column/direction pairs. Validates direction (ASC/DESC) and is case-insensitive. Added 6 focused unit tests. Full test suite: 116 passed.
- Implemented `sql.emit.limit_offset(limit, offset)` to emit LIMIT/OFFSET fragments. Handles None, zero, and negative values correctly. Added 8 focused unit tests. Full test suite: 124 passed.
- Implemented `sql.emit.pivot_basic(params)` to generate basic pivot SQL using CASE expressions. Takes table, pivot column, value column, aggregate function, and list of values. Added 4 focused unit tests. Full test suite: 128 passed.
- Implemented `sql.emit.unpivot_basic(params)` to generate basic unpivot SQL using UNION ALL. Takes table, list of columns to unpivot, attribute column name, and value column name. Added 4 focused unit tests. Full test suite: 132 passed.
- Pre-commit workflow: To avoid black reformatting failures on commit, run `black src/ tests/` BEFORE `git add -A` to format files first, then stage and commit. This prevents the pre-commit hook from modifying already-staged files.
- Implemented `ident.quote(name)` to safely quote SQL identifiers. Escapes embedded double quotes by doubling them. Added 7 focused unit tests. Full test suite: 139 passed.
