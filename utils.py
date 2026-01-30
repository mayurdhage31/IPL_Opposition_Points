"""
Utility Functions
Helper functions for the cricket analysis application.
"""

import pandas as pd
import numpy as np
from typing import List, Dict


def validate_writeup(writeup: Dict, max_words: int = 150, max_lines: int = 10) -> Dict:
    """
    Validate write-up against word and line count constraints.
    
    Args:
        writeup: Write-up dictionary
        max_words: Maximum allowed words
        max_lines: Maximum allowed lines
        
    Returns:
        Dictionary with validation results
    """
    word_count = writeup['word_count']
    line_count = writeup['line_count']
    
    validation = {
        'valid': True,
        'warnings': [],
        'errors': []
    }
    
    if word_count > max_words:
        validation['valid'] = False
        validation['errors'].append(f"Word count ({word_count}) exceeds limit ({max_words})")
    
    if line_count > max_lines:
        validation['warnings'].append(f"Line count ({line_count}) exceeds recommended limit ({max_lines})")
    
    if writeup['num_insights'] < 3:
        validation['warnings'].append(f"Only {writeup['num_insights']} insights generated (expected 5)")
    
    return validation


def format_percentage(value: float, decimals: int = 0) -> str:
    """Format a value as percentage."""
    return f"{value:.{decimals}f}%"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default if denominator is 0."""
    if denominator == 0 or pd.isna(denominator):
        return default
    return numerator / denominator


def clean_shot_name(shot_name: str) -> str:
    """Clean and format shot name for display."""
    # Replace underscores with spaces
    clean_name = shot_name.replace('_', ' ')
    # Capitalize first letter of each word
    clean_name = clean_name.title()
    return clean_name


def get_data_summary(df: pd.DataFrame) -> Dict:
    """
    Get summary statistics about the dataset.
    
    Args:
        df: DataFrame to summarize
        
    Returns:
        Dictionary with summary stats
    """
    return {
        'total_batters': len(df),
        'columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'complete_records': len(df.dropna())
    }


if __name__ == "__main__":
    # Test utilities
    test_writeup = {
        'batter_name': 'Test Player',
        'batting_hand': 'RHB',
        'writeup': 'Test writeup text.',
        'word_count': 145,
        'line_count': 8,
        'num_insights': 5
    }
    
    validation = validate_writeup(test_writeup)
    print(f"Validation: {validation}")
