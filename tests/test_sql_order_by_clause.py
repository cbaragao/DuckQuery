import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.emit import order_by_clause


def test_order_by_clause_single_asc():
    assert order_by_clause([("name", "ASC")]) == 'ORDER BY "name" ASC'


def test_order_by_clause_single_desc():
    assert order_by_clause([("age", "DESC")]) == 'ORDER BY "age" DESC'


def test_order_by_clause_multiple():
    result = order_by_clause([("region", "ASC"), ("score", "DESC")])
    assert result == 'ORDER BY "region" ASC, "score" DESC'


def test_order_by_clause_case_insensitive():
    assert order_by_clause([("name", "asc")]) == 'ORDER BY "name" ASC'
    assert order_by_clause([("name", "desc")]) == 'ORDER BY "name" DESC'


def test_order_by_clause_empty():
    assert order_by_clause([]) == ""


def test_order_by_clause_invalid_direction():
    import pytest

    with pytest.raises(ValueError, match="Invalid sort direction"):
        order_by_clause([("name", "RANDOM")])
