#!/usr/bin/env python3
"""Mark an atomized checklist item in .github/PROJECT_PLAN.md as completed.

Usage:
    python -m scripts.mark_project_plan \
        --task "ast.nodes.Unpivot" [--commit] [--push]

The script looks for the first unchecked checklist line and replaces the leading
"- [ ]" with "- [x]".

It will only modify a line that contains the task text wrapped in backticks (for
example, `ast.nodes.Unpivot`). If `--commit` is passed the script stages and
commits the modified file. If `--push` is passed it will also push the commit to
the current branch.
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path
import sys

PROJECT_PLAN = Path(__file__).resolve().parents[1] / ".github" / "PROJECT_PLAN.md"


def mark_task(task: str) -> bool:
    text = PROJECT_PLAN.read_text(encoding="utf8")
    target = f"`{task}`"
    lines = text.splitlines()
    changed = False
    for i, line in enumerate(lines):
        if "- [ ]" in line and target in line:
            # Normalize indentation: keep leading whitespace but ensure hyphen
            # immediately follows indentation and a single space after hyphen.
            lines[i] = re.sub(r"^(\s*)-\s*\[ \]", r"\1- [x]", line, count=1)
            changed = True
            break
    if not changed:
        return False
    PROJECT_PLAN.write_text("\n".join(lines) + "\n", encoding="utf8")
    return True


def git_commit_and_push(commit: bool, push: bool, task: str | None = None) -> None:
    if not commit and not push:
        return
    subprocess.run(["git", "add", str(PROJECT_PLAN)], check=True)
    if commit:
        msg = (
            f"PROJECT_PLAN: mark {task} as completed"
            if task
            else "PROJECT_PLAN: update"
        )
        subprocess.run(["git", "commit", "-m", msg], check=True)
    if push:
        subprocess.run(["git", "push", "origin", "HEAD"], check=True)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--task", required=True, help="Task name (e.g. ast.nodes.Unpivot)")
    p.add_argument("--commit", action="store_true", help="Stage and commit the change")
    p.add_argument("--push", action="store_true", help="Push the commit to origin")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not PROJECT_PLAN.exists():
        print("PROJECT_PLAN.md not found at", PROJECT_PLAN, file=sys.stderr)
        raise SystemExit(2)
    ok = mark_task(args.task)
    if not ok:
        print(f"Task '{args.task}' not found or already marked.")
        raise SystemExit(1)
    print(f"Marked '{args.task}' as completed in {PROJECT_PLAN}")
    try:
        git_commit_and_push(args.commit, args.push)
    except subprocess.CalledProcessError as e:
        print("Git command failed:", e, file=sys.stderr)
        raise
