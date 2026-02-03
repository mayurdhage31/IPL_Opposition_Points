"""
Module to generate color-coded performance vs bowling types table
"""

import pandas as pd
import streamlit as st


def get_color_for_rank(rank, total_count, reverse=False):
    """
    Get color based on rank position (top 2 = green, middle 2 = yellow, bottom 2 = red).
    
    Args:
        rank: The rank (1 = best)
        total_count: Total number of items
        reverse: If True, reverse the logic (for dot ball % where lower is better)
    
    Returns:
        Color code as hex string
    """
    # Colors
    GREEN = '#10b981'  # Emerald green
    YELLOW = '#f59e0b'  # Amber
    RED = '#ef4444'  # Red
    
    if reverse:
        # For dot ball %, lower values are better, so reverse the ranking
        rank = total_count - rank + 1
    
    # Top 2 ranks get green
    if rank <= 2:
        return GREEN
    # Bottom 2 ranks get red
    elif rank > total_count - 2:
        return RED
    # Middle ranks get yellow
    else:
        return YELLOW


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
    
    # Select and rename columns for display (excluding balls_faced)
    display_df = batter_df[[
        'bowler.type',
        'strike_rate',
        'batting_avg',
        'dot_pct',
        'boundary_pct'
    ]].copy()
    
    # Rename columns
    display_df.columns = ['Bowler Type', 'Strike Rate', 'Average', 'Dot Ball %', 'Boundary %']
    
    # Sort by strike rate (descending) to show best performing types first
    display_df = display_df.sort_values('Strike Rate', ascending=False)
    
    # Reset index
    display_df = display_df.reset_index(drop=True)
    
    return display_df


def display_bowler_type_table_html(df: pd.DataFrame):
    """
    Display the bowler type table with rank-based color coding.
    
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
    total_rows = len(display_df)
    
    # Calculate ranks for each column (1 = best, higher is worse)
    # For Strike Rate, Average, Boundary % - higher is better
    display_df['SR_rank'] = display_df['Strike Rate'].rank(ascending=False, method='min')
    display_df['Avg_rank'] = display_df['Average'].rank(ascending=False, method='min')
    display_df['Boundary_rank'] = display_df['Boundary %'].rank(ascending=False, method='min')
    # For Dot Ball % - lower is better
    display_df['Dot_rank'] = display_df['Dot Ball %'].rank(ascending=True, method='min')
    
    # Function to apply text color styling to cells
    def apply_text_color_styling(row):
        # Get colors based on ranks
        sr_color = get_color_for_rank(int(row['SR_rank']), total_rows, reverse=False)
        avg_color = get_color_for_rank(int(row['Avg_rank']), total_rows, reverse=False)
        dot_color = get_color_for_rank(int(row['Dot_rank']), total_rows, reverse=True)
        boundary_color = get_color_for_rank(int(row['Boundary_rank']), total_rows, reverse=False)
        
        return [
            '',  # Bowler Type - no color
            f'color: {sr_color}; font-weight: 600',  # Strike Rate
            f'color: {avg_color}; font-weight: 600',  # Average
            f'color: {dot_color}; font-weight: 600',  # Dot Ball %
            f'color: {boundary_color}; font-weight: 600'  # Boundary %
        ]
    
    # Create display dataframe without rank columns
    display_clean = display_df[['Bowler Type', 'Strike Rate', 'Average', 'Dot Ball %', 'Boundary %']].copy()
    
    # Apply the styling
    styled = display_clean.style.apply(apply_text_color_styling, axis=1)
    
    # Format numeric columns
    styled = styled.format({
        'Strike Rate': lambda x: f'{x:.1f}' if pd.notna(x) else '-',
        'Average': lambda x: f'{x:.1f}' if pd.notna(x) else '-',
        'Dot Ball %': lambda x: f'{x:.1f}%' if pd.notna(x) else '-',
        'Boundary %': lambda x: f'{x:.1f}%' if pd.notna(x) else '-'
    })
    
    # Set table styles for better appearance
    styled = styled.set_table_styles([
        {'selector': 'thead th', 'props': [
            ('background', 'linear-gradient(135deg, #334155 0%, #1e293b 100%)'),
            ('color', '#94a3b8'),
            ('padding', '18px 20px'),
            ('text-align', 'left'),
            ('font-weight', '600'),
            ('font-size', '13px'),
            ('letter-spacing', '0.5px'),
            ('text-transform', 'uppercase'),
            ('border-bottom', '2px solid #00d9c0')
        ]},
        {'selector': 'tbody tr', 'props': [
            ('background', '#1e293b'),
            ('border-bottom', '1px solid rgba(71, 85, 105, 0.3)')
        ]},
        {'selector': 'tbody tr:hover', 'props': [
            ('background', 'rgba(51, 65, 85, 0.4)')
        ]},
        {'selector': 'tbody td', 'props': [
            ('padding', '16px 20px'),
            ('color', '#e2e8f0'),
            ('font-size', '15px')
        ]},
        {'selector': 'tbody td:first-child', 'props': [
            ('font-weight', '500'),
            ('color', '#f1f5f9')
        ]},
        {'selector': 'table', 'props': [
            ('width', '100%'),
            ('border-collapse', 'separate'),
            ('border-spacing', '0'),
            ('margin', '1.5rem 0'),
            ('background', 'linear-gradient(135deg, #1e293b 0%, #0f172a 100%)'),
            ('border-radius', '12px'),
            ('overflow', 'hidden'),
            ('box-shadow', '0 10px 30px rgba(0, 0, 0, 0.3)')
        ]}
    ])
    
    # Display the table
    st.dataframe(
        styled,
        use_container_width=True,
        hide_index=True,
        height=min(450, (len(display_clean) + 1) * 60 + 10)
    )
    
    # Add context info
    st.markdown(
        '<p style="color: #64748b; font-size: 13px; margin-top: 0.5rem; font-style: italic;">'
        'Performance statistics against different bowling types</p>',
        unsafe_allow_html=True
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
