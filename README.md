# DuckQuery

A small experimental project that provides M-flavored, DuckDB-backed primitives for ad-hoc inquiry and data preparation.

Key pointers
- Repository Copilot instructions: [.github/COPILOT_INSTRUCTIONS.md](.github/COPILOT_INSTRUCTIONS.md)
- Development notes and lessons: [Historical/LESSONS.md](Historical/LESSONS.md)
- Tests: run `python -m pytest -q` from the project root; unit tests live in `tests/`.

- Development setup (pre-commit hooks)
	- Install developer dependencies into the project's virtualenv and enable pre-commit hooks to run formatters/linters automatically:

		```bash
		.venv/bin/python -m pip install -r requirements.txt
		.venv/bin/python -m pip install pre-commit
		.venv/bin/pre-commit install
		.venv/bin/pre-commit run --all-files
		```

	- This will run `black`, `flake8`, and `mypy` (as configured in `.pre-commit-config.yaml`) on commit and can be run manually with `pre-commit run --all-files`.

- Project plan (features & priorities): [.github/PROJECT_PLAN.md](.github/PROJECT_PLAN.md)

Consult the project plan and update completed items there and in the project's TODO list as we make progress.

If you're using GitHub Copilot, that tool will read `.github/COPILOT_INSTRUCTIONS.md` for repository-level guidance.
