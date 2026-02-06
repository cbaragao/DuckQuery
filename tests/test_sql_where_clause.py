import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.emit import where_clause


def test_where_clause_single_condition():
    assert where_clause(['"age" >= 30']) == 'WHERE "age" >= 30'


def test_where_clause_multiple_conditions():
    result = where_clause(['"age" >= 30', "\"city\" = 'NYC'"])
    assert result == 'WHERE "age" >= 30 AND "city" = \'NYC\''


def test_where_clause_empty():
    assert where_clause([]) == ""
