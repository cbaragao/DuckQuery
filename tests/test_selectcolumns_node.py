import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from m_ast.nodes import SelectColumns


def test_selectcolumns_repr_and_fields():
    node = SelectColumns(table='my_table', columns=['id', 'name'])
    assert node.table == 'my_table'
    assert node.columns == ['id', 'name']
    r = repr(node)
    assert 'SelectColumns' in r
    assert 'id' in r
    assert 'name' in r
