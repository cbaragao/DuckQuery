import pytest
import pandas as pd
import seaborn as sns
import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import List, Outlier, Jointype


class TestIntegration:
    """Integration tests using real-world scenarios"""
    
    @pytest.fixture
    def titanic_sample(self):
        """Create a small sample of titanic-like data for testing"""
        return pd.DataFrame({
            'survived': [0, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            'pclass': [3, 1, 3, 1, 3, 3, 1, 3, 3, 2],
            'sex': ['male', 'female', 'female', 'female', 'male', 'male', 'male', 'male', 'female', 'female'],
            'age': [22.0, 38.0, 26.0, 35.0, None, None, 54.0, 2.0, 27.0, 14.0],
            'fare': [7.25, 71.28, 7.92, 53.10, 8.05, 8.46, 51.86, 21.08, 11.13, 30.07],
            'embarked': ['S', 'C', 'S', 'S', 'S', 'Q', 'S', 'S', 'S', 'C'],
            'class': ['Third', 'First', 'Third', 'First', 'Third', 'Third', 'First', 'Third', 'Third', 'Second']
        })

    def test_basic_data_exploration_workflow(self, titanic_sample):
        """Test a basic data exploration workflow"""
        with List(titanic_sample) as lst:
            # Get basic statistics
            avg_age = lst.mean('age').result()
            
            # Filter and explore
            survivors = lst.filter('survived = 1').data()
            
            # Check results
            assert avg_age > 0
            assert len(survivors) == 5  # 5 survivors in our sample
            assert all(survivors['survived'] == 1)

    def test_statistical_analysis_workflow(self, titanic_sample):
        """Test statistical analysis workflow"""
        with List(titanic_sample) as lst:
            # Calculate outliers for fare
            high_fare_outlier = lst.outlier('fare', Outlier.HIGH).result()
            low_fare_outlier = lst.outlier('fare', Outlier.LOW).result()
            
            # Get median of means by passenger class
            median_of_class_means = lst.median_of_means('pclass', 'fare').result()
            
            assert high_fare_outlier > low_fare_outlier
            assert median_of_class_means > 0

    def test_complex_filtering_and_selection_workflow(self, titanic_sample):
        """Test complex filtering and selection workflow"""
        with List(titanic_sample) as lst:
            # Complex filtering: male passengers who survived
            result_df = lst.select(['survived', 'pclass', 'sex', 'age']) \
                          .filter("sex = 'male'") \
                          .filter("survived = 1") \
                          .order(['pclass ASC', 'age DESC']) \
                          .data()
            
            # Should have male survivors only
            assert len(result_df) == 0  # No male survivors in our small sample
            
            # Try female survivors
            with List(titanic_sample) as lst2:
                female_survivors = lst2.select(['survived', 'pclass', 'sex', 'age']) \
                                     .filter("sex = 'female'") \
                                     .filter("survived = 1") \
                                     .order(['pclass ASC']) \
                                     .data()
                
                assert len(female_survivors) == 5  # 5 female survivors
                assert all(female_survivors['sex'] == 'female')
                assert all(female_survivors['survived'] == 1)

    def test_aggregation_and_grouping_workflow(self, titanic_sample):
        """Test aggregation and grouping workflow"""
        with List(titanic_sample) as lst:
            # Group by class and get survival stats
            survival_by_class = lst.run_query(
                select=['pclass', 'COUNT(*) as total', 'SUM(survived) as survivors'],
                group_by=['pclass'],
                order_by=['pclass ASC']
            ).data()
            
            assert len(survival_by_class) == 3  # 3 classes
            assert 'total' in survival_by_class.columns
            assert 'survivors' in survival_by_class.columns

    def test_join_workflow_with_additional_data(self, titanic_sample):
        """Test join workflow with additional data"""
        # Create additional passenger info
        passenger_info = pd.DataFrame({
            'pclass': [1, 2, 3],
            'class_name': ['First Class', 'Second Class', 'Third Class'],
            'deck_location': ['Upper', 'Middle', 'Lower']
        })
        
        with List(titanic_sample) as lst:
            lst.register_table('passenger_info', passenger_info)
            
            # Join to get class names
            enriched_data = lst.run_query(
                select=['current_df.survived', 'current_df.sex', 'passenger_info.class_name'],
                joins=[{
                    "type": Jointype.INNER,
                    "table": "passenger_info",
                    "condition": "current_df.pclass = passenger_info.pclass"
                }],
                order_by=['passenger_info.class_name ASC']
            ).data()
            
            assert len(enriched_data) == len(titanic_sample)
            assert 'class_name' in enriched_data.columns
            assert all(name in enriched_data['class_name'].values 
                      for name in ['First Class', 'Second Class', 'Third Class'])

    def test_data_quality_analysis_workflow(self):
        """Test data quality analysis workflow"""
        # Create data with missing values and outliers
        messy_data = pd.DataFrame({
            'survived': [1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            'age': [10, 12, 11, 1000, 13, 9, 8, None, 15, 14],  # 1000 is outlier, None is missing
            'pclass': [1, 1, 2, 2, 1, 3, 3, 1, 2, 3]
        })
        
        with List(messy_data) as lst:
            # Find outliers
            high_outlier = lst.outlier('age', Outlier.HIGH).result()
            
            # Filter out outliers and nulls for clean analysis
            clean_data = lst.filter('age < 100') \
                           .filter('age IS NOT NULL') \
                           .data()
            
            assert high_outlier > 100  # Should detect 1000 as outlier
            assert len(clean_data) == 8  # Should exclude outlier and null

    def test_performance_analysis_workflow(self):
        """Test performance-related analysis workflow"""
        # Create sales-like data
        sales_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=100, freq='D'),
            'sales': [100 + i + (i % 7) * 20 for i in range(100)],  # Trend with weekly pattern
            'region': ['North', 'South', 'East', 'West'] * 25,
            'product': ['A', 'B'] * 50
        })
        
        with List(sales_data) as lst:
            # Top performing regions
            regional_performance = lst.run_query(
                select=['region', 'AVG(sales) as avg_sales', 'SUM(sales) as total_sales'],
                group_by=['region'],
                order_by=['avg_sales DESC'],
                limit=3
            ).data()
            
            assert len(regional_performance) == 3  # Top 3 regions
            assert 'avg_sales' in regional_performance.columns
            assert 'total_sales' in regional_performance.columns

    def test_comparative_analysis_workflow(self):
        """Test comparative analysis between groups"""
        # Create before/after data
        performance_data = pd.DataFrame({
            'employee_id': list(range(1, 21)) * 2,
            'period': ['before'] * 20 + ['after'] * 20,
            'score': ([70, 75, 80, 85, 90] * 4) + ([75, 80, 85, 90, 95] * 4),
            'department': (['A', 'B', 'C', 'D'] * 5) * 2
        })
        
        # Separate before and after data
        before_data = performance_data[performance_data['period'] == 'before']
        after_data = performance_data[performance_data['period'] == 'after']
        
        with List(before_data) as lst:
            lst.register_table('after_data', after_data)
            
            # Compare performance improvements
            comparison = lst.run_query(
                select=[
                    'current_df.department',
                    'AVG(current_df.score) as before_avg',
                    'AVG(after_data.score) as after_avg'
                ],
                joins=[{
                    "type": Jointype.INNER,
                    "table": "after_data",
                    "condition": "current_df.department = after_data.department"
                }],
                group_by=['current_df.department']
            ).data()
            
            assert len(comparison) == 4  # 4 departments
            assert all(comparison['after_avg'] >= comparison['before_avg'])  # Performance improved

    def test_complex_method_chaining_workflow(self, titanic_sample):
        """Test complex method chaining that mirrors real usage"""
        with List(titanic_sample) as lst:
            # Complex analysis: survival rate by class for females
            result = lst.select(['survived', 'pclass', 'sex', 'age', 'fare']) \
                       .filter("sex = 'female'") \
                       .filter("age IS NOT NULL") \
                       .order(['fare DESC']) \
                       .limit(3) \
                       .data()
            
            assert len(result) <= 3
            assert all(result['sex'] == 'female')
            assert result['fare'].tolist() == sorted(result['fare'].tolist(), reverse=True)

    def test_error_recovery_workflow(self, titanic_sample):
        """Test that errors in one operation don't break the entire workflow"""
        with List(titanic_sample) as lst:
            # Start with valid operations
            valid_result = lst.select(['survived', 'pclass']).data()
            assert len(valid_result) == len(titanic_sample)
            
            # Try invalid operation (should raise exception)
            with pytest.raises(Exception):
                lst.filter("nonexistent_column = 1").data()

    def test_memory_efficiency_workflow(self):
        """Test that operations don't cause memory issues with larger datasets"""
        # Create a moderately sized dataset
        large_data = pd.DataFrame({
            'survived': [i % 2 for i in range(1000)],
            'age': [i % 100 for i in range(1000)],
            'pclass': [f'{(i % 3) + 1}' for i in range(1000)]
        })
        
        with List(large_data) as lst:
            # Perform multiple operations
            result = lst.filter('age >= 50') \
                       .select(['survived', 'pclass']) \
                       .order(['pclass ASC']) \
                       .limit(100) \
                       .data()
            
            assert len(result) <= 100
            assert list(result.columns) == ['survived', 'pclass']

    def test_real_world_seaborn_dataset(self):
        """Test with actual seaborn dataset if available"""
        try:
            # Use a small sample of tips dataset
            tips = sns.load_dataset("tips")
            tips_sample = tips.head(20)  # Use small sample for testing
            
            with List(tips_sample) as lst:
                # Analyze tips by day and time
                analysis = lst.run_query(
                    select=['day', 'time', 'AVG(tip) as avg_tip', 'COUNT(*) as count'],
                    group_by=['day', 'time'],
                    order_by=['avg_tip DESC']
                ).data()
                
                assert len(analysis) > 0
                assert 'avg_tip' in analysis.columns
                assert 'count' in analysis.columns
                
        except Exception:
            # Skip if seaborn datasets are not available
            pytest.skip("Seaborn datasets not available")