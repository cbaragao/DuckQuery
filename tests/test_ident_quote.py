import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.ident import quote


def test_quote_simple():
    assert quote("column") == '"column"'


def test_quote_with_underscore():
    assert quote("my_column") == '"my_column"'


def test_quote_with_number():
    assert quote("col123") == '"col123"'


def test_quote_with_spaces():
    assert quote("my column") == '"my column"'


def test_quote_with_special_chars():
    assert quote("col-name") == '"col-name"'
    assert quote("col.name") == '"col.name"'


def test_quote_with_embedded_quotes():
    # Double quotes should be escaped by doubling them
    assert quote('my"column') == '"my""column"'
    assert quote('test"quote"here') == '"test""quote""here"'


def test_quote_empty_string():
    import pytest

    with pytest.raises(ValueError, match="cannot be empty"):
        quote("")
