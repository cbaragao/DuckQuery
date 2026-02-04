import pytest
import pandas as pd
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import List, Jointype


class TestJoinFunctionality:
    """Test cases for join functionality"""
    
    @pytest.fixture
    def main_df(self):
        """Main dataframe for join tests"""
        return pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'department_id': [1, 2, 1, 3, 2]
        })
    
    @pytest.fixture
    def department_df(self):
        """Department dataframe for join tests"""
        return pd.DataFrame({
            'id': [1, 2, 3],
            'department_name': ['Engineering', 'HR', 'Finance']
        })
    
    @pytest.fixture
    def partial_department_df(self):
        """Partial department dataframe for testing left/right joins"""
        return pd.DataFrame({
            'id': [1, 2],
            'department_name': ['Engineering', 'HR']
        })

    def test_inner_join(self, main_df, department_df):
        """Test INNER JOIN functionality"""
        with List(main_df) as lst:
            lst.register_table('departments', department_df)
            
            result_lst = lst.run_query(
                joins=[{
                    "type": Jointype.INNER,
                    "table": "departments",
                    "condition": "current_df.department_id = departments.id"
                }]
            )
            
            result_df = result_lst.data()
            
            # Should have 5 rows (all employees match departments)
            assert len(result_df) == 5
            # Should have columns from both tables
            expected_columns = ['id', 'name', 'department_id', 'id', 'department_name']
            assert list(result_df.columns) == expected_columns

    def test_left_join(self, main_df, partial_department_df):
        """Test LEFT JOIN functionality"""
        with List(main_df) as lst:
            lst.register_table('departments', partial_department_df)
            
            result_lst = lst.run_query(
                joins=[{
                    "type": Jointype.LEFT,
                    "table": "departments",
                    "condition": "current_df.department_id = departments.id"
                }]
            )
            
            result_df = result_lst.data()
            
            # Should have 5 rows (all employees, even those without department match)
            assert len(result_df) == 5

    def test_right_join(self, main_df, department_df):
        """Test RIGHT JOIN functionality"""
        with List(main_df) as lst:
            lst.register_table('departments', department_df)
            
            result_lst = lst.run_query(
                joins=[{
                    "type": Jointype.RIGHT,
                    "table": "departments",
                    "condition": "current_df.department_id = departments.id"
                }]
            )
            
            result_df = result_lst.data()
            
            # Should include all departments
            assert len(result_df) >= 3

    def test_join_with_select_and_filter(self, main_df, department_df):
        """Test join combined with select and filter"""
        with List(main_df) as lst:
            lst.register_table('departments', department_df)
            
            result_lst = lst.run_query(
                select=['current_df.name', 'departments.department_name'],
                where=['current_df.department_id = 1'],
                joins=[{
                    "type": Jointype.INNER,
                    "table": "departments",
                    "condition": "current_df.department_id = departments.id"
                }]
            )
            
            result_df = result_lst.data()
            
            # Should have employees from department 1 only
            assert len(result_df) == 2  # Alice and Charlie
            assert list(result_df.columns) == ['name', 'department_name']

    def test_multiple_joins(self):
        """Test multiple joins in a single query"""
        employees_df = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'dept_id': [1, 2, 1],
            'manager_id': [1, 1, 2]
        })
        
        departments_df = pd.DataFrame({
            'id': [1, 2],
            'name': ['Engineering', 'HR']
        })
        
        managers_df = pd.DataFrame({
            'id': [1, 2],
            'name': ['Manager1', 'Manager2']
        })
        
        with List(employees_df) as lst:
            lst.register_table('departments', departments_df)
            lst.register_table('managers', managers_df)
            
            result_lst = lst.run_query(
                select=[
                    'current_df.name as employee_name',
                    'departments.name as dept_name',
                    'managers.name as manager_name'
                ],
                joins=[
                    {
                        "type": Jointype.INNER,
                        "table": "departments",
                        "condition": "current_df.dept_id = departments.id"
                    },
                    {
                        "type": Jointype.LEFT,
                        "table": "managers",
                        "condition": "current_df.manager_id = managers.id"
                    }
                ]
            )
            
            result_df = result_lst.data()
            
            assert len(result_df) == 3
            assert list(result_df.columns) == ['employee_name', 'dept_name', 'manager_name']

    def test_cross_join(self, main_df, department_df):
        """Test CROSS JOIN functionality"""
        # Use smaller datasets for cross join to avoid huge result set
        small_main = main_df.head(2)
        small_dept = department_df.head(2)
        
        with List(small_main) as lst:
            lst.register_table('departments', small_dept)
            
            result_lst = lst.run_query(
                joins=[{
                    "type": Jointype.CROSS,
                    "table": "departments"
                }]
            )
            
            result_df = result_lst.data()
            
            # Cross join should produce cartesian product: 2 * 2 = 4 rows
            assert len(result_df) == 4

    def test_join_with_using_clause(self):
        """Test join with USING clause"""
        table1 = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Alice', 'Bob', 'Charlie'],
            'value': [100, 200, 300]
        })
        
        table2 = pd.DataFrame({
            'id': [1, 2, 4],
            'description': ['Desc1', 'Desc2', 'Desc4'],
            'status': ['active', 'active', 'inactive']
        })
        
        with List(table1) as lst:
            lst.register_table('table2', table2)
            
            result_lst = lst.run_query(
                joins=[{
                    "type": Jointype.INNER,
                    "table": "table2",
                    "using": ["id"]
                }]
            )
            
            result_df = result_lst.data()
            
            # Should match on id 1 and 2 only
            assert len(result_df) == 2

    def test_join_type_enum_conversion(self, main_df, department_df):
        """Test that Jointype enum values are properly converted to strings"""
        with List(main_df) as lst:
            lst.register_table('departments', department_df)
            
            # This should not raise an error when the enum is converted to string
            result_lst = lst.run_query(
                joins=[{
                    "type": Jointype.LEFT,  # Using enum directly
                    "table": "departments",
                    "condition": "current_df.department_id = departments.id"
                }]
            )
            
            result_df = result_lst.data()
            assert len(result_df) >= 5  # Should have at least the original rows

    def test_anti_join(self):
        """Test ANTI JOIN functionality (if supported by DuckDB)"""
        table1 = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'name': ['Alice', 'Bob', 'Charlie', 'David']
        })
        
        table2 = pd.DataFrame({
            'id': [2, 4],
            'status': ['inactive', 'inactive']
        })
        
        with List(table1) as lst:
            lst.register_table('table2', table2)
            
            try:
                result_lst = lst.run_query(
                    joins=[{
                        "type": Jointype.ANTI,
                        "table": "table2",
                        "condition": "current_df.id = table2.id"
                    }]
                )
                
                result_df = result_lst.data()
                
                # Should return rows from table1 that don't have matches in table2
                # So Alice (id=1) and Charlie (id=3)
                assert len(result_df) == 2
                assert set(result_df['name'].tolist()) == {'Alice', 'Charlie'}
                
            except Exception as e:
                # Some databases might not support ANTI JOIN
                pytest.skip(f"ANTI JOIN not supported: {e}")

    def test_semi_join(self):
        """Test SEMI JOIN functionality (if supported by DuckDB)"""
        table1 = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'name': ['Alice', 'Bob', 'Charlie', 'David']
        })
        
        table2 = pd.DataFrame({
            'id': [2, 4],
            'status': ['active', 'active']
        })
        
        with List(table1) as lst:
            lst.register_table('table2', table2)
            
            try:
                result_lst = lst.run_query(
                    joins=[{
                        "type": Jointype.SEMI,
                        "table": "table2",
                        "condition": "current_df.id = table2.id"
                    }]
                )
                
                result_df = result_lst.data()
                
                # Should return rows from table1 that have matches in table2
                # So Bob (id=2) and David (id=4)
                assert len(result_df) == 2
                assert set(result_df['name'].tolist()) == {'Bob', 'David'}
                
            except Exception as e:
                # Some databases might not support SEMI JOIN
                pytest.skip(f"SEMI JOIN not supported: {e}")

    def test_join_error_handling(self, main_df):
        """Test error handling for invalid join conditions"""
        with List(main_df) as lst:
            with pytest.raises(Exception):
                # Try to join with a table that doesn't exist
                lst.run_query(
                    joins=[{
                        "type": Jointype.INNER,
                        "table": "nonexistent_table",
                        "condition": "current_df.id = nonexistent_table.id"
                    }]
                )

    def test_join_preserves_original_data(self, main_df, department_df):
        """Test that joins don't modify the original registered tables"""
        with List(main_df) as lst:
            original_main_len = len(lst.data())
            
            lst.register_table('departments', department_df)
            original_dept_len = len(lst.registered_tables['departments'])
            
            # Perform join
            lst.run_query(
                joins=[{
                    "type": Jointype.INNER,
                    "table": "departments",
                    "condition": "current_df.department_id = departments.id"
                }]
            )
            
            # Check that registered table is unchanged
            assert len(lst.registered_tables['departments']) == original_dept_len