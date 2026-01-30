"""
Outlier Detector Module
Identifies outlier performances using statistical analysis (z-scores).
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


# Length columns in the dataset
LENGTH_COLS = [
    'full', 'good_length', 'short', 'short_of_a_good_length', 'yorker', 'full_toss'
]

# Line columns in the dataset
LINE_COLS = [
    'down_leg', 'on_the_stumps', 'outside_offstump', 'wide_outside_offstump', 'wide_down_leg'
]


def get_avg_col(dimension: str, value: str) -> str:
    """Get average column name for a dimension."""
    return f"avg_runs_per_dismissal_vs_pitch_{dimension}_{value}"


def get_sr_col(dimension: str, value: str) -> str:
    """Get strike rate column name for a dimension."""
    return f"strike_rate_vs_pitch_{dimension}_{value}"


def calculate_z_scores(df: pd.DataFrame, column: str) -> pd.Series:
    """
    Calculate z-scores for a column, handling NaN values.
    
    Args:
        df: DataFrame with batting data
        column: Column name to calculate z-scores for
        
    Returns:
        Series with z-scores
    """
    values = df[column].dropna()
    if len(values) < 2:
        return pd.Series([np.nan] * len(df), index=df.index)
    
    mean = values.mean()
    std = values.std()
    
    if std == 0:
        return pd.Series([0] * len(df), index=df.index)
    
    z_scores = (df[column] - mean) / std
    return z_scores


def detect_length_outliers(df: pd.DataFrame, batter_id: int, threshold: float = 1.5) -> Dict:
    """
    Detect outlier performances for different pitch lengths.
    
    Args:
        df: DataFrame with all batting data (for z-score calculation)
        batter_id: ID of the batter to analyze
        threshold: Z-score threshold for outlier detection (default 1.5)
        
    Returns:
        Dictionary with outlier information
    """
    outliers = {
        'strengths': [],  # [(length, avg, sr, z_score_avg)]
        'weaknesses': []  # [(length, avg, sr, z_score_avg)]
    }
    
    batter_data = df[df['batter_id'] == batter_id].iloc[0]
    
    for length in LENGTH_COLS:
        avg_col = get_avg_col('length', length)
        sr_col = get_sr_col('length', length)
        
        # Skip if data is missing
        if pd.isna(batter_data[avg_col]) or pd.isna(batter_data[sr_col]):
            continue
        
        # Calculate z-scores
        avg_z_scores = calculate_z_scores(df, avg_col)
        sr_z_scores = calculate_z_scores(df, sr_col)
        
        batter_idx = df[df['batter_id'] == batter_id].index[0]
        avg_z = avg_z_scores.loc[batter_idx]
        sr_z = sr_z_scores.loc[batter_idx]
        
        # Check if it's an outlier (using average z-score as primary indicator)
        if not pd.isna(avg_z) and abs(avg_z) > threshold:
            avg_val = batter_data[avg_col]
            sr_val = batter_data[sr_col]
            
            # Format length name nicely
            length_name = length.replace('_', ' ')
            
            if avg_z > 0:
                # Strength: high average
                outliers['strengths'].append((length_name, avg_val, sr_val, avg_z))
            else:
                # Weakness: low average
                outliers['weaknesses'].append((length_name, avg_val, sr_val, abs(avg_z)))
    
    # Sort by z-score magnitude (strongest first)
    outliers['strengths'].sort(key=lambda x: x[3], reverse=True)
    outliers['weaknesses'].sort(key=lambda x: x[3], reverse=True)
    
    return outliers


def detect_line_outliers(df: pd.DataFrame, batter_id: int, threshold: float = 1.5) -> Dict:
    """
    Detect outlier performances for different pitch lines.
    
    Args:
        df: DataFrame with all batting data (for z-score calculation)
        batter_id: ID of the batter to analyze
        threshold: Z-score threshold for outlier detection (default 1.5)
        
    Returns:
        Dictionary with outlier information
    """
    outliers = {
        'strengths': [],  # [(line, avg, sr, z_score_avg)]
        'weaknesses': []  # [(line, avg, sr, z_score_avg)]
    }
    
    batter_data = df[df['batter_id'] == batter_id].iloc[0]
    
    for line in LINE_COLS:
        avg_col = get_avg_col('line', line)
        sr_col = get_sr_col('line', line)
        
        # Skip if data is missing
        if pd.isna(batter_data[avg_col]) or pd.isna(batter_data[sr_col]):
            continue
        
        # Calculate z-scores
        avg_z_scores = calculate_z_scores(df, avg_col)
        sr_z_scores = calculate_z_scores(df, sr_col)
        
        batter_idx = df[df['batter_id'] == batter_id].index[0]
        avg_z = avg_z_scores.loc[batter_idx]
        sr_z = sr_z_scores.loc[batter_idx]
        
        # Check if it's an outlier
        if not pd.isna(avg_z) and abs(avg_z) > threshold:
            avg_val = batter_data[avg_col]
            sr_val = batter_data[sr_col]
            
            # Format line name nicely
            line_name = line.replace('_', ' ')
            
            if avg_z > 0:
                # Strength: high average
                outliers['strengths'].append((line_name, avg_val, sr_val, avg_z))
            else:
                # Weakness: low average
                outliers['weaknesses'].append((line_name, avg_val, sr_val, abs(avg_z)))
    
    # Sort by z-score magnitude
    outliers['strengths'].sort(key=lambda x: x[3], reverse=True)
    outliers['weaknesses'].sort(key=lambda x: x[3], reverse=True)
    
    return outliers


def get_all_length_line_stats(df: pd.DataFrame, batter_id: int) -> Dict:
    """
    Get all length and line statistics for a batter, including outliers.
    
    Args:
        df: DataFrame with all batting data
        batter_id: ID of the batter to analyze
        
    Returns:
        Dictionary with all stats and outliers
    """
    length_outliers = detect_length_outliers(df, batter_id)
    line_outliers = detect_line_outliers(df, batter_id)
    
    batter_data = df[df['batter_id'] == batter_id].iloc[0]
    
    # Get all length stats
    length_stats = {}
    for length in LENGTH_COLS:
        avg_col = get_avg_col('length', length)
        sr_col = get_sr_col('length', length)
        length_name = length.replace('_', ' ')
        length_stats[length_name] = {
            'avg': batter_data[avg_col],
            'sr': batter_data[sr_col]
        }
    
    # Get all line stats
    line_stats = {}
    for line in LINE_COLS:
        avg_col = get_avg_col('line', line)
        sr_col = get_sr_col('line', line)
        line_name = line.replace('_', ' ')
        line_stats[line_name] = {
            'avg': batter_data[avg_col],
            'sr': batter_data[sr_col]
        }
    
    return {
        'length_outliers': length_outliers,
        'line_outliers': line_outliers,
        'length_stats': length_stats,
        'line_stats': line_stats
    }


if __name__ == "__main__":
    # Test outlier detection
    import data_loader
    
    batting_df, merged_df, teams = data_loader.load_all_data(
        'Batting_data_IPL__2123.csv',
        'IPL_top7_run_scorers_by_team_2021_2023.csv'
    )
    
    # Test with a sample batter (Virat Kohli)
    test_batter_id = 253802
    stats = get_all_length_line_stats(batting_df, test_batter_id)
    
    print("Length Outliers:")
    print(f"  Strengths: {stats['length_outliers']['strengths']}")
    print(f"  Weaknesses: {stats['length_outliers']['weaknesses']}")
    
    print("\nLine Outliers:")
    print(f"  Strengths: {stats['line_outliers']['strengths']}")
    print(f"  Weaknesses: {stats['line_outliers']['weaknesses']}")
