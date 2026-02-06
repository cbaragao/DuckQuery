import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.emit import unpivot_basic


def test_unpivot_basic_two_columns():
    result = unpivot_basic(
        table_name="sales",
        columns=["Q1", "Q2"],
        attribute_column="quarter",
        value_column="amount",
    )
    assert 'SELECT \'Q1\' AS "quarter", "Q1" AS "amount" FROM "sales"' in result
    assert 'SELECT \'Q2\' AS "quarter", "Q2" AS "amount" FROM "sales"' in result
    assert " UNION ALL " in result


def test_unpivot_basic_three_columns():
    result = unpivot_basic(
        table_name="data",
        columns=["col1", "col2", "col3"],
        attribute_column="attribute",
        value_column="value",
    )
    assert 'SELECT \'col1\' AS "attribute", "col1" AS "value" FROM "data"' in result
    assert 'SELECT \'col2\' AS "attribute", "col2" AS "value" FROM "data"' in result
    assert 'SELECT \'col3\' AS "attribute", "col3" AS "value" FROM "data"' in result
    # Should have 2 UNION ALLs for 3 columns
    assert result.count(" UNION ALL ") == 2


def test_unpivot_basic_single_column():
    result = unpivot_basic(
        table_name="table",
        columns=["only_col"],
        attribute_column="attr",
        value_column="val",
    )
    assert result == 'SELECT \'only_col\' AS "attr", "only_col" AS "val" FROM "table"'
    assert " UNION ALL " not in result


def test_unpivot_basic_no_columns():
    import pytest

    with pytest.raises(ValueError, match="requires a non-empty 'columns' list"):
        unpivot_basic("table", [], "attr", "val")
