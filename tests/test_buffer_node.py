"""Focused unit test for m_ast.nodes.Buffer AST node."""

from src.m_ast.nodes import Buffer


def test_buffer_node_constructor_and_repr():
    """Test Buffer node can be constructed with a table and has a simple repr."""
    # Create a Buffer node with a simple table identifier
    node = Buffer(table="employees")

    # Verify the node has the expected fields
    assert node.table == "employees"

    # Verify repr is clean and informative
    repr_str = repr(node)
    assert "Buffer" in repr_str
    assert "employees" in repr_str
    assert repr_str == "Buffer(table='employees')"


def test_buffer_node_with_mock_table_object():
    """Test Buffer node works with a table-like object."""

    class MockTable:
        __name__ = "MockEmployees"

    mock_tbl = MockTable()
    node = Buffer(table=mock_tbl)

    assert node.table == mock_tbl

    # Verify repr extracts __name__ if available
    repr_str = repr(node)
    assert "Buffer" in repr_str
    assert "MockEmployees" in repr_str
