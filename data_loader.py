"""
Data Loader Module
Loads and merges batting statistics and team selection data.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List


def load_batting_data(batting_csv_path: str) -> pd.DataFrame:
    """
    Load batting statistics CSV.
    
    Args:
        batting_csv_path: Path to Batting_data_IPL__2123.csv
        
    Returns:
        DataFrame with batting statistics
    """
    df = pd.read_csv(batting_csv_path)
    
    # Drop the unnamed index column if present
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis=1)
    
    return df


def load_team_data(team_csv_path: str) -> pd.DataFrame:
    """
    Load team selection CSV with top 7 players per team.
    
    Args:
        team_csv_path: Path to IPL_top7_run_scorers_by_team_2021_2023.csv
        
    Returns:
        DataFrame with team and player information
    """
    df = pd.read_csv(team_csv_path)
    return df


def infer_batting_hand(batter_name: str) -> str:
    """
    Infer batting hand (LHB/RHB) based on common cricket knowledge.
    This is a fallback - ideally this should be in the data.
    
    Args:
        batter_name: Name of the batter
        
    Returns:
        'LHB' or 'RHB'
    """
    # Common left-handed batters in IPL
    known_lhb = {
        'David Warner', 'Shikhar Dhawan', 'Quinton de Kock', 'Rishabh Pant',
        'Ishan Kishan', 'Devon Conway', 'Rovman Powell', 'Shimron Hetmyer',
        'Nicholas Pooran', 'Ravindra Jadeja', 'Axar Patel', 'Krunal Pandya',
        'Mitchell Marsh', 'Lalit Yadav', 'Venkatesh Iyer', 'Rinku Singh',
        'Marcus Stoinis', 'Cameron Green', 'Prithvi Shaw', 'Yashasvi Jaiswal',
        'Tilak Varma', 'Angkrish Raghuvanshi', 'Travis Head', 'Abhishek Sharma'
    }
    
    # Check if batter is in known LHB list
    if batter_name in known_lhb:
        return 'LHB'
    return 'RHB'  # Default to RHB


def merge_data(batting_df: pd.DataFrame, team_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge batting statistics with team data.
    
    Args:
        batting_df: Batting statistics DataFrame
        team_df: Team selection DataFrame
        
    Returns:
        Merged DataFrame with batting hand from CSV or inferred
    """
    # Merge on batter_id (p_bat in team_df)
    merged_df = team_df.merge(
        batting_df,
        left_on='p_bat',
        right_on='batter_id',
        how='left'
    )
    
    # Use bat_hand column from CSV if available, otherwise infer
    if 'bat_hand' in merged_df.columns:
        # Rename to batting_hand for consistency
        merged_df['batting_hand'] = merged_df['bat_hand']
        # Fill any missing values with inferred hand
        missing_mask = merged_df['batting_hand'].isna()
        if missing_mask.any():
            merged_df.loc[missing_mask, 'batting_hand'] = merged_df.loc[missing_mask, 'bat'].apply(infer_batting_hand)
    else:
        # Fallback: infer batting hand for all batters
        merged_df['batting_hand'] = merged_df['bat'].apply(infer_batting_hand)
    
    return merged_df


def get_teams(team_df: pd.DataFrame) -> List[str]:
    """
    Get list of unique teams from team data.
    
    Args:
        team_df: Team selection DataFrame
        
    Returns:
        Sorted list of team names
    """
    return sorted(team_df['team_bat'].unique().tolist())


def get_team_players(merged_df: pd.DataFrame, team_name: str) -> pd.DataFrame:
    """
    Get top 7 players for a specific team.
    
    Args:
        merged_df: Merged DataFrame
        team_name: Name of the team
        
    Returns:
        DataFrame with top 7 players for the team
    """
    team_players = merged_df[merged_df['team_bat'] == team_name].copy()
    # Sort by team_runs_rank to ensure top 7 order
    team_players = team_players.sort_values('team_runs_rank')
    return team_players


def load_all_data(batting_csv_path: str, team_csv_path: str) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
    """
    Load and prepare all data for the application.
    
    Args:
        batting_csv_path: Path to batting statistics CSV
        team_csv_path: Path to team selection CSV
        
    Returns:
        Tuple of (batting_df, merged_df, teams_list)
    """
    # Load both CSVs
    batting_df = load_batting_data(batting_csv_path)
    team_df = load_team_data(team_csv_path)
    
    # Merge data
    merged_df = merge_data(batting_df, team_df)
    
    # Get list of teams
    teams = get_teams(team_df)
    
    return batting_df, merged_df, teams


if __name__ == "__main__":
    # Test the data loader
    batting_df, merged_df, teams = load_all_data(
        'Batting_data_IPL__2123.csv',
        'IPL_top7_run_scorers_by_team_2021_2023.csv'
    )
    
    print(f"Loaded {len(batting_df)} batters from batting data")
    print(f"Loaded {len(merged_df)} player records from team data")
    print(f"Found {len(teams)} teams: {teams}")
    print(f"\nSample merged data:")
    print(merged_df[['team_bat', 'bat', 'batting_hand', 'team_runs_rank']].head(10))
