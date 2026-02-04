"""Minimal AST package for DuckQuery (M-like transforms).

This package will host tiny AST node classes used to compose transforms before
emitting SQL. Keep nodes minimal and data-focused.
"""

from .nodes import SelectRows, SelectColumns, AddColumn

__all__ = ["SelectRows", "SelectColumns", "AddColumn"]
