import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.nodes import RenameColumns


def test_renamecolumns_repr():
    node = RenameColumns(table="T", mapping={"a": "alpha", "b": "beta"})
    assert repr(node) == "RenameColumns(table='T', mapping={'a': 'alpha', 'b': 'beta'})"
