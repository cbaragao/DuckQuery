import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from m_ast.nodes import Group


def test_group_repr_and_fields():
    node = Group(table='T', keys=['id', 'category'], aggs={'cnt': 'COUNT(id)'})
    assert node.table == 'T'
    assert node.keys == ['id', 'category']
    assert 'Group' in repr(node)
    assert 'id' in repr(node)
    assert "'cnt': 'COUNT(id)'" in repr(node)
