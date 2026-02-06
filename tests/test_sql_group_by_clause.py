import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.emit import group_by_clause


def test_group_by_clause_single_column():
    assert group_by_clause(["region"]) == 'GROUP BY "region"'


def test_group_by_clause_multiple_columns():
    result = group_by_clause(["region", "category"])
    assert result == 'GROUP BY "region", "category"'


def test_group_by_clause_empty():
    assert group_by_clause([]) == ""
