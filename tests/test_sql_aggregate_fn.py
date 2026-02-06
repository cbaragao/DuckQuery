import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.emit import aggregate_fn


def test_aggregate_fn_sum():
    assert aggregate_fn("SUM", "amount") == 'SUM("amount")'


def test_aggregate_fn_count():
    assert aggregate_fn("COUNT", "id") == 'COUNT("id")'


def test_aggregate_fn_count_star():
    assert aggregate_fn("COUNT", "*") == "COUNT(*)"


def test_aggregate_fn_avg():
    assert aggregate_fn("AVG", "price") == 'AVG("price")'


def test_aggregate_fn_min():
    assert aggregate_fn("MIN", "score") == 'MIN("score")'


def test_aggregate_fn_max():
    assert aggregate_fn("MAX", "score") == 'MAX("score")'


def test_aggregate_fn_case_insensitive():
    assert aggregate_fn("sum", "amount") == 'SUM("amount")'
    assert aggregate_fn("Count", "id") == 'COUNT("id")'


def test_aggregate_fn_unsupported():
    import pytest

    with pytest.raises(ValueError, match="Unsupported aggregate function"):
        aggregate_fn("MEDIAN", "value")
