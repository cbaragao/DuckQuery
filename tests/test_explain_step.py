"""Focused unit test for m_ast.explain_step function."""

from src.m_ast import explain_step
from src.m_ast.nodes import (
    SelectRows,
    SelectColumns,
    AddColumn,
    RenameColumns,
    Group,
    Join,
    Pivot,
    Unpivot,
    Buffer,
)


def test_explain_step_selectrows():
    """Test explain_step returns a description for SelectRows."""
    step = SelectRows(table="employees", condition="age >= 30")
    desc = explain_step(step)
    assert "SelectRows" in desc
    assert "age >= 30" in desc
    assert desc == "SelectRows: filter by age >= 30"


def test_explain_step_selectcolumns():
    """Test explain_step returns a description for SelectColumns."""
    step = SelectColumns(table="employees", columns=["name", "salary"])
    desc = explain_step(step)
    assert "SelectColumns" in desc
    assert "name" in desc
    assert "salary" in desc
    assert desc == "SelectColumns: project [name, salary]"


def test_explain_step_addcolumn():
    """Test explain_step returns a description for AddColumn."""
    step = AddColumn(table="employees", new_column="bonus", expression="salary * 0.1")
    desc = explain_step(step)
    assert "AddColumn" in desc
    assert "bonus" in desc
    assert "salary * 0.1" in desc
    assert desc == "AddColumn: add bonus = salary * 0.1"


def test_explain_step_renamecolumns():
    """Test explain_step returns a description for RenameColumns."""
    step = RenameColumns(table="employees", mapping={"old_name": "new_name"})
    desc = explain_step(step)
    assert "RenameColumns" in desc
    assert "old_name->new_name" in desc


def test_explain_step_group():
    """Test explain_step returns a description for Group."""
    step = Group(
        table="sales",
        keys=["region"],
        aggs={"total": "SUM(amount)", "count": "COUNT(*)"},
    )
    desc = explain_step(step)
    assert "Group" in desc
    assert "region" in desc
    assert "total=SUM(amount)" in desc


def test_explain_step_join():
    """Test explain_step returns a description for Join."""
    step = Join(
        left="employees",
        right="departments",
        on={"dept_id": "id"},
        kind="inner",
    )
    desc = explain_step(step)
    assert "Join" in desc
    assert "inner" in desc
    assert "dept_id=id" in desc


def test_explain_step_pivot():
    """Test explain_step returns a description for Pivot."""
    step = Pivot(
        table="sales",
        pivot_column="product",
        value_column="revenue",
        agg="SUM",
    )
    desc = explain_step(step)
    assert "Pivot" in desc
    assert "product" in desc
    assert "revenue" in desc


def test_explain_step_unpivot():
    """Test explain_step returns a description for Unpivot."""
    step = Unpivot(
        table="sales",
        columns=["Q1", "Q2", "Q3"],
        attribute_column="quarter",
        value_column="revenue",
    )
    desc = explain_step(step)
    assert "Unpivot" in desc
    assert "Q1" in desc
    assert "quarter" in desc
    assert "revenue" in desc


def test_explain_step_buffer():
    """Test explain_step returns a description for Buffer."""
    step = Buffer(table="employees")
    desc = explain_step(step)
    assert "Buffer" in desc
    assert "materialize" in desc
    assert desc == "Buffer: materialize table (prevent query folding)"
