import numpy as np
import pandas as pd
from scipy.stats import spearmanr

class SingleGroupTests:
    """measurements relevant to a single group of samples"""

    @staticmethod
    def calc_mean_feature_correlation(df1: pd.DataFrame, df2: pd.DataFrame) -> float:
        """Calculate Spearman correlation between corresponding columns in two dataframes.
        Args:
            df1: First dataframe
            df2: Second dataframe
        assumption: rows are samples, columns are features (e.g. genes or cell types)             
        Returns:
            float: Mean correlation coefficient between the two dataframes
            
        Raises:
            ValueError: If no common columns or if any column has constant values
        """
        # Ensure dataframes have same columns
        common_cols = df1.columns.intersection(df2.columns)
        common_rows = df1.index.intersection(df2.index)
        if len(common_cols) == 0:
            raise ValueError("No common columns between dataframes")
        if len(common_rows) == 0:
            raise ValueError("No common rows between dataframes")
            
        # Calculate correlation for each common column
        correlations = []
        for col in common_cols:
            # Check for constant values
            if df1[col].std() == 0 or df2[col].std() == 0:
                raise ValueError(f"Column {col} contains constant values - correlation undefined")
                
            corr, _ = spearmanr(df1.loc[common_rows, col].values, df2.loc[common_rows, col].values)
            correlations.append(corr)
            
        return correlations, np.mean(correlations)

    
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
        common_rows = df1.index.intersection(df2.index)
        if len(common_cols) == 0:
            raise ValueError("No common columns between dataframes")
        if len(common_rows) == 0:
            raise ValueError("No common rows between dataframes")
            
        # Calculate statistics for each feature
        results = []
        for col in common_cols:
            values1 = df1.loc[common_rows, col].values
            values2 = df2.loc[common_rows, col].values
            mean_diff = (values1 - values2).mean()
            abs_diff = abs(mean_diff)
            # Calculate percent change as the mean of all percent changes between the two dataframes
            with np.errstate(divide='ignore', invalid='ignore'):
                pct_changes = np.where(values2 != 0, (values1 - values2) / values2 * 100, 0)
            pct_change = np.mean(pct_changes)
            
            results.append({
                'feature': col,
                'absolute_difference': abs_diff,
                'percent_change': pct_change
            })
        
        # Create DataFrame and sort by absolute difference
        result_df = pd.DataFrame(results)
        result_df = result_df.sort_values('absolute_difference', ascending=False)
        result_df = result_df.reset_index(drop=True)
        
        return result_df


    