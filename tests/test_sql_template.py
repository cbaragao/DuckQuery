import pytest
import sys
import os
from jinja2 import Environment, PackageLoader, select_autoescape

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import Jointype


class TestSQLTemplateRendering:
    """Test cases for SQL template rendering functionality"""
    
    @pytest.fixture
    def jinja_env(self):
        """Set up Jinja2 environment for template testing"""
        # We need to use the same environment setup as in main.py
        env = Environment(
            loader=PackageLoader("main"),
            autoescape=select_autoescape()
        )
        return env

    def test_basic_select_all(self, jinja_env):
        """Test basic SELECT * query"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],
            "table": "test_table",
            "where": [],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": []
        }
        
        query = template.render(**params)
        
        # Should contain basic SELECT * FROM table
        assert "SELECT\n    *\nFROM test_table" in query.strip()

    def test_select_specific_columns(self, jinja_env):
        """Test SELECT with specific columns"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": ["name", "age", "salary"],
            "table": "employees",
            "where": [],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": []
        }
        
        query = template.render(**params)
        
        assert "SELECT\n    name, age, salary\nFROM employees" in query

    def test_where_clause_single_condition(self, jinja_env):
        """Test WHERE clause with single condition"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],
            "table": "employees",
            "where": ["age >= 30"],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": []
        }
        
        query = template.render(**params)
        
        assert "WHERE\n    age >= 30" in query

    def test_where_clause_multiple_conditions(self, jinja_env):
        """Test WHERE clause with multiple conditions"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],
            "table": "employees",
            "where": ["age >= 30", "department = 'IT'", "salary > 50000"],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": []
        }
        
        query = template.render(**params)
        
        assert "WHERE\n    age >= 30 AND\n    department = 'IT' AND\n    salary > 50000" in query

    def test_group_by_clause(self, jinja_env):
        """Test GROUP BY clause"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": ["department", "COUNT(*) as count"],
            "table": "employees",
            "where": [],
            "group_by": ["department"],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": []
        }
        
        query = template.render(**params)
        
        assert "GROUP BY department" in query

    def test_group_by_multiple_columns(self, jinja_env):
        """Test GROUP BY with multiple columns"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": ["department", "location", "COUNT(*) as count"],
            "table": "employees",
            "where": [],
            "group_by": ["department", "location"],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": []
        }
        
        query = template.render(**params)
        
        assert "GROUP BY department, location" in query

    def test_having_clause(self, jinja_env):
        """Test HAVING clause"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": ["department", "COUNT(*) as count"],
            "table": "employees",
            "where": [],
            "group_by": ["department"],
            "having": "COUNT(*) > 5",
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": []
        }
        
        query = template.render(**params)
        
        assert "HAVING COUNT(*) > 5" in query

    def test_order_by_clause(self, jinja_env):
        """Test ORDER BY clause"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],
            "table": "employees",
            "where": [],
            "group_by": [],
            "having": None,
            "order_by": ["age DESC", "name ASC"],
            "limit": None,
            "offset": None,
            "joins": []
        }
        
        query = template.render(**params)
        
        assert "ORDER BY age DESC, name ASC" in query

    def test_limit_clause(self, jinja_env):
        """Test LIMIT clause"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],
            "table": "employees",
            "where": [],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": 10,
            "offset": None,
            "joins": []
        }
        
        query = template.render(**params)
        
        assert "LIMIT 10" in query

    def test_offset_clause(self, jinja_env):
        """Test OFFSET clause"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],
            "table": "employees",
            "where": [],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": 20,
            "joins": []
        }
        
        query = template.render(**params)
        
        assert "OFFSET 20" in query

    def test_limit_and_offset(self, jinja_env):
        """Test LIMIT and OFFSET together"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],
            "table": "employees",
            "where": [],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": 10,
            "offset": 20,
            "joins": []
        }
        
        query = template.render(**params)
        
        assert "LIMIT 10" in query
        assert "OFFSET 20" in query

    def test_inner_join(self, jinja_env):
        """Test INNER JOIN rendering"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],
            "table": "employees",
            "where": [],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": [{
                "type": "INNER",
                "table": "departments",
                "condition": "employees.dept_id = departments.id"
            }]
        }
        
        query = template.render(**params)
        
        assert "INNER JOIN departments" in query
        assert "ON employees.dept_id = departments.id" in query

    def test_left_join_with_using(self, jinja_env):
        """Test LEFT JOIN with USING clause"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],
            "table": "employees",
            "where": [],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": [{
                "type": "LEFT",
                "table": "departments",
                "using": ["dept_id", "location_id"]
            }]
        }
        
        query = template.render(**params)
        
        assert "LEFT JOIN departments" in query
        assert "USING (dept_id, location_id)" in query

    def test_multiple_joins(self, jinja_env):
        """Test multiple joins"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],
            "table": "employees",
            "where": [],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": [
                {
                    "type": "INNER",
                    "table": "departments",
                    "condition": "employees.dept_id = departments.id"
                },
                {
                    "type": "LEFT",
                    "table": "managers",
                    "using": ["manager_id"]
                }
            ]
        }
        
        query = template.render(**params)
        
        assert "INNER JOIN departments" in query
        assert "ON employees.dept_id = departments.id" in query
        assert "LEFT JOIN managers" in query
        assert "USING (manager_id)" in query

    def test_complex_query_all_clauses(self, jinja_env):
        """Test complex query with all clauses"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": ["e.name", "d.department_name", "AVG(e.salary) as avg_salary"],
            "table": "employees e",
            "where": ["e.age >= 25", "d.active = true"],
            "group_by": ["e.name", "d.department_name"],
            "having": "AVG(e.salary) > 50000",
            "order_by": ["avg_salary DESC", "e.name ASC"],
            "limit": 20,
            "offset": 0,
            "joins": [{
                "type": "INNER",
                "table": "departments d",
                "condition": "e.dept_id = d.id"
            }]
        }
        
        query = template.render(**params)
        
        # Check that all parts are present
        assert "SELECT\n    e.name, d.department_name, AVG(e.salary) as avg_salary" in query
        assert "FROM employees e" in query
        assert "INNER JOIN departments d" in query
        assert "ON e.dept_id = d.id" in query
        assert "WHERE\n    e.age >= 25 AND\n    d.active = true" in query
        assert "GROUP BY e.name, d.department_name" in query
        assert "HAVING AVG(e.salary) > 50000" in query
        assert "ORDER BY avg_salary DESC, e.name ASC" in query
        assert "LIMIT 20" in query
        assert "OFFSET 0" in query

    def test_empty_lists_ignored(self, jinja_env):
        """Test that empty lists are properly ignored"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": [],  # Empty - should use *
            "table": "employees",
            "where": [],  # Empty - should be ignored
            "group_by": [],  # Empty - should be ignored
            "having": None,
            "order_by": [],  # Empty - should be ignored
            "limit": None,
            "offset": None,
            "joins": []  # Empty - should be ignored
        }
        
        query = template.render(**params).strip()
        
        # Should only have SELECT * FROM table
        expected = "SELECT\n    *\nFROM employees"
        assert query == expected

    def test_whitespace_handling(self, jinja_env):
        """Test that whitespace is handled correctly"""
        template = jinja_env.get_template("sql.txt")
        
        params = {
            "select": ["name"],
            "table": "employees",
            "where": [],
            "group_by": [],
            "having": None,
            "order_by": [],
            "limit": None,
            "offset": None,
            "joins": []
        }
        
        query = template.render(**params)
        
        # Check that there's no excessive whitespace
        lines = query.strip().split('\n')
        assert all(line.strip() != '' for line in lines if line.strip())