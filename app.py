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
    
    /* Card styling */
    .insight-card {
        background-color: #243447;
        border: 1px solid #2a3f57;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        height: 100%;
    }
    
    .card-ai {
        border-left: 3px solid #00d9c0;
        background: linear-gradient(135deg, #243447 0%, #1e3a4a 100%);
    }
    
    .card-strength {
        border-left: 3px solid #10b981;
        background: linear-gradient(135deg, #243447 0%, #1e3f33 100%);
    }
    
    .card-weakness {
        border-left: 3px solid #f59e0b;
        background: linear-gradient(135deg, #243447 0%, #3f3220 100%);
    }
    
    .card-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    .card-header-ai {
        color: #00d9c0;
    }
    
    .card-header-strength {
        color: #10b981;
    }
    
    .card-header-weakness {
        color: #f59e0b;
    }
    
    .card-icon {
        margin-right: 0.5rem;
        font-size: 1.2rem;
    }
    
    .card-content {
        color: #d1d5db;
        font-size: 0.9rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .card-bullet {
        margin-bottom: 0.5rem;
        padding-left: 1rem;
    }
    
    .card-button {
        background-color: rgba(0, 217, 192, 0.1);
        border: 1px solid #00d9c0;
        color: #00d9c0;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 500;
        cursor: pointer;
        margin-top: 1rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1a2332;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #2a3444;
        border-radius: 8px;
        color: #9ca3af;
        padding: 0.5rem 1rem;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #00d9c0;
        color: #0f1722;
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
    """Display a formatted write-up in card layout."""
    # Create three columns for the card layout
    col1, col2, col3 = st.columns(3)
    
    insights = writeup_dict['insights']
    
    # AI Insights Card (combines length and line insights)
    with col1:
        ai_insights = []
        for insight in insights[:2]:  # Length and Line insights
            ai_insights.append(insight)
        
        st.markdown(f"""
        <div class="insight-card card-ai">
            <div class="card-header card-header-ai">
                <span class="card-icon">🎯</span> AI Insights
            </div>
            <div class="card-content">
                <div class="card-bullet">• {writeup_dict['batter_name']} - {writeup_dict['batting_hand']}</div>
                {"".join([f'<div class="card-bullet">• {insight.replace("**", "").replace(":", ":")}</div>' for insight in ai_insights])}
            </div>
            <button class="card-button">+ Add Insight</button>
        </div>
        """, unsafe_allow_html=True)
    
    # Strengths Card
    with col2:
        strength_insights = []
        # Extract strength-related content
        for insight in insights:
            if 'Strong' in insight or 'Excels' in insight or 'Boundaries' in insight:
                strength_insights.append(insight)
        
        st.markdown(f"""
        <div class="insight-card card-strength">
            <div class="card-header card-header-strength">
                <span class="card-icon">📈</span> Strengths
            </div>
            <div class="card-content">
                <div class="card-bullet">✓ Generate insights to see player strengths</div>
                {"".join([f'<div class="card-bullet">✓ {insight.replace("**", "").replace(":", ":")}</div>' for insight in strength_insights[:2]])}
            </div>
            <button class="card-button">+ Add Strength</button>
        </div>
        """, unsafe_allow_html=True)
    
    # Areas for Improvement Card
    with col3:
        weakness_insights = []
        # Extract weakness-related content
        for insight in insights:
            if 'weak' in insight or 'struggles' in insight or 'Dismissals' in insight or 'Target' in insight:
                weakness_insights.append(insight)
        
        st.markdown(f"""
        <div class="insight-card card-weakness">
            <div class="card-header card-header-weakness">
                <span class="card-icon">⚠️</span> Areas for Improvement
            </div>
            <div class="card-content">
                <div class="card-bullet">⚠ Generate insights to see areas for improvement</div>
                {"".join([f'<div class="card-bullet">⚠ {insight.replace("**", "").replace(":", ":")}</div>' for insight in weakness_insights[:2]])}
            </div>
            <button class="card-button">+ Add Weakness</button>
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
    
    # Get data for selected player
    player_data = merged_df[
        (merged_df['team_bat'] == selected_team) & 
        (merged_df['bat'] == selected_player)
    ]
    
    if player_data.empty:
        st.warning("⚠️ No data available for the selected player.")
        return
    
    batter_data = player_data.iloc[0]
    
    # Player Analysis Header
    st.markdown(f'<div class="player-analysis-header">Player Analysis: {selected_player}</div>', unsafe_allow_html=True)
    
    # Generate write-up
    try:
        writeup = writeup_generator.generate_writeup(batting_df, batter_data)
        
        # Check if we have sufficient insights
        if writeup['num_insights'] < 3:
            st.info(f"ℹ️ Limited data available for {batter_data['bat']}. Only {writeup['num_insights']} insight(s) generated.")
        
        display_writeup(writeup)
        
    except Exception as e:
        st.error(f"Error generating write-up for {batter_data['bat']}: {str(e)}")


if __name__ == "__main__":
    main()
