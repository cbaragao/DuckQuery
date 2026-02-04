import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.nodes import SelectRows


def test_selectrows_repr_and_fields():
    node = SelectRows(table="my_table", condition="age >= 30")
    assert node.table == "my_table"
    assert node.condition == "age >= 30"
    r = repr(node)
    assert "SelectRows" in r
    assert "age >= 30" in r
