import pytest
import pandas as pd
import numpy as np
import sys
import os
from unittest.mock import patch

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import List, Outlier, Jointype


class TestList:
    """Test cases for the List class functionality"""
    
    @pytest.fixture
    def sample_df(self):
        """Create a sample dataframe for testing"""
        return pd.DataFrame({
            'id': [1, 2, 3, 4, 5],
            'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
            'age': [25, 30, 35, 40, 45],
            'salary': [50000, 60000, 70000, 80000, 90000],
            'department': ['IT', 'HR', 'IT', 'Finance', 'IT']
        })
    
    @pytest.fixture
    def numeric_df(self):
        """Create a dataframe with titanic-style columns for precise testing"""
        return pd.DataFrame({
            'age': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'pclass': [1, 1, 2, 2, 3, 3, 1, 1, 2, 2]
        })

    def test_list_initialization(self, sample_df):
        """Test List class initialization"""
        with List(sample_df) as lst:
            assert lst.df.equals(sample_df)
            assert lst.value == 0
            assert lst.db is not None
            assert 'current_df' in lst.db.execute("SHOW TABLES").df()['name'].values

    def test_context_manager(self, sample_df):
        """Test that List works as a context manager"""
        with List(sample_df) as lst:
            assert lst.db is not None
        # After context exit, db should be closed
        assert lst.db is None

    def test_mean_calculation(self, numeric_df):
        """Test mean calculation"""
        with List(numeric_df) as lst:
            result = lst.mean('age').result()
            expected = numeric_df['age'].mean()
            assert result == expected

    def test_multiply_operation(self, sample_df):
        """Test multiply operation"""
        with List(sample_df, value=10) as lst:
            result = lst.multiply(2.5).result()
            assert result == 25.0

    def test_method_chaining(self, numeric_df):
        """Test method chaining functionality"""
        with List(numeric_df) as lst:
            result = lst.mean('age').multiply(2).result()
            expected = numeric_df['age'].mean() * 2
            assert result == expected

    def test_quantile_calculation(self, numeric_df):
        """Test quantile calculation"""
        with List(numeric_df) as lst:
            result = lst.quantile('age', 0.5).result()
            expected = numeric_df['age'].quantile(0.5)
            assert result == expected

    def test_outlier_detection_high(self):
        """Test high outlier detection"""
        # Create titanic-style data for outlier testing
        test_data = pd.DataFrame({
            'age': [1, 2, 3, 4, 5, 6, 7, 8, 9, 100],
            'survived': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            'pclass': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]
        })
        
        with List(test_data) as lst:
            result = lst.outlier('age', Outlier.HIGH).result()
            
            # Calculate expected manually
            q1 = test_data['age'].quantile(0.25)
            q3 = test_data['age'].quantile(0.75)
            iqr = q3 - q1
            expected = q3 + (1.5 * iqr)
            
            assert result == expected

    def test_outlier_detection_low(self):
        """Test low outlier detection"""
        # Create titanic-style data for outlier testing
        test_data = pd.DataFrame({
            'age': [-100, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            'survived': [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            'pclass': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]
        })
        
        with List(test_data) as lst:
            result = lst.outlier('age', Outlier.LOW).result()
            
            # Calculate expected manually
            q1 = test_data['age'].quantile(0.25)
            q3 = test_data['age'].quantile(0.75)
            iqr = q3 - q1
            expected = q1 - (1.5 * iqr)
            
            assert result == expected

    def test_median_of_means(self):
        """Test median of means calculation"""
        test_data = pd.DataFrame({
            'pclass': [1, 1, 1, 2, 2, 2, 3, 3, 3],
            'age': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'survived': [0, 1, 0, 1, 0, 1, 0, 1, 0]
        })
        
        with List(test_data) as lst:
            result = lst.median_of_means('pclass', 'age').result()
            
            # Calculate expected manually
            group_means = test_data.groupby('pclass')['age'].mean()
            expected = group_means.median()
            
            assert result == expected

    def test_filter_operation(self, sample_df):
        """Test filter operation"""
        with List(sample_df) as lst:
            filtered_lst = lst.filter("age >= 35")
            filtered_df = filtered_lst.data()
            
            # Should have 3 rows (ages 35, 40, 45)
            assert len(filtered_df) == 3
            assert all(filtered_df['age'] >= 35)

    def test_select_columns(self, sample_df):
        """Test column selection"""
        with List(sample_df) as lst:
            selected_lst = lst.select(['name', 'age'])
            selected_df = selected_lst.data()
            
            assert list(selected_df.columns) == ['name', 'age']
            assert len(selected_df) == len(sample_df)

    def test_order_operation(self, sample_df):
        """Test ordering operation"""
        with List(sample_df) as lst:
            ordered_lst = lst.order(['age DESC'])
            ordered_df = ordered_lst.data()
            
            # Should be ordered by age descending
            assert ordered_df['age'].tolist() == [45, 40, 35, 30, 25]

    def test_limit_operation(self, sample_df):
        """Test limit operation"""
        with List(sample_df) as lst:
            limited_lst = lst.limit(3)
            limited_df = limited_lst.data()
            
            assert len(limited_df) == 3

    def test_register_table(self, sample_df):
        """Test table registration for joins"""
        additional_df = pd.DataFrame({
            'id': [1, 2, 3],
            'bonus': [1000, 2000, 3000]
        })
        
        with List(sample_df) as lst:
            lst.register_table('bonuses', additional_df)
            
            assert 'bonuses' in lst.registered_tables
            assert lst.registered_tables['bonuses'].equals(additional_df)

    def test_run_query_basic_select(self, sample_df):
        """Test run_query with basic select"""
        with List(sample_df) as lst:
            result_lst = lst.run_query(select=['name', 'age'])
            result_df = result_lst.data()
            
            assert list(result_df.columns) == ['name', 'age']

    def test_run_query_with_where(self, sample_df):
        """Test run_query with WHERE clause"""
        with List(sample_df) as lst:
            result_lst = lst.run_query(
                select=['name', 'age'],
                where=['age >= 35']
            )
            result_df = result_lst.data()
            
            assert len(result_df) == 3
            assert all(result_df['age'] >= 35)

    def test_run_query_with_order_by(self, sample_df):
        """Test run_query with ORDER BY"""
        with List(sample_df) as lst:
            result_lst = lst.run_query(
                select=['name', 'age'],
                order_by=['age DESC']
            )
            result_df = result_lst.data()
            
            assert result_df['age'].tolist() == [45, 40, 35, 30, 25]

    def test_run_query_with_limit(self, sample_df):
        """Test run_query with LIMIT"""
        with List(sample_df) as lst:
            result_lst = lst.run_query(limit=2)
            result_df = result_lst.data()
            
            assert len(result_df) == 2

    def test_run_query_with_group_by(self, sample_df):
        """Test run_query with GROUP BY"""
        with List(sample_df) as lst:
            result_lst = lst.run_query(
                select=['department', 'COUNT(*) as count'],
                group_by=['department']
            )
            result_df = result_lst.data()
            
            # Should have 3 departments
            assert len(result_df) == 3

    def test_jointype_enum_values(self):
        """Test Jointype enum values"""
        assert Jointype.INNER.value == "INNER"
        assert Jointype.LEFT.value == "LEFT"
        assert Jointype.RIGHT.value == "RIGHT"
        assert Jointype.FULL.value == "FULL OUTER"
        assert Jointype.CROSS.value == "CROSS"
        assert Jointype.SEMI.value == "SEMI"
        assert Jointype.ANTI.value == "ANTI"

    def test_outlier_enum_values(self):
        """Test Outlier enum values"""
        assert Outlier.HIGH.name == "HIGH"
        assert Outlier.LOW.name == "LOW"

    def test_method_chaining_complex(self, sample_df):
        """Test complex method chaining"""
        with List(sample_df) as lst:
            result_df = lst.select(['name', 'age', 'department']) \
                          .filter("department = 'IT'") \
                          .order(['age ASC']) \
                          .limit(2) \
                          .data()
            
            assert len(result_df) == 2
            assert all(result_df['department'] == 'IT')
            assert list(result_df.columns) == ['name', 'age', 'department']

    def test_error_handling_invalid_column(self, sample_df):
        """Test error handling for invalid column names"""
        with pytest.raises(Exception):
            with List(sample_df) as lst:
                lst.mean('nonexistent_column').result()

    def test_data_persistence_after_operations(self, sample_df):
        """Test that data persists correctly after operations"""
        with List(sample_df) as lst:
            # Perform some operations
            lst.filter("age >= 30")
            lst.select(['name', 'age'])
            
            # Check that the data is what we expect
            result_df = lst.data()
            assert len(result_df) == 4  # 4 people with age >= 30
            assert list(result_df.columns) == ['name', 'age']

    def test_show_info_method(self, sample_df, capsys):
        """Test the show_info debug method"""
        with List(sample_df) as lst:
            lst.show_info()
            captured = capsys.readouterr()
            
            assert "Current dataframe shape: (5, 5)" in captured.out
            assert "Columns: ['id', 'name', 'age', 'salary', 'department']" in captured.out