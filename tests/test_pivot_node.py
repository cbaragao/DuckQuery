import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from m_ast.nodes import Pivot


def test_pivot_repr_and_fields():
    node = Pivot(table='T', pivot_column='category', value_column='value', agg='SUM', values=['A', 'B'])
    assert node.table == 'T'
    assert node.pivot_column == 'category'
    assert 'Pivot' in repr(node)
    assert 'category' in repr(node)
    assert 'SUM' in repr(node)
