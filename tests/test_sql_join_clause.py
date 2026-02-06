import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from m_ast.emit import join_clause
from m_ast.nodes import Join


def test_join_clause_inner():
    join = Join(left="users", right="orders", on={"id": "user_id"}, kind="inner")
    result = join_clause(join)
    assert result == 'INNER JOIN "orders" ON "id" = "user_id"'


def test_join_clause_left():
    join = Join(left="users", right="orders", on={"id": "user_id"}, kind="left")
    result = join_clause(join)
    assert result == 'LEFT JOIN "orders" ON "id" = "user_id"'


def test_join_clause_multiple_on():
    join = Join(
        left="users",
        right="orders",
        on={"id": "user_id", "region": "order_region"},
        kind="inner",
    )
    result = join_clause(join)
    assert 'INNER JOIN "orders"' in result
    assert '"id" = "user_id"' in result
    assert '"region" = "order_region"' in result
    assert " AND " in result


def test_join_clause_full_outer():
    join = Join(left="users", right="orders", on={"id": "user_id"}, kind="full")
    result = join_clause(join)
    assert result == 'FULL OUTER JOIN "orders" ON "id" = "user_id"'
