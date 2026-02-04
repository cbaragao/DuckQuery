import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from m_ast.nodes import AddColumn


def test_addcolumn_repr_and_fields():
    node = AddColumn(table='my_table', new_column='age_plus_one', expression='age + 1')
    assert node.table == 'my_table'
    assert node.new_column == 'age_plus_one'
    assert node.expression == 'age + 1'
    r = repr(node)
    assert 'AddColumn' in r
    assert 'age + 1' in r
