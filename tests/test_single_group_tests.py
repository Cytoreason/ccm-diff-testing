import pytest
import pandas as pd
import numpy as np
from diff_tests.single_group_tests import SingleGroupTests


@pytest.fixture
def sample_dataframes():
    """Create sample dataframes for testing"""
    df1 = pd.DataFrame({
        'sample1': range(1,31),
        'sample2': range(2, 62, 2),
        'sample3': [1] * 30 * np.random.normal(0, np.sqrt(0.01), 30)
    })
    df1.index = ['feature' + str(x) for x in range(1,31)]
    # df2 is perfectly correlated with df1 for col1, 
    # negatively correlated for col2, and uncorrelated for col3
    df2 = pd.DataFrame({
        'sample1': range(1,31),
        'sample2': range(30,0,-1),
        'sample3': range(1,31)
    })
    df2.index = ['feature' + str(x) for x in range(1,31)]
    return df1.T, df2.T # Transpose the dataframes to have features as columns


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
        df1 = pd.DataFrame({'sample1': [1, 2, 3]})
        df2 = pd.DataFrame({'sample2': [4, 5, 6]})
        df1.index = ['feature1', 'feature2', 'feature3']
        df2.index = ['feature1', 'feature2', 'feature3']
        
        with pytest.raises(ValueError, match="No common columns between dataframes"):
            SingleGroupTests.calc_mean_feature_correlation(df1, df2)

    def test_calc_mean_feature_correlation_no_common_rows(self):
        """Test that calc_mean_feature_correlation 
        raises an error if there are no common rows between the dataframes"""
        df1 = pd.DataFrame({'sample1': [1, 2, 3]})
        df2 = pd.DataFrame({'sample1': [4, 5, 6]})
        df1.index = ['feature1', 'feature2', 'feature3']
        df2.index = ['feature4', 'feature5', 'feature6']
        
        with pytest.raises(ValueError, match="No common rows between dataframes"):
            SingleGroupTests.calc_mean_feature_correlation(df1, df2)

    def test_rank_features_by_discrepancy(self, sample_dataframes):
        """
        Test that rank_features_by_discrepancy returns the correct results for the sample dataframes.

        This test checks that the function returns a DataFrame with the correct features,
        columns, and that the values are as expected given the current implementation,
        which only returns 'feature', 'absolute_difference', and 'percent_change'.
        """
        df1, df2 = sample_dataframes
        ranked_features = SingleGroupTests.rank_features_by_discrepancy(df1, df2)

        # Check that we have results for all columns
        assert set(ranked_features['feature']) == {'feature' + str(x) for x in range(1,31)}

        # Check that the DataFrame has all expected columns (per current implementation)
        expected_columns = {'feature', 'absolute_difference', 'percent_change'}
        assert set(ranked_features.columns) == expected_columns

        # Check that the DataFrame is sorted by absolute_difference descending
        abs_diffs = ranked_features['absolute_difference'].values
        assert all(abs_diffs[i] >= abs_diffs[i+1] for i in range(len(abs_diffs)-1))

        # Check that all features are present and percent_change is finite
        for _, row in ranked_features.iterrows():
            assert row['feature'] in {'feature' + str(x) for x in range(1,31)}
            assert np.isfinite(row['percent_change'])

    def test_rank_features_by_discrepancy_no_common_cols(self):
        """Test that rank_features_by_discrepancy 
        raises an error if there are no common columns between the dataframes"""
        df1 = pd.DataFrame({'col1': [1, 2, 3]})
        df2 = pd.DataFrame({'col2': [4, 5, 6]})
        
        with pytest.raises(ValueError, match="No common columns between dataframes"):
            SingleGroupTests.rank_features_by_discrepancy(df1, df2)


