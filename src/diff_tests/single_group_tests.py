"""Module providing a sample function"""
import fire
import pycytocc
import numpy as np
from scipy import stats
import pandas as pd
from loguru import logger
from sample_pkg.utils.util import get_date
from pycytocc.client import create_task, post_tasks, wait_wf


class SingleGroupTests:
    """simple class for running something"""

    # def do_something(self, input1, input2='stam'):
    #     """
    #     :param input1:
    #     :param input2:
    #     :return: True or False
    #     """
    #     logger.debug(f"input1={input1}, input2={input2}")
    #     logger.info(get_date())
    #     return pycytocc.client.is_capsule_env()

    @staticmethod
    def calc_corr_diff(input1, input2='stam'):
        """
        :param input1:
        :param input2:
        :return: wf status
        :rtype: str
        """
        logger.debug(f"input1={input1}, input2={input2}")
        logger.info("Running cyto-cc task")
        my_task = create_task(command='ls -lh')
        wf = post_tasks([my_task], wait=False, force_execution=True)
        wf = wait_wf(wf['workflow_id'], wait_for_descendants=True, interval=69)
        return wf['status']

    @staticmethod
    def compare_correlations(df1: pd.DataFrame, df2: pd.DataFrame) -> float:
        """Calculate Pearson correlation between corresponding columns in two dataframes.
        
        Args:
            df1: First dataframe
            df2: Second dataframe
            
        Returns:
            float: Correlation coefficient between the two dataframes
        """
        # Ensure dataframes have same columns
        common_cols = df1.columns.intersection(df2.columns)
        if len(common_cols) == 0:
            raise ValueError("No common columns between dataframes")
            
        # Calculate correlation for each common column
        correlations = []
        for col in common_cols:
            corr = np.corrcoef(df1[col].values, df2[col].values)[0, 1]
            correlations.append(corr)
            
        return np.mean(correlations)

    @staticmethod
    def compare_biological_expectations(df1: pd.DataFrame, df2: pd.DataFrame, 
                                     expectations: list) -> dict:
        """Compare how many biological expectations are met in each dataset.
        
        Args:
            df1: First dataframe
            df2: Second dataframe
            expectations: List of dictionaries containing expectations, each with:
                - 'column': Column name to check
                - 'condition': String representing condition ('>', '<', '>=', '<=', '==')
                - 'value': Value to compare against
                
        Returns:
            dict: Dictionary containing differences in met expectations
        """
        def check_expectation(df, exp):
            col = exp['column']
            val = exp['value']
            condition = exp['condition']
            
            if condition == '>':
                return (df[col] > val).mean()
            elif condition == '<':
                return (df[col] < val).mean()
            elif condition == '>=':
                return (df[col] >= val).mean()
            elif condition == '<=':
                return (df[col] <= val).mean()
            elif condition == '==':
                return (df[col] == val).mean()
            else:
                raise ValueError(f"Unknown condition: {condition}")

        results = {
            'df1_met': [],
            'df2_met': [],
            'differences': []
        }
        
        for exp in expectations:
            df1_result = check_expectation(df1, exp)
            df2_result = check_expectation(df2, exp)
            results['df1_met'].append(df1_result)
            results['df2_met'].append(df2_result)
            results['differences'].append(df2_result - df1_result)
            
        return results

    @staticmethod
    def compare_distributions(df1: pd.DataFrame, df2: pd.DataFrame) -> dict:
        """Compare distributions of values using KS test.
        
        Args:
            df1: First dataframe
            df2: Second dataframe
            
        Returns:
            dict: Dictionary containing KS test statistics and p-values for each column
        """
        common_cols = df1.columns.intersection(df2.columns)
        if len(common_cols) == 0:
            raise ValueError("No common columns between dataframes")
            
        results = {}
        for col in common_cols:
            # Scale the data to [0,1] range to make comparisons fair
            df1_scaled = (df1[col] - df1[col].min()) / (df1[col].max() - df1[col].min())
            df2_scaled = (df2[col] - df2[col].min()) / (df2[col].max() - df2[col].min())
            
            # Perform KS test
            statistic, pvalue = stats.ks_2samp(df1_scaled, df2_scaled)
            results[col] = {
                'statistic': statistic,
                'pvalue': pvalue
            }
            
        return results



# # example usage
# # For correlations
# correlation = SingleGroupTests.compare_correlations(df1, df2)

# # For biological expectations
# expectations = [
#     {'column': 'value1', 'condition': '>', 'value': 0.5},
#     {'column': 'value2', 'condition': '<', 'value': 100}
# ]
# bio_results = SingleGroupTests.compare_biological_expectations(df1, df2, expectations)

# # For distribution comparison
# dist_results = SingleGroupTests.compare_distributions(df1, df2)
