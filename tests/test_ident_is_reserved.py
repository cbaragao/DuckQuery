import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.ident import is_reserved


def test_reserved_lowercase():
    assert is_reserved("select") is True


def test_reserved_uppercase():
    assert is_reserved("SELECT") is True


def test_reserved_mixed_case():
    assert is_reserved("From") is True


def test_reserved_words_sample():
    for word in (
        "where",
        "join",
        "group",
        "order",
        "limit",
        "offset",
        "null",
        "true",
        "false",
    ):
        assert is_reserved(word) is True, f"Expected '{word}' to be reserved"


def test_not_reserved_plain_identifier():
    assert is_reserved("my_column") is False


def test_not_reserved_partial_match():
    # 'selector' contains 'select' but is not itself reserved
    assert is_reserved("selector") is False


def test_not_reserved_empty_string():
    assert is_reserved("") is False
