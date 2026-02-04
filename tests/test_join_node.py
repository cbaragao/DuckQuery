import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from m_ast.nodes import Join


def test_join_repr_and_fields():
    node = Join(left='L', right='R', on={'id': 'id'}, kind='inner')
    assert node.left == 'L'
    assert node.right == 'R'
    r = repr(node)
    assert 'Join' in r
    assert "'id': 'id'" in r or 'id' in r
    assert "'inner'" in r
