"""
Streamlit Application for Cricket Tactical Write-ups
Opposition Batter Analysis Tool
"""

import streamlit as st
import pandas as pd
from typing import List
import data_loader
import writeup_generator


# Page configuration
st.set_page_config(
    page_title="Cricket Opposition Planning",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS matching the design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background-color: #1a2332;
        color: #e0e0e0;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #0f1722;
        border-right: 1px solid #2a3444;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #e0e0e0;
    }
    
    /* Logo styling */
    .logo-container {
        display: flex;
        align-items: center;
        padding: 1rem 0;
        margin-bottom: 2rem;
    }
    
    .logo-icon {
        width: 30px;
        height: 30px;
        background-color: #00d9c0;
        border-radius: 50%;
        margin-right: 10px;
    }
    
    .logo-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffffff;
    }
    
    /* Navigation items */
    .nav-section {
        margin-bottom: 2rem;
    }
    
    .nav-item {
        padding: 0.5rem 0;
        color: #9ca3af;
        font-size: 0.95rem;
        cursor: pointer;
    }
    
    .nav-item:hover {
        color: #00d9c0;
    }
    
    /* Team Selection section */
    .team-selection-header {
        color: #00d9c0;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 1rem;
        margin-top: 2rem;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background-color: #2a3444;
        border: 1px solid #3a4556;
        color: #e0e0e0;
    }
    
    .stSelectbox label {
        color: #9ca3af;
        font-size: 0.85rem;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background-color: #00d9c0;
        color: #0f1722;
        border: none;
        border-radius: 8px;
        padding: 0.75rem;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        background-color: #00c0aa;
    }
    
    /* Download button */
    .download-btn {
        background-color: transparent !important;
        border: 1px solid #3a4556 !important;
        color: #00d9c0 !important;
    }
    
    /* Main content header */
    .main-header {
        color: #00d9c0;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-subtitle {
        color: #9ca3af;
        font-size: 1rem;
        margin-bottom: 3rem;
    }
    
    /* Player analysis header */
    .player-analysis-header {
        color: #00d9c0;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 2rem;
        margin-top: 2rem;
    }
    
    /* Write-up container styling */
    .writeup-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 2rem 0;
    }
    
    .batter-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        color: #60a5fa;
    }
    
    .batter-hand {
        font-size: 1.2rem;
        color: #9ca3af;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .insight {
        margin-bottom: 1.5rem;
        padding: 1.5rem;
        background-color: #243447;
        border-radius: 8px;
        border-left: 4px solid #00d9c0;
        color: #e0e0e0;
        line-height: 1.8;
    }
    
    .insight p {
        margin: 0;
        line-height: 1.8;
    }
    
    .stats-footer {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 2px solid #2a3444;
        font-size: 0.9rem;
        color: #9ca3af;
        font-style: italic;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
        border-bottom: 1px solid #2a3444;
        padding-bottom: 0;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 0;
        color: #d1d5db;
        padding: 1rem 0.5rem;
        font-size: 0.95rem;
        font-weight: 500;
        border-bottom: 3px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #ffffff;
        background-color: transparent;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent;
        color: #ef4444;
        border-bottom: 3px solid #ef4444;
    }
    
    /* Multiselect styling */
    .stMultiSelect > div > div {
        background-color: #2a3444;
        border: 1px solid #3a4556;
    }
    
    .stMultiSelect label {
        color: #9ca3af;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    """Load all data (cached for performance)."""
    batting_df, merged_df, teams = data_loader.load_all_data(
        'Batting_data_IPL__2123.csv',
        'IPL_top7_run_scorers_by_team_2021_2023.csv'
    )
    return batting_df, merged_df, teams


def get_team_players_list(merged_df: pd.DataFrame, team_name: str) -> List[str]:
    """Get list of player names for a team."""
    team_players = merged_df[merged_df['team_bat'] == team_name].copy()
    team_players = team_players.sort_values('team_runs_rank')
    return team_players['bat'].tolist()


def display_writeup(writeup_dict: dict):
    """Display a formatted write-up."""
    st.markdown(f"""
    <div class="writeup-container">
        <div class="batter-header">{writeup_dict['batter_name']}</div>
        <div class="batter-hand">{writeup_dict['batting_hand']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display insights
    for i, insight in enumerate(writeup_dict['insights'], 1):
        st.markdown(f"""
        <div class="insight">
            {insight}
        </div>
        """, unsafe_allow_html=True)
    
    # Display stats footer
    st.markdown(f"""
    <div class="stats-footer">
        {writeup_dict['num_insights']} insights | {writeup_dict['word_count']} words | {writeup_dict['line_count']} lines
    </div>
    """, unsafe_allow_html=True)


def main():
    # Load data first
    try:
        batting_df, merged_df, teams = load_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please ensure both CSV files are in the same directory as the app.")
        return
    
    # Sidebar for team and player selection
    with st.sidebar:
        # Logo
        st.markdown("""
        <div class="logo-container">
            <div class="logo-icon"></div>
            <div class="logo-text">Wicky Sports</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("""
        <div class="nav-section">
            <div class="nav-item">🏠 Home</div>
            <div class="nav-item">🏏 Cricket</div>
            <div class="nav-item">🏀 NBA</div>
            <div class="nav-item">⚽ EPL</div>
            <div class="nav-item">🏈 AFL</div>
            <div class="nav-item">🏉 NRL</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Team Selection section
        st.markdown('<div class="team-selection-header">Team Selection</div>', unsafe_allow_html=True)
        
        st.markdown('<p style="color: #9ca3af; font-size: 0.85rem; margin-bottom: 0.5rem;">Your Team</p>', unsafe_allow_html=True)
        your_team = st.selectbox(
            "Your Team",
            options=teams,
            label_visibility="collapsed",
            key="your_team"
        )
        
        st.markdown('<p style="color: #9ca3af; font-size: 0.85rem; margin-bottom: 0.5rem; margin-top: 1rem;">Opposition</p>', unsafe_allow_html=True)
        selected_team = st.selectbox(
            "Opposition",
            options=teams,
            label_visibility="collapsed",
            help="Choose the opposition team to analyze",
            key="opposition_team"
        )
        
        # Get players for selected team
        team_players = get_team_players_list(merged_df, selected_team)
        
        st.markdown('<p style="color: #9ca3af; font-size: 0.85rem; margin-bottom: 0.5rem; margin-top: 1rem;">Opposition Player</p>', unsafe_allow_html=True)
        selected_player = st.selectbox(
            "Opposition Player",
            options=team_players,
            label_visibility="collapsed",
            help="Choose the player to analyze",
            key="opposition_player"
        )
        
        # Generate Insights button
        if st.button("Generate Insights"):
            st.session_state['generate_clicked'] = True
        
        # Download PPT button
        st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
        st.markdown("""
        <button class="card-button download-btn" style="width: 100%; text-align: center;">
            📥 Download PPT
        </button>
        """, unsafe_allow_html=True)
    
    # Main content area - Header
    st.markdown('<div class="main-header">Cricket Opposition Planning</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Analyze player performance and opposition strategies</div>', unsafe_allow_html=True)
    
    # Get all players for selected team
    team_players = get_team_players_list(merged_df, selected_team)
    selected_df = merged_df[merged_df['team_bat'] == selected_team].sort_values('team_runs_rank')
    
    if selected_df.empty:
        st.warning("⚠️ No data available for the selected team.")
        return
    
    # Player tabs at the top
    player_names = selected_df['bat'].tolist()
    tabs = st.tabs(player_names)
    
    for tab_idx, (tab, player_row) in enumerate(zip(tabs, selected_df.iterrows())):
        with tab:
            batter_data = player_row[1]
            
            # Generate write-up
            with st.spinner(f"Generating analysis for {batter_data['bat']}..."):
                try:
                    writeup = writeup_generator.generate_writeup(batting_df, batter_data)
                    
                    # Check if we have sufficient insights
                    if writeup['num_insights'] < 3:
                        st.warning(f"⚠️ Limited data available for {batter_data['bat']}. Only {writeup['num_insights']} insight(s) generated.")
                    
                    display_writeup(writeup)
                    
                except Exception as e:
                    st.error(f"Error generating write-up for {batter_data['bat']}: {str(e)}")


if __name__ == "__main__":
    main()
