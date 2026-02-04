"""
Streamlit Application for Cricket Tactical Write-ups
Opposition Batter Analysis Tool
"""

import streamlit as st
import pandas as pd
from typing import List
import data_loader
import writeup_generator
import bowler_type_table
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import HexColor
from io import BytesIO
import re


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
        margin-left: 1.5rem;
        color: #e0e0e0;
        line-height: 1.8;
        list-style-type: disc;
    }
    
    .insight p {
        margin: 0;
        line-height: 1.8;
    }
    
    .additional-comments-label {
        color: #00d9c0;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .stTextArea > label {
        color: #00d9c0 !important;
        font-weight: 600;
    }
    
    .stTextArea textarea {
        background-color: #2a3444;
        border: 1px solid #3a4556;
        color: #e0e0e0;
        border-radius: 8px;
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
    
    /* Checkbox styling */
    .stCheckbox {
        color: #e0e0e0;
    }
    
    .stCheckbox > label {
        color: #e0e0e0 !important;
        font-size: 0.95rem;
        padding: 0.5rem 0;
    }
    
    .stCheckbox > label > div {
        color: #e0e0e0 !important;
    }
    
    /* Style the checkbox input */
    input[type="checkbox"] {
        accent-color: #3b82f6;
        width: 18px;
        height: 18px;
        cursor: pointer;
    }
    
    /* Toggle button styling */
    .element-container:has(button[kind="secondary"]) button {
        background-color: #2a3444 !important;
        border: 1px solid #3a4556 !important;
        color: #00d9c0 !important;
        font-size: 0.85rem !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    
    .element-container:has(button[kind="secondary"]) button:hover {
        background-color: #3a4556 !important;
        border-color: #00d9c0 !important;
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
    
    # Load bowler type data
    bowler_type_df = pd.read_csv('Batters_StrikeRateVSBowlerTypeNew.csv')
    
    # Load zone data
    zone_df = pd.read_csv('batter_fours_sixes_by_zone_wide_2021_2023.csv')
    
    return batting_df, merged_df, teams, bowler_type_df, zone_df


def generate_pdf(batting_df: pd.DataFrame, selected_df: pd.DataFrame, team_name: str) -> BytesIO:
    """Generate PDF document with write-ups for selected players."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.75*inch, bottomMargin=0.75*inch)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#00d9c0'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=HexColor('#9ca3af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    player_name_style = ParagraphStyle(
        'PlayerName',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=HexColor('#60a5fa'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    player_hand_style = ParagraphStyle(
        'PlayerHand',
        parent=styles['Normal'],
        fontSize=12,
        textColor=HexColor('#9ca3af'),
        spaceAfter=20
    )
    
    insight_style = ParagraphStyle(
        'Insight',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#1a2332'),
        spaceAfter=12,
        leading=16,
        leftIndent=20,
        bulletIndent=10,
        bulletFontName='Helvetica'
    )
    
    comments_label_style = ParagraphStyle(
        'CommentsLabel',
        parent=styles['Normal'],
        fontSize=12,
        textColor=HexColor('#00d9c0'),
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    comments_style = ParagraphStyle(
        'Comments',
        parent=styles['Normal'],
        fontSize=11,
        textColor=HexColor('#1a2332'),
        spaceAfter=12,
        leading=16,
        leftIndent=10
    )
    
    # Add title
    elements.append(Paragraph("Cricket Opposition Planning", title_style))
    elements.append(Paragraph(f"Opposition Team: {team_name}", subtitle_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Add each player's write-up
    for idx, (_, player_row) in enumerate(selected_df.iterrows()):
        batter_data = player_row
        player_name = batter_data['bat']
        
        try:
            writeup = writeup_generator.generate_writeup(batting_df, batter_data)
            
            # Player name and hand
            elements.append(Paragraph(writeup['batter_name'], player_name_style))
            elements.append(Paragraph(writeup['batting_hand'], player_hand_style))
            
            # Add insights as bullet points
            for insight in writeup['insights']:
                # Convert **text** to <b>text</b> for PDF
                formatted_insight = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', insight)
                # Convert *text* to <i>text</i>
                formatted_insight = re.sub(r'\*(.*?)\*', r'<i>\1</i>', formatted_insight)
                # Add bullet point
                bullet_text = f"• {formatted_insight}"
                elements.append(Paragraph(bullet_text, insight_style))
            
            # Add additional comments if they exist
            comments_key = f"comments_{player_name}"
            if comments_key in st.session_state and st.session_state[comments_key].strip():
                elements.append(Spacer(1, 0.2*inch))
                elements.append(Paragraph("Additional Comments:", comments_label_style))
                elements.append(Paragraph(st.session_state[comments_key], comments_style))
            
            # Add page break between players (except for the last one)
            if idx < len(selected_df) - 1:
                elements.append(PageBreak())
        
        except Exception as e:
            # Add error message for this player
            elements.append(Paragraph(f"Error generating write-up for {batter_data['bat']}: {str(e)}", insight_style))
            if idx < len(selected_df) - 1:
                elements.append(PageBreak())
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer


def get_team_players_list(merged_df: pd.DataFrame, team_name: str) -> List[str]:
    """Get list of player names for a team."""
    team_players = merged_df[merged_df['team_bat'] == team_name].copy()
    team_players = team_players.sort_values('team_runs_rank')
    return team_players['bat'].tolist()


def format_insight_text(insight: str) -> str:
    """Convert markdown-style formatting to HTML."""
    # Convert **text** to <strong>text</strong>
    import re
    # Replace **text** with <strong>text</strong>
    insight = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', insight)
    # Replace *text* with <em>text</em> (for any remaining single asterisks)
    insight = re.sub(r'\*(.*?)\*', r'<em>\1</em>', insight)
    return insight


def display_writeup(writeup_dict: dict, player_name: str):
    """Display a formatted write-up."""
    st.markdown(f"""
    <div class="writeup-container">
        <div class="batter-header">{writeup_dict['batter_name']}</div>
        <div class="batter-hand">{writeup_dict['batting_hand']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display insights as bullet points
    st.markdown('<ul style="color: #e0e0e0; line-height: 2;">', unsafe_allow_html=True)
    for i, insight in enumerate(writeup_dict['insights'], 1):
        formatted_insight = format_insight_text(insight)
        st.markdown(f"""
        <li style="margin-bottom: 1.5rem; font-size: 0.95rem;">
            {formatted_insight}
        </li>
        """, unsafe_allow_html=True)
    st.markdown('</ul>', unsafe_allow_html=True)
    
    # Add Additional Comments text area
    st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
    
    # Initialize the value in session state if it doesn't exist (before widget creation)
    comments_key = f"comments_{player_name}"
    if comments_key not in st.session_state:
        st.session_state[comments_key] = ""
    
    # Create the text area widget (it will automatically use and update session_state)
    st.text_area(
        "Additional Comments",
        key=comments_key,
        height=100,
        placeholder="Enter any additional tactical notes or observations..."
    )


def main():
    # Load data first
    try:
        batting_df, merged_df, teams, bowler_type_df, zone_df = load_data()
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        st.info("Please ensure all CSV files are in the same directory as the app.")
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
        
        
        # Team Selection section
        st.markdown('<div class="team-selection-header">Team Selection</div>', unsafe_allow_html=True)
        
        st.markdown('<p style="color: #9ca3af; font-size: 0.85rem; margin-bottom: 0.5rem;">Opposition</p>', unsafe_allow_html=True)
        selected_team = st.selectbox(
            "Opposition",
            options=teams,
            label_visibility="collapsed",
            help="Choose the opposition team to analyze",
            key="opposition_team"
        )
        
        # Get players for selected team
        team_players = get_team_players_list(merged_df, selected_team)
        
        # Opposition Players with checkboxes
        st.markdown('<p style="color: #ffffff; font-size: 1rem; margin-bottom: 1rem; margin-top: 1.5rem; font-weight: 600;">Opposition Players</p>', unsafe_allow_html=True)
        
        # Initialize session state for selected players if not exists
        if 'selected_players' not in st.session_state:
            st.session_state['selected_players'] = team_players.copy()
        
        # Update selected players when team changes
        if 'prev_team' not in st.session_state or st.session_state['prev_team'] != selected_team:
            st.session_state['selected_players'] = team_players.copy()
            st.session_state['prev_team'] = selected_team
        
        # Create checkboxes for each player
        selected_players = []
        for player in team_players:
            is_selected = st.checkbox(
                player,
                value=True,
                key=f"player_{player}"
            )
            if is_selected:
                selected_players.append(player)
        
        st.session_state['selected_players'] = selected_players
        
        # Download PDF button
        st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
        if st.button("📥 Download PDF", use_container_width=True, type="primary"):
            st.session_state['download_clicked'] = True
    
    # Main content area - Header
    st.markdown('<div class="main-header">Cricket Opposition Planning</div>', unsafe_allow_html=True)
    st.markdown('<div class="main-subtitle">Analyze player performance and opposition strategies</div>', unsafe_allow_html=True)
    
    # Get selected players from session state
    if 'selected_players' not in st.session_state or not st.session_state['selected_players']:
        st.warning("⚠️ Please select at least one player from the sidebar.")
        return
    
    selected_players = st.session_state['selected_players']
    
    # Get data for selected players only
    selected_df = merged_df[
        (merged_df['team_bat'] == selected_team) & 
        (merged_df['bat'].isin(selected_players))
    ].sort_values('team_runs_rank')
    
    if selected_df.empty:
        st.warning("⚠️ No data available for the selected players.")
        return
    
    # Player tabs at the top
    player_names = selected_df['bat'].tolist()
    tabs = st.tabs(player_names)
    
    for tab_idx, (tab, player_row) in enumerate(zip(tabs, selected_df.iterrows())):
        with tab:
            batter_data = player_row[1]
            batter_name = batter_data['bat']
            
            # Add toggle button in the top right corner
            col1, col2 = st.columns([3, 1])
            with col2:
                # Initialize toggle state for this player if not exists
                toggle_key = f"show_viz_{batter_name}"
                if toggle_key not in st.session_state:
                    st.session_state[toggle_key] = False
                
                # Create toggle button with shorter label to prevent text wrapping
                button_label = "📊 Show Visualizations" if not st.session_state[toggle_key] else "📝 Show Text"
                if st.button(button_label, key=f"toggle_{batter_name}", use_container_width=True, type="secondary"):
                    st.session_state[toggle_key] = not st.session_state[toggle_key]
                    st.rerun()
            
            # Display content based on toggle state
            if st.session_state[toggle_key]:
                # Show visualizations
                st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
                
                # Display bowler type table
                try:
                    table_df = bowler_type_table.generate_bowler_type_table(bowler_type_df, batter_name)
                    if not table_df.empty:
                        bowler_type_table.display_bowler_type_table_html(table_df)
                    else:
                        st.warning(f"⚠️ No bowling type data available for {batter_name}")
                except Exception as e:
                    st.error(f"Error generating table for {batter_name}: {str(e)}")
                
                # Display zone analysis (placeholder for future implementation)
                st.markdown('<div style="margin-top: 3rem;"></div>', unsafe_allow_html=True)
                try:
                    bowler_type_table.display_zone_analysis(zone_df, batter_name)
                except Exception as e:
                    st.error(f"Error generating zone analysis for {batter_name}: {str(e)}")
            else:
                # Show text write-up
                with st.spinner(f"Generating analysis for {batter_name}..."):
                    try:
                        writeup = writeup_generator.generate_writeup(batting_df, batter_data)
                        
                        # Check if we have sufficient insights
                        if writeup['num_insights'] < 3:
                            st.warning(f"⚠️ Limited data available for {batter_name}. Only {writeup['num_insights']} insight(s) generated.")
                        
                        display_writeup(writeup, batter_name)
                        
                    except Exception as e:
                        st.error(f"Error generating write-up for {batter_name}: {str(e)}")
    
    # Handle PDF download in sidebar
    with st.sidebar:
        if st.session_state.get('download_clicked', False):
            with st.spinner("Generating PDF..."):
                try:
                    pdf_buffer = generate_pdf(batting_df, selected_df, selected_team)
                    st.download_button(
                        label="📥 Download PDF",
                        data=pdf_buffer,
                        file_name=f"Opposition_Analysis_{selected_team.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
                    st.session_state['download_clicked'] = False
                except Exception as e:
                    st.error(f"Error generating PDF: {str(e)}")
                    st.session_state['download_clicked'] = False


if __name__ == "__main__":
    main()
