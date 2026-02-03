"""
Module to generate color-coded performance vs bowling types table
"""

import pandas as pd
import streamlit as st


def get_color_for_metric(value, metric_type, thresholds=None):
    """
    Get color based on metric value and type.
    
    Args:
        value: The metric value
        metric_type: Type of metric ('strike_rate', 'average', 'boundary_pct', 'dot_pct')
        thresholds: Optional custom thresholds
    
    Returns:
        Color code as hex string
    """
    # Default thresholds based on cricket standards
    if thresholds is None:
        thresholds = {
            'strike_rate': {'good': 140, 'medium': 120},  # Good >= 140, Medium >= 120
            'average': {'good': 40, 'medium': 25},  # Good >= 40, Medium >= 25
            'boundary_pct': {'good': 20, 'medium': 15},  # Good >= 20%, Medium >= 15%
            'dot_pct': {'good': 30, 'medium': 40}  # Good <= 30%, Medium <= 40% (reversed)
        }
    
    # Colors
    GREEN = '#22c55e'  # Good
    YELLOW = '#facc15'  # Medium
    RED = '#ef4444'  # Bad
    
    if pd.isna(value) or value == 0:
        return '#6b7280'  # Gray for NA/0
    
    # For dot_pct, lower is better (reverse logic)
    if metric_type == 'dot_pct':
        if value <= thresholds[metric_type]['good']:
            return GREEN
        elif value <= thresholds[metric_type]['medium']:
            return YELLOW
        else:
            return RED
    else:
        # For other metrics, higher is better
        if value >= thresholds[metric_type]['good']:
            return GREEN
        elif value >= thresholds[metric_type]['medium']:
            return YELLOW
        else:
            return RED


def generate_bowler_type_table(bowler_data_df: pd.DataFrame, batter_name: str) -> pd.DataFrame:
    """
    Generate performance vs bowling types table for a specific batter.
    
    Args:
        bowler_data_df: DataFrame with columns from Batters_StrikeRateVSBowlerTypeNew.csv
        batter_name: Name of the batter to generate table for
    
    Returns:
        Formatted DataFrame with performance metrics
    """
    # Filter data for the specific batter
    batter_df = bowler_data_df[bowler_data_df['Batter_Name'] == batter_name].copy()
    
    if batter_df.empty:
        return pd.DataFrame()
    
    # Calculate strike rate
    batter_df['strike_rate'] = (batter_df['runs_vs_type'] / batter_df['balls_faced'] * 100).round(1)
    
    # Select and rename columns for display
    display_df = batter_df[[
        'bowler.type',
        'balls_faced',
        'strike_rate',
        'batting_avg',
        'dot_pct',
        'boundary_pct'
    ]].copy()
    
    # Rename columns
    display_df.columns = ['Bowler Type', 'Balls Faced', 'Strike Rate', 'Average', 'Dot Ball %', 'Boundary %']
    
    # Sort by balls faced (descending) to show most relevant bowler types first
    display_df = display_df.sort_values('Balls Faced', ascending=False)
    
    # Reset index
    display_df = display_df.reset_index(drop=True)
    
    return display_df


def display_bowler_type_table_html(df: pd.DataFrame):
    """
    Display the bowler type table with color coding using Streamlit's dataframe styling.
    
    Args:
        df: DataFrame with performance metrics
    """
    if df.empty:
        st.warning("⚠️ No bowling type data available for this player.")
        return
    
    # Display title
    st.markdown('<h2 style="color: #00d9c0; margin-top: 2rem;">Performance vs Bowling Types</h2>', unsafe_allow_html=True)
    
    # Create a copy for styling
    display_df = df.copy()
    
    # Function to apply background color to cells
    def apply_color_gradient(row):
        # Get colors for each metric
        sr_color = get_color_for_metric(row['Strike Rate'], 'strike_rate')
        avg_color = get_color_for_metric(row['Average'], 'average')
        dot_color = get_color_for_metric(row['Dot Ball %'], 'dot_pct')
        boundary_color = get_color_for_metric(row['Boundary %'], 'boundary_pct')
        
        return [
            '',  # Bowler Type
            '',  # Balls Faced
            f'background-color: {sr_color}; color: #1a2332; font-weight: bold',  # Strike Rate
            f'background-color: {avg_color}; color: #1a2332; font-weight: bold',  # Average
            f'background-color: {dot_color}; color: #1a2332; font-weight: bold',  # Dot Ball %
            f'background-color: {boundary_color}; color: #1a2332; font-weight: bold'  # Boundary %
        ]
    
    # Apply the styling
    styled = display_df.style.apply(apply_color_gradient, axis=1)
    
    # Format numeric columns
    styled = styled.format({
        'Balls Faced': '{:.0f}',
        'Strike Rate': lambda x: f'{x:.1f}' if pd.notna(x) else '-',
        'Average': lambda x: f'{x:.1f}' if pd.notna(x) else '-',
        'Dot Ball %': lambda x: f'{x:.1f}%' if pd.notna(x) else '-',
        'Boundary %': lambda x: f'{x:.1f}%' if pd.notna(x) else '-'
    })
    
    # Display the table
    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        height=min(400, (len(df) + 1) * 35 + 10)
    )


def display_zone_analysis(zone_df: pd.DataFrame, batter_name: str):
    """
    Display zone-based boundary analysis.
    
    Args:
        zone_df: DataFrame with zone data
        batter_name: Name of the batter
    """
    # Filter for the batter
    batter_zone = zone_df[zone_df['bat'] == batter_name]
    
    if batter_zone.empty:
        st.info("📊 No zone analysis data available for this player.")
        return
    
    st.markdown('<div class="table-title">Boundary Distribution by Zone</div>', unsafe_allow_html=True)
    st.info("🚧 Zone visualization coming soon...")
