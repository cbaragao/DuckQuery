import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from m_ast.nodes import SelectColumns
from m_ast.emit import emit_selectcolumns


def test_emit_selectcolumns_simple():
    node = SelectColumns(table='my_table', columns=['id', 'name'])
    sql = emit_selectcolumns(node)
    assert sql.strip() == 'SELECT "id", "name" FROM my_table'
