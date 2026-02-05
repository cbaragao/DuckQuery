import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.emit import from_clause


def test_from_clause_basic():
    assert from_clause("users") == 'FROM "users"'


def test_from_clause_empty():
    import pytest

    with pytest.raises(ValueError):
        from_clause("")
