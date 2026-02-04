import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.nodes import Unpivot


def test_unpivot_repr_and_fields():
    node = Unpivot(
        table="T",
        columns=["A", "B"],
        attribute_column="attr",
        value_column="val",
    )
    assert node.table == "T"
    assert node.columns == ["A", "B"]
    assert "Unpivot" in repr(node)
    assert "attr" in repr(node)
    assert "val" in repr(node)
