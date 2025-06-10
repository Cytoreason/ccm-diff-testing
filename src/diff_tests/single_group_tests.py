import numpy as np
import pandas as pd


class SingleGroupTests:
    """measurements relevant to a single group of samples"""

    @staticmethod
    def calc_mean_feature_correlation(df1: pd.DataFrame, df2: pd.DataFrame) -> float:
        """Calculate Pearson correlation between corresponding columns in two dataframes.
        
        Args:
            df1: First dataframe
            df2: Second dataframe
            
        Returns:
            float: Mean correlation coefficient between the two dataframes
            
        Raises:
            ValueError: If no common columns or if any column has constant values
        """
        # Ensure dataframes have same columns
        common_cols = df1.columns.intersection(df2.columns)
        if len(common_cols) == 0:
            raise ValueError("No common columns between dataframes")
            
        # Calculate correlation for each common column
        correlations = []
        for col in common_cols:
            # Check for constant values
            if df1[col].std() == 0 or df2[col].std() == 0:
                raise ValueError(f"Column {col} contains constant values - correlation undefined")
                
            corr = np.corrcoef(df1[col].values, df2[col].values)[0, 1]
            correlations.append(corr)
            
        return correlations, np.mean(correlations)

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
    def rank_features_by_discrepancy(df1: pd.DataFrame, df2: pd.DataFrame) -> pd.DataFrame:
        """Rank features based on their discrepancy between two dataframes.
        
        Args:
            df1: First dataframe
            df2: Second dataframe
            
        Returns:
            pd.DataFrame: DataFrame containing features ranked by absolute mean difference,
                         including mean values and percent change
                         
        Raises:
            ValueError: If no common columns between dataframes
        """
        # Ensure dataframes have same columns
        common_cols = df1.columns.intersection(df2.columns)
        if len(common_cols) == 0:
            raise ValueError("No common columns between dataframes")
            
        # Calculate statistics for each feature
        results = []
        for col in common_cols:
            mean1 = df1[col].mean()
            mean2 = df2[col].mean()
            abs_diff = abs(mean2 - mean1)
            # Calculate percent change, handling zero mean1 case
            pct_change = ((mean2 - mean1) / mean1 * 100) if mean1 != 0 else float('inf')
            
            results.append({
                'feature': col,
                'mean_df1': mean1,
                'mean_df2': mean2,
                'absolute_difference': abs_diff,
                'percent_change': pct_change
            })
        
        # Create DataFrame and sort by absolute difference
        result_df = pd.DataFrame(results)
        result_df = result_df.sort_values('absolute_difference', ascending=False)
        result_df = result_df.reset_index(drop=True)
        
        return result_df


    