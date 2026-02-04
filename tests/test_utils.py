"""
Test utilities and helper functions for GrizzlyDuck tests
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List as ListType
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import List, Outlier, Jointype


class DataGenerator:
    """Helper class to generate test data"""
    
    @staticmethod
    def create_employee_data(n_rows: int = 10) -> pd.DataFrame:
        """Create sample employee data for testing"""
        np.random.seed(42)  # For reproducible tests
        
        departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance']
        names = [f'Employee_{i}' for i in range(n_rows)]
        
        return pd.DataFrame({
            'id': range(1, n_rows + 1),
            'name': names,
            'age': np.random.randint(22, 65, n_rows),
            'salary': np.random.randint(40000, 120000, n_rows),
            'department': np.random.choice(departments, n_rows),
            'years_experience': np.random.randint(0, 20, n_rows),
            'performance_rating': np.random.uniform(1.0, 5.0, n_rows)
        })
    
    @staticmethod
    def create_sales_data(n_rows: int = 100) -> pd.DataFrame:
        """Create sample sales data for testing"""
        np.random.seed(42)
        
        regions = ['North', 'South', 'East', 'West']
        products = ['Product_A', 'Product_B', 'Product_C', 'Product_D']
        
        return pd.DataFrame({
            'id': range(1, n_rows + 1),
            'date': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
            'region': np.random.choice(regions, n_rows),
            'product': np.random.choice(products, n_rows),
            'sales_amount': np.random.uniform(100, 10000, n_rows),
            'quantity': np.random.randint(1, 100, n_rows),
            'discount': np.random.uniform(0, 0.3, n_rows)
        })
    
    @staticmethod
    def create_numeric_sequence(start: int = 1, end: int = 10) -> pd.DataFrame:
        """Create simple numeric sequence for mathematical testing"""
        return pd.DataFrame({
            'value': list(range(start, end + 1)),
            'squared': [i**2 for i in range(start, end + 1)],
            'group': ['A' if i % 2 == 0 else 'B' for i in range(start, end + 1)]
        })
    
    @staticmethod
    def create_data_with_nulls(n_rows: int = 10, null_percentage: float = 0.2) -> pd.DataFrame:
        """Create data with missing values for testing null handling"""
        np.random.seed(42)
        
        data = pd.DataFrame({
            'id': range(1, n_rows + 1),
            'value1': np.random.normal(0, 1, n_rows),
            'value2': np.random.normal(10, 5, n_rows),
            'category': np.random.choice(['A', 'B', 'C'], n_rows)
        })
        
        # Introduce nulls
        null_count = int(n_rows * null_percentage)
        null_indices = np.random.choice(n_rows, null_count, replace=False)
        data.loc[null_indices, 'value1'] = None
        
        return data
    
    @staticmethod
    def create_outlier_data() -> pd.DataFrame:
        """Create data with known outliers for testing outlier detection"""
        # Normal data
        normal_data = list(range(1, 21))  # 1 to 20
        
        # Add outliers
        outliers = [100, 200, -50]  # Clear outliers
        
        all_data = normal_data + outliers
        
        return pd.DataFrame({
            'value': all_data,
            'category': ['normal'] * len(normal_data) + ['outlier'] * len(outliers)
        })


class TestAssertions:
    """Helper class with custom assertions for testing"""
    
    @staticmethod
    def assert_dataframe_equals_ignoring_order(df1: pd.DataFrame, df2: pd.DataFrame):
        """Assert that two dataframes are equal, ignoring row order"""
        df1_sorted = df1.sort_values(list(df1.columns)).reset_index(drop=True)
        df2_sorted = df2.sort_values(list(df2.columns)).reset_index(drop=True)
        pd.testing.assert_frame_equal(df1_sorted, df2_sorted)
    
    @staticmethod
    def assert_columns_present(df: pd.DataFrame, expected_columns: ListType[str]):
        """Assert that all expected columns are present in dataframe"""
        missing_columns = set(expected_columns) - set(df.columns)
        assert not missing_columns, f"Missing columns: {missing_columns}"
    
    @staticmethod
    def assert_statistical_value_close(actual: float, expected: float, tolerance: float = 0.001):
        """Assert that statistical values are close within tolerance"""
        assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}, tolerance {tolerance}"
    
    @staticmethod
    def assert_sql_query_contains(query: str, expected_clauses: ListType[str]):
        """Assert that SQL query contains all expected clauses"""
        query_upper = query.upper()
        for clause in expected_clauses:
            assert clause.upper() in query_upper, f"Query missing clause: {clause}"


class ListTestHelpers:
    """Helper methods for testing List class functionality"""
    
    @staticmethod
    def create_test_list_with_data(data: pd.DataFrame) -> List:
        """Create a List instance with test data"""
        return List(data)
    
    @staticmethod
    def perform_basic_operations(lst: List, test_column: str) -> Dict[str, Any]:
        """Perform basic operations and return results"""
        return {
            'mean': lst.mean(test_column).result(),
            'quantile_50': lst.quantile(test_column, 0.5).result(),
            'outlier_high': lst.outlier(test_column, Outlier.HIGH).result(),
            'outlier_low': lst.outlier(test_column, Outlier.LOW).result()
        }
    
    @staticmethod
    def test_method_chaining(lst: List, operations: ListType[Dict[str, Any]]) -> pd.DataFrame:
        """Test method chaining with a list of operations"""
        result = lst
        
        for op in operations:
            method = op['method']
            args = op.get('args', [])
            kwargs = op.get('kwargs', {})
            
            result = getattr(result, method)(*args, **kwargs)
        
        return result.data() if hasattr(result, 'data') else result
    
    @staticmethod
    def validate_list_state(lst: List, expected_shape: tuple = None, 
                          expected_columns: ListType[str] = None):
        """Validate the current state of a List instance"""
        if expected_shape:
            assert lst.data().shape == expected_shape, f"Expected shape {expected_shape}, got {lst.data().shape}"
        
        if expected_columns:
            TestAssertions.assert_columns_present(lst.data(), expected_columns)


class MockDataSets:
    """Pre-defined datasets for specific test scenarios"""
    
    @staticmethod
    def get_titanic_mini():
        """Mini version of titanic dataset for testing"""
        return pd.DataFrame({
            'survived': [0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            'pclass': [3, 1, 3, 1, 3, 3, 1, 3, 3, 2],
            'sex': ['male', 'female', 'female', 'female', 'male', 'male', 'male', 'male', 'female', 'female'],
            'age': [22.0, 38.0, 26.0, 35.0, 35.0, 54.0, 54.0, 2.0, 27.0, 14.0],
            'fare': [7.25, 71.28, 7.92, 53.10, 8.05, 8.46, 51.86, 21.08, 11.13, 30.07],
            'embarked': ['S', 'C', 'S', 'S', 'S', 'Q', 'S', 'S', 'S', 'C']
        })
    
    @staticmethod
    def get_perfect_groups():
        """Data with perfect groupings for testing statistical functions"""
        return pd.DataFrame({
            'group': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
            'value': [10, 20, 30, 40, 50, 60, 70, 80, 90]
        })
    
    @staticmethod
    def get_join_test_data():
        """Data specifically designed for join testing"""
        main_table = pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'dept_id': [1, 2, 1, 3, 2]
        })
        
        dept_table = pd.DataFrame({
            'id': [1, 2, 3, 4],
            'dept_name': ['Engineering', 'Sales', 'Marketing', 'HR'],
            'location': ['Building A', 'Building B', 'Building C', 'Building D']
        })
        
        return main_table, dept_table


# Test fixtures that can be imported
def pytest_configure():
    """Configure pytest with custom markers"""
    import pytest
    
    pytest.register_marker_line = """
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    statistical: marks tests that involve statistical calculations
    """