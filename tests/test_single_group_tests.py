import pytest
import pandas as pd
import numpy as np
from diff_tests.single_group_tests import SingleGroupTests


@pytest.fixture
def sample_dataframes():
    """Create sample dataframes for testing"""
    df1 = pd.DataFrame({
        'col1': range(1,31),
        'col2': range(2, 62, 2),
        'col3': [1] * 30 * np.random.normal(0, np.sqrt(0.01), 30)
    })
    
    # df2 is perfectly correlated with df1 for col1, 
    # negatively correlated for col2, and uncorrelated for col3
    df2 = pd.DataFrame({
        'col1': range(1,31),
        'col2': range(30,0,-1),
        'col3': range(1,31)
    })
    return df1, df2


@pytest.mark.unittest
class TestSingleGroupTests:
    """Test the single group tests"""
    def test_calc_mean_feature_correlation(self, sample_dataframes):
        """Test that calc_mean_feature_correlation 
        returns the correct results for the sample dataframes"""
        df1, df2 = sample_dataframes
        _, mean_corr = SingleGroupTests.calc_mean_feature_correlation(df1, df2)
        
        # Expected correlations: col1=1.0, col2=-1.0, col3=0
        # Mean correlation should be 0 (approximately)
        assert np.isclose(mean_corr, 0, atol=1e-3)

    def test_calc_mean_feature_correlation_no_common_cols(self):
        """Test that calc_mean_feature_correlation 
        raises an error if there are no common columns between the dataframes"""
        df1 = pd.DataFrame({'col1': [1, 2, 3]})
        df2 = pd.DataFrame({'col2': [4, 5, 6]})
        
        with pytest.raises(ValueError, match="No common columns between dataframes"):
            SingleGroupTests.calc_mean_feature_correlation(df1, df2)

    def test_calc_mean_feature_correlation_no_common_rows(self):
        """Test that calc_mean_feature_correlation 
        raises an error if there are no common rows between the dataframes"""
        df1 = pd.DataFrame({'col1': [1, 2, 3]})
        df2 = pd.DataFrame({'col1': [4, 5, 6]})
        
        with pytest.raises(ValueError, match="No common rows between dataframes"):
            SingleGroupTests.calc_mean_feature_correlation(df1, df2)

    def test_rank_features_by_discrepancy(self, sample_dataframes):
        """Test that rank_features_by_discrepancy 
        returns the correct results for the sample dataframes"""
        df1, df2 = sample_dataframes
        ranked_features = SingleGroupTests.rank_features_by_discrepancy(df1, df2)
        
        # Check that we have results for all columns
        assert set(ranked_features['feature']) == {'col1', 'col2', 'col3'}
        
        # Check that the DataFrame has all expected columns
        expected_columns = {'feature', 'mean_df1', 'mean_df2', 'absolute_difference', 'percent_change'}
        assert set(ranked_features.columns) == expected_columns
        
        # Check ordering - col3 should have largest difference, then col2, then col1
        assert ranked_features['feature'].iloc[0] == 'col3'  # Largest difference (mean1=0.9976, mean2=3)
        assert ranked_features['feature'].iloc[1] == 'col2'  # Second largest (mean1=6, mean2=6)
        assert ranked_features['feature'].iloc[2] == 'col1'  # No difference (mean1=3, mean2=3)
        
        # Check specific values for col1 (identical in both dataframes)
        col1_row = ranked_features[ranked_features['feature'] == 'col1'].iloc[0]
        assert np.isclose(col1_row['mean_df1'], 3.0)
        assert np.isclose(col1_row['mean_df2'], 3.0)
        assert np.isclose(col1_row['absolute_difference'], 0.0)
        assert np.isclose(col1_row['percent_change'], 0.0)

    def test_rank_features_by_discrepancy_no_common_cols(self):
        """Test that rank_features_by_discrepancy 
        raises an error if there are no common columns between the dataframes"""
        df1 = pd.DataFrame({'col1': [1, 2, 3]})
        df2 = pd.DataFrame({'col2': [4, 5, 6]})
        
        with pytest.raises(ValueError, match="No common columns between dataframes"):
            SingleGroupTests.rank_features_by_discrepancy(df1, df2)


