import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.emit import select_clause


def test_select_clause_basic():
    assert select_clause(["id", "name"]) == 'SELECT "id", "name"'


def test_select_clause_empty():
    assert select_clause([]) == "SELECT *"
