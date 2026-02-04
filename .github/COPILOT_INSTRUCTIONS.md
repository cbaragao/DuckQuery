## DuckQuery — Copilot Repository Instructions

This file mirrors the project-level Copilot instructions and is placed where GitHub expects repository instructions to live.

Project goal
- Build `DuckQuery`: a small, M-flavored query/prep layer that compiles high-level dataset transformations into DuckDB SQL for fast, ad-hoc inquiry and data preparation.

Daily refactoring goals
- Triage failing tests and implement minimal, well-scoped fixes.
- Preserve behavioral compatibility with pandas where tests expect pandas semantics (e.g., quantile interpolation).
- Improve template generation for robust SQL (escape/formatting/reserved words) and make joins predictable.

What we've done
- Fixed dataframe registration flow and normalization of duplicate column names.
- Tightened Jinja2 templates to remove superfluous blank lines and ensure consistent clause rendering.

What's left / roadmap
- Make column-normalization optional and configurable.
- Add more robust escaping for SQL reserved words and identifier quoting.
- Implement richer M-inspired transformation primitives and ensure query folding where possible.

How to work with me (the copilot)
- Make small, test-driven changes.
- Run focused tests locally: `python -m pytest tests/test_file.py::TestClass::test_name -q`.
- When refactoring, prefer minimal, reversible changes and update `Historical/LESSONS.md` with discoveries.

Verb Naming Convention
- Canonical API names follow M-style PascalCase with a module prefix, for example `Table.SelectRows`, `Table.AddColumn`, and `Table.Pivot`.
- No ergonomic/dplyr aliases: expose canonical M verb names only. Avoid providing snake_case aliases or multiple synonyms for the same operation.
- Group verbs by module (`Table.*`, `Value.*`, `Query.*`) and follow the Verb+Noun pattern (e.g., `SelectRows`, `AddColumn`).
- Use PascalCase for canonical public API names; pick a single canonical name per operation and avoid aliases.

When you add a new transform, update this convention list and document the canonical name in the API reference.
