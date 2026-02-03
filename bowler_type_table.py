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
    Display the bowler type table with color coding using HTML/CSS.
    
    Args:
        df: DataFrame with performance metrics
    """
    if df.empty:
        st.warning("⚠️ No bowling type data available for this player.")
        return
    
    # Build HTML table
    html = """
    <style>
        .performance-table {
            width: 100%;
            border-collapse: collapse;
            margin: 2rem 0;
            font-family: 'Inter', sans-serif;
            background-color: #1a2332;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .performance-table thead {
            background-color: #0f1722;
        }
        
        .performance-table th {
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            color: #60a5fa;
            font-size: 0.95rem;
            border-bottom: 2px solid #2a3444;
        }
        
        .performance-table tbody tr {
            border-bottom: 1px solid #2a3444;
        }
        
        .performance-table tbody tr:last-child {
            border-bottom: none;
        }
        
        .performance-table tbody tr:hover {
            background-color: #243447;
        }
        
        .performance-table td {
            padding: 1rem;
            color: #e0e0e0;
            font-size: 0.9rem;
        }
        
        .performance-table td:first-child {
            font-weight: 500;
            color: #ffffff;
        }
        
        .metric-cell {
            font-weight: 600;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            display: inline-block;
            min-width: 60px;
            text-align: center;
        }
        
        .table-title {
            color: #00d9c0;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            margin-top: 2rem;
        }
    </style>
    
    <div class="table-title">Performance vs Bowling Types</div>
    <table class="performance-table">
        <thead>
            <tr>
                <th>Bowler Type</th>
                <th>Balls Faced</th>
                <th>Strike Rate</th>
                <th>Average</th>
                <th>Dot Ball %</th>
                <th>Boundary %</th>
            </tr>
        </thead>
        <tbody>
    """
    
    # Add rows
    for _, row in df.iterrows():
        # Get colors for each metric
        sr_color = get_color_for_metric(row['Strike Rate'], 'strike_rate')
        avg_color = get_color_for_metric(row['Average'], 'average')
        dot_color = get_color_for_metric(row['Dot Ball %'], 'dot_pct')
        boundary_color = get_color_for_metric(row['Boundary %'], 'boundary_pct')
        
        # Format values
        strike_rate = f"{row['Strike Rate']:.1f}" if pd.notna(row['Strike Rate']) else "-"
        average = f"{row['Average']:.1f}" if pd.notna(row['Average']) else "-"
        dot_pct = f"{row['Dot Ball %']:.1f}%" if pd.notna(row['Dot Ball %']) else "-"
        boundary_pct = f"{row['Boundary %']:.1f}%" if pd.notna(row['Boundary %']) else "-"
        
        html += f"""
            <tr>
                <td>{row['Bowler Type']}</td>
                <td>{int(row['Balls Faced'])}</td>
                <td><span class="metric-cell" style="background-color: {sr_color};">{strike_rate}</span></td>
                <td><span class="metric-cell" style="background-color: {avg_color};">{average}</span></td>
                <td><span class="metric-cell" style="background-color: {dot_color};">{dot_pct}</span></td>
                <td><span class="metric-cell" style="background-color: {boundary_color};">{boundary_pct}</span></td>
            </tr>
        """
    
    html += """
        </tbody>
    </table>
    """
    
    st.markdown(html, unsafe_allow_html=True)


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
