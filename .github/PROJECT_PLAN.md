# DuckQuery — Project Plan (Atomized)

This plan is the canonical, atomized project plan: every task is intentionally tiny (one function/method and a focused unit test).

Core Microsoft Learn references

- Query folding basics: [Query folding overview](https://learn.microsoft.com/en-us/power-query/query-folding-basics#query-folding-overview)
- Table functions index (pivot/unpivot/group/others): [Table functions](https://learn.microsoft.com/en-us/powerquery-m/table-functions#column-operations)
- Pivot columns: [Pivot columns](https://learn.microsoft.com/en-us/power-query/pivot-columns)
- Unpivot columns: [Unpivot columns](https://learn.microsoft.com/en-us/power-query/unpivot-column)

Atomized checklist (implement one function/method + one unit test per item)

- [x] `ast.nodes.SelectRows`: constructor + simple repr
- [x] `ast.nodes.SelectColumns`: constructor + simple repr
- [x] `ast.nodes.AddColumn`: constructor + simple repr
- [x] `ast.nodes.RenameColumns`: constructor + simple repr
- [x] `ast.nodes.Group`: constructor + simple repr
- [x] `ast.nodes.Join`: constructor + simple repr
- [x] `ast.nodes.Pivot`: constructor + simple repr
- [x] `ast.nodes.Unpivot`: constructor + simple repr
- [x] `ast.nodes.Buffer`: constructor + simple repr
- [x] `ast.explain_step(step)`: returns a short description string
- [x] `sql.emit.select_clause(columns)`: emit SELECT fragment
- [x] `sql.emit.from_clause(table_name)`: emit FROM fragment
- [x] `sql.emit.where_clause(conditions)`: emit WHERE fragment for simple conditions
- [x] `sql.emit.join_clause(join)`: emit SQL for a single JOIN
- [x] `sql.emit.group_by_clause(columns)`: emit GROUP BY fragment
- [x] `sql.emit.aggregate_fn(name, arg)`: map SUM/COUNT/AVG to SQL
- [x] `sql.emit.order_by_clause(orderings)`: emit ORDER BY fragment
- [x] `sql.emit.limit_offset(limit, offset)`: emit LIMIT/OFFSET fragments (handle 0)
- [x] `sql.emit.pivot_basic(params)`: generate basic pivot SQL
- [x] `sql.emit.unpivot_basic(params)`: generate basic unpivot SQL
- [x] `ident.quote(name)`: safely quote an identifier
- [ ] `ident.is_reserved(name)`: detect common reserved words
- [ ] `cols.normalize_suffixes(columns)`: strip `_1`, `_2` suffixes when safe
- [ ] `tests.test_normalize_single_suffix()`: unit test for suffix stripper
- [ ] `config.set_normalize_columns(bool)`: toggle normalization flag
- [ ] `filter.parse_simple(expr)`: parse `col = value` or `col >= value` into AST
- [ ] `addcol.translate_simple(expr)`: translate `col + 1` style expression
- [ ] `rename.apply_mapping(df, mapping)`: apply rename mapping to dataframe and SQL aliases
- [ ] `group.emit_single_key_count(key)`: emit SQL for COUNT grouped by `key`
- [ ] `join.emit_inner(join)`: emit SQL for an inner join with ON clause
- [ ] `tests.test_pivot_shape_basic()`: unit test asserting pivot output columns/rows
- [ ] `tests.test_unpivot_shape_basic()`: unit test asserting unpivot attribute/value result
- [ ] `materialize.register_temp(df, name)`: register df in DuckDB with a temp name
- [ ] `explain.format(sql, folded_steps)`: return multiline explain output
- [ ] `folding.can_fold_chain(steps)`: true/false for a simple SelectRows+SelectColumns chain
- [ ] `tests.test_partial_folding_detection()`: unit test for partial folding case
- [ ] `native.execute_passthrough(sql)`: execute native SQL without further translation
- [ ] `validate.basic_check(expr)`: return error for unsupported constructs
- [x] `ci.workflow.yaml`: workflow function that runs `pytest -q` (create CI config file)
- [x] `.pre-commit-config.yaml`: pre-commit hooks (black, flake8, mypy) added and validated
- [x] `setup.cfg` / `pyproject.toml`: linting and mypy configuration added
- [x] `requirements.txt`: updated from development venv with `pip freeze`
- [x] `README.md`: pre-commit install instructions added
- [x] `mypy`: tightened config and typing fixes applied (e.g., `src/main.py`)
- [ ] `docs.cookbook_select_where_join.md`: one-page examples mapping M-like ops to SQL
- [x] `lint.markdown`: add markdown linter (e.g., `remark-lint` / `markdownlint`) and fix repo warnings

How to work from this plan

- Implement one item at a time: function + single unit test.
- Run the focused test, then the full test suite: `python -m pytest -q`.
- Update this file and the project's TODOs when items are completed.

Development workflow (iterative single-feature development)

For each feature from the atomized checklist:

1. Add or update the single feature implementation (one small function/class).
2. Add one focused unit test that reproduces the desired behavior.
3. Run the focused test only: `python -m pytest -q tests/test_<feature>_node.py`. If it fails, iterate on the implementation until the focused test passes.
4. After the focused test passes, run the full test suite: `python -m pytest -q`. If any tests fail, fix regressions and re-run the full suite until all pass.
5. When the full suite passes, update `Historical/LESSONS.md` and `docs/API_REFERENCE.md`
   with a short entry describing the new feature and any usage notes. Optionally use
   `scripts/mark_project_plan.py --task "<module.item>" --commit --push` to automatically
   mark the corresponding item in `.github/PROJECT_PLAN.md` as completed and commit the
   change. Example:

      python -m scripts.mark_project_plan --task "ast.nodes.Unpivot" --commit --push

6. Commit the changes and push to the remote branch (or let the script handle commit/push).

Follow this loop for each atomized item to keep changes small and regressions easy to find.

Rationale

- Atomization keeps changes small, simplifies review, and ensures regressions are easy to find and fix.

Verb Naming Convention

- Canonical API names follow M-style PascalCase with a module prefix, for example `Table.SelectRows`, `Table.AddColumn`, and `Table.Pivot`.
- No ergonomic aliases: the project will expose only canonical M verb names. Do not provide dplyr/R-style snake_case aliases; this keeps the API faithful to M and avoids synonym confusion.
- Modules: group verbs by module (e.g. `Table.*`, `Value.*`, `Query.*`).
- Verb form: use Verb+Noun (e.g. `SelectRows`, `AddColumn`, `RenameColumns`). Keep verbs single-responsibility and document side effects explicitly.
- Case & style: PascalCase for all public API names. Choose one canonical name per operation and avoid synonyms.

Example canonical names

- `Table.SelectRows`
- `Table.SelectColumns`
- `Table.AddColumn`
- `Table.RenameColumns`
- `Table.Group`
- `Table.Join`
- `Table.Pivot`
- `Table.Unpivot`

Document these conventions in the API reference and use the canonical names consistently across implementation and docs.
