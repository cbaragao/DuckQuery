import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import pytest
from m_ast.config import set_normalize_columns, get_normalize_columns


@pytest.fixture(autouse=True)
def restore_default():
    """Restore normalize_columns to True after each test."""
    yield
    set_normalize_columns(True)


def test_default_is_enabled():
    assert get_normalize_columns() is True


def test_set_false():
    set_normalize_columns(False)
    assert get_normalize_columns() is False


def test_set_true_explicitly():
    set_normalize_columns(False)
    set_normalize_columns(True)
    assert get_normalize_columns() is True


def test_normalization_applied_when_enabled():
    """run_query strips _1 suffixes when normalize_columns is True."""
    import pandas as pd
    from main import List, Jointype

    left = pd.DataFrame({"id": [1, 2], "val": [10, 20]})
    other = pd.DataFrame({"id": [1, 2], "label": ["a", "b"]})

    set_normalize_columns(True)
    with List(left) as lst:
        lst.register_table("other", other)
        result = lst.run_query(
            select=["id", "val", "other.id", "label"],
            joins=[
                {
                    "type": Jointype.INNER,
                    "table": "other",
                    "condition": "current_df.id = other.id",
                }
            ],
        ).data()

    assert not any(str(c).endswith("_1") for c in result.columns)


def test_normalization_skipped_when_disabled():
    """run_query preserves raw _1 suffixes when normalize_columns is False."""
    import pandas as pd
    from main import List, Jointype

    left = pd.DataFrame({"id": [1, 2], "val": [10, 20]})
    other = pd.DataFrame({"id": [1, 2], "label": ["a", "b"]})

    set_normalize_columns(False)
    with List(left) as lst:
        lst.register_table("other", other)
        result = lst.run_query(
            select=["id", "val", "other.id", "label"],
            joins=[
                {
                    "type": Jointype.INNER,
                    "table": "other",
                    "condition": "current_df.id = other.id",
                }
            ],
        ).data()

    assert any(str(c).endswith("_1") for c in result.columns)
