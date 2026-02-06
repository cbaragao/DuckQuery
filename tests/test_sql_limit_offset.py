import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.emit import limit_offset


def test_limit_offset_limit_only():
    assert limit_offset(10, None) == "LIMIT 10"


def test_limit_offset_offset_only():
    assert limit_offset(None, 5) == "OFFSET 5"


def test_limit_offset_both():
    assert limit_offset(10, 5) == "LIMIT 10 OFFSET 5"


def test_limit_offset_both_none():
    assert limit_offset(None, None) == ""


def test_limit_offset_zero_limit():
    # Zero limit should be treated as "no limit"
    assert limit_offset(0, 5) == "OFFSET 5"


def test_limit_offset_zero_offset():
    # Zero offset should be treated as "no offset"
    assert limit_offset(10, 0) == "LIMIT 10"


def test_limit_offset_both_zero():
    assert limit_offset(0, 0) == ""


def test_limit_offset_negative_values():
    # Negative values should be ignored
    assert limit_offset(-1, 5) == "OFFSET 5"
    assert limit_offset(10, -1) == "LIMIT 10"
    assert limit_offset(-1, -1) == ""
