import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.emit import pivot_basic


def test_pivot_basic_sum():
    result = pivot_basic(
        table_name="sales",
        pivot_column="region",
        value_column="amount",
        agg="SUM",
        values=["East", "West"],
    )
    assert 'FROM "sales"' in result
    assert 'SUM(CASE WHEN "region" = \'East\' THEN "amount" END) AS "East"' in result
    assert 'SUM(CASE WHEN "region" = \'West\' THEN "amount" END) AS "West"' in result


def test_pivot_basic_count():
    result = pivot_basic(
        table_name="data",
        pivot_column="category",
        value_column="id",
        agg="COUNT",
        values=["A", "B", "C"],
    )
    assert 'FROM "data"' in result
    assert 'COUNT(CASE WHEN "category" = \'A\' THEN "id" END) AS "A"' in result
    assert 'COUNT(CASE WHEN "category" = \'B\' THEN "id" END) AS "B"' in result
    assert 'COUNT(CASE WHEN "category" = \'C\' THEN "id" END) AS "C"' in result


def test_pivot_basic_avg():
    result = pivot_basic(
        table_name="scores",
        pivot_column="subject",
        value_column="score",
        agg="avg",
        values=["Math", "English"],
    )
    assert 'AVG(CASE WHEN "subject" = \'Math\' THEN "score" END) AS "Math"' in result
    assert (
        'AVG(CASE WHEN "subject" = \'English\' THEN "score" END) AS "English"' in result
    )


def test_pivot_basic_no_values():
    import pytest

    with pytest.raises(ValueError, match="requires a non-empty 'values' list"):
        pivot_basic("table", "col", "val", "SUM", values=None)

    with pytest.raises(ValueError, match="requires a non-empty 'values' list"):
        pivot_basic("table", "col", "val", "SUM", values=[])
