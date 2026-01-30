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
    page_title="Opposition Batter Analysis",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for better formatting
st.markdown("""
<style>
    .writeup-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        line-height: 1.8;
        font-size: 16px;
    }
    
    .batter-header {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #1f77b4;
    }
    
    .batter-hand {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .insight {
        margin-bottom: 1.5rem;
        padding: 1rem;
        background-color: #f8f9fa;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
    }
    
    .insight p {
        margin: 0;
        line-height: 1.8;
    }
    
    .stats-footer {
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 2px solid #ddd;
        font-size: 0.9rem;
        color: #666;
        font-style: italic;
    }
    
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 500;
    }
    
    .player-selector {
        padding: 1rem;
        background-color: #f0f2f6;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    @media (max-width: 768px) {
        .writeup-container {
            padding: 1rem;
            font-size: 14px;
        }
        
        .batter-header {
            font-size: 1.5rem;
        }
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
    # Title
    st.title("🏏 Opposition Batter Analysis")
    st.markdown("### Tactical Write-ups for Bowlers")
    st.markdown("---")
    
    # Load data
    try:
        batting_df, merged_df, teams = load_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please ensure both CSV files are in the same directory as the app.")
        return
    
    # Sidebar for team and player selection
    with st.sidebar:
        st.header("⚙️ Selection")
        
        # Team selection
        selected_team = st.selectbox(
            "Select Opposition Team",
            options=teams,
            help="Choose the opposition team to analyze"
        )
        
        # Get players for selected team
        team_players = get_team_players_list(merged_df, selected_team)
        
        st.markdown("---")
        st.subheader("Players")
        st.caption("Top 7 run-scorers pre-selected. Deselect if needed.")
        
        # Player selection with multiselect (all pre-selected)
        selected_players = st.multiselect(
            "Select Players to Analyze",
            options=team_players,
            default=team_players,  # All 7 pre-selected
            help="Deselect players you don't want to analyze"
        )
        
        st.markdown("---")
        
        # Display count
        st.info(f"📊 {len(selected_players)} player(s) selected")
        
        # Export options
        st.markdown("---")
        st.subheader("📥 Export")
        st.caption("Export functionality coming soon")
    
    # Main content area
    if not selected_players:
        st.warning("⚠️ Please select at least one player from the sidebar.")
        return
    
    # Get data for selected players
    selected_df = merged_df[
        (merged_df['team_bat'] == selected_team) & 
        (merged_df['bat'].isin(selected_players))
    ].sort_values('team_runs_rank')
    
    # Navigation options
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Player navigation tabs or slider
        if len(selected_players) <= 7:
            # Use tabs for <= 7 players
            player_names = selected_df['bat'].tolist()
            tabs = st.tabs([f"{i+1}. {name}" for i, name in enumerate(player_names)])
            
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
        else:
            # Use slider for > 7 players (shouldn't happen with top 7, but good to have)
            player_idx = st.slider(
                "Select Player",
                min_value=0,
                max_value=len(selected_df) - 1,
                value=0,
                format="Player %d"
            )
            
            batter_data = selected_df.iloc[player_idx]
            
            # Navigation buttons
            col_prev, col_info, col_next = st.columns([1, 2, 1])
            
            with col_prev:
                if st.button("⬅️ Previous", disabled=(player_idx == 0)):
                    st.session_state['player_idx'] = player_idx - 1
                    st.rerun()
            
            with col_info:
                st.markdown(f"**Player {player_idx + 1} of {len(selected_df)}**")
            
            with col_next:
                if st.button("Next ➡️", disabled=(player_idx == len(selected_df) - 1)):
                    st.session_state['player_idx'] = player_idx + 1
                    st.rerun()
            
            st.markdown("---")
            
            # Generate and display write-up
            with st.spinner(f"Generating analysis for {batter_data['bat']}..."):
                try:
                    writeup = writeup_generator.generate_writeup(batting_df, batter_data)
                    
                    if writeup['num_insights'] < 3:
                        st.warning(f"⚠️ Limited data available for {batter_data['bat']}. Only {writeup['num_insights']} insight(s) generated.")
                    
                    display_writeup(writeup)
                    
                except Exception as e:
                    st.error(f"Error generating write-up: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>Cricket Tactical Analysis Tool | Data: IPL 2021-2023</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
