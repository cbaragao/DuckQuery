import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.cols import normalize_suffixes


def test_single_suffix_stripped():
    assert normalize_suffixes(["name_1"]) == ["name"]


def test_multiple_distinct_suffixes_stripped():
    assert normalize_suffixes(["name_1", "value_2"]) == ["name", "value"]


def test_suffix_conflicts_with_original():
    # "id_1" would strip to "id", but "id" already exists — keep original
    assert normalize_suffixes(["id", "id_1"]) == ["id", "id_1"]


def test_two_suffixes_same_base_kept():
    # both strip to "x" — collision, keep both
    assert normalize_suffixes(["x_1", "x_2"]) == ["x_1", "x_2"]


def test_no_suffixes_unchanged():
    assert normalize_suffixes(["alpha", "beta", "gamma"]) == ["alpha", "beta", "gamma"]


def test_empty_list():
    assert normalize_suffixes([]) == []


def test_suffix_zero_not_stripped():
    # "_0" is a numeric suffix — strip it when safe
    assert normalize_suffixes(["col_0"]) == ["col"]


def test_non_numeric_suffix_unchanged():
    assert normalize_suffixes(["col_a", "col_b"]) == ["col_a", "col_b"]
