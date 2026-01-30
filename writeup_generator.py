"""
Write-up Generator Module
Generates tactical cricket write-ups for batters with 5 key insights.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import outlier_detector
import zone_mapper


def format_metric_first_occurrence(avg: float, sr: float) -> str:
    """Format metrics for first occurrence with labels."""
    return f"{avg:.0f} avg; {sr:.0f} SR"


def format_metric_subsequent(avg: float, sr: float) -> str:
    """Format metrics for subsequent occurrences without labels."""
    return f"({avg:.0f}; {sr:.0f})"


def get_top_shots(batter_data: pd.Series, bowling_type: str, top_n: int = 2) -> List[Tuple[str, float]]:
    """
    Get top N shots for a bowling type (pace or spin).
    
    Args:
        batter_data: Series with batter's data
        bowling_type: 'pace' or 'spin'
        top_n: Number of top shots to return
        
    Returns:
        List of (shot_name, percentage) tuples
    """
    # Get all shot columns for this bowling type
    shot_cols = [col for col in batter_data.index if f'pct_shots_by_shot_type_vs_{bowling_type}_' in col]
    
    # Extract shot values
    shots = []
    for col in shot_cols:
        pct = batter_data[col]
        if pd.notna(pct) and pct > 0:
            # Extract shot name from column
            shot_name = col.replace(f'pct_shots_by_shot_type_vs_{bowling_type}_', '').replace('_', ' ')
            shots.append((shot_name, pct))
    
    # Sort by percentage and get top N
    shots.sort(key=lambda x: x[1], reverse=True)
    return shots[:top_n]


def get_top_zones(batter_data: pd.Series, zone_type: str, batting_hand: str, top_n: int = 3) -> List[Tuple[str, float]]:
    """
    Get top N wagon zones for boundaries or dismissals.
    
    Args:
        batter_data: Series with batter's data
        zone_type: 'boundaries' or 'caught_dismissals'
        batting_hand: 'LHB' or 'RHB'
        top_n: Number of top zones to return
        
    Returns:
        List of (zone_name, percentage) tuples
    """
    zones = []
    
    for zone_num in range(1, 9):
        col = f'pct_{zone_type}_in_wagon_zone_{zone_num}'
        pct = batter_data[col]
        
        if pd.notna(pct) and pct > 0:
            zone_name = zone_mapper.get_zone_name(zone_num, batting_hand)
            zones.append((zone_name, pct))
    
    # Sort by percentage and get top N
    zones.sort(key=lambda x: x[1], reverse=True)
    return zones[:top_n]


def generate_length_insight(stats: Dict, first_metric_used: List[bool]) -> str:
    """
    Generate Insight 1: Performance against different lengths with outliers.
    
    Args:
        stats: Statistics dictionary from outlier_detector
        first_metric_used: List to track if first metric format has been used
        
    Returns:
        Formatted insight string or None if no data
    """
    length_outliers = stats['length_outliers']
    strengths = length_outliers['strengths']
    weaknesses = length_outliers['weaknesses']
    
    if not strengths and not weaknesses:
        return None
    
    parts = []
    
    # Add strengths
    if strengths:
        strength_parts = []
        for i, (length, avg, sr, z_score) in enumerate(strengths[:2]):  # Max 2 strengths
            if not first_metric_used[0]:
                metric_str = format_metric_first_occurrence(avg, sr)
                first_metric_used[0] = True
            else:
                metric_str = format_metric_subsequent(avg, sr)
            strength_parts.append(f"{length} {metric_str}")
        
        if len(strength_parts) == 1:
            parts.append(f"Strong vs {strength_parts[0]}")
        else:
            parts.append(f"Strong vs {' and '.join(strength_parts)}")
    
    # Add weaknesses
    if weaknesses:
        weakness_parts = []
        for i, (length, avg, sr, z_score) in enumerate(weaknesses[:2]):  # Max 2 weaknesses
            if not first_metric_used[0]:
                metric_str = format_metric_first_occurrence(avg, sr)
                first_metric_used[0] = True
            else:
                metric_str = format_metric_subsequent(avg, sr)
            weakness_parts.append(f"{length} {metric_str}")
        
        if len(weakness_parts) == 1:
            parts.append(f"weak vs {weakness_parts[0]}")
        else:
            parts.append(f"weak vs {' and '.join(weakness_parts)}")
    
    # Add bowling advice
    if weaknesses:
        weak_lengths = [w[0] for w in weaknesses[:2]]
        if len(weak_lengths) == 1:
            parts.append(f"Target {weak_lengths[0]}")
        else:
            parts.append(f"Target {weak_lengths[0]}")
    
    insight = ". ".join(parts) + "."
    return f"**Length:** {insight}"


def generate_line_insight(stats: Dict, first_metric_used: List[bool]) -> str:
    """
    Generate Insight 2: Performance against different lines with outliers.
    
    Args:
        stats: Statistics dictionary from outlier_detector
        first_metric_used: List to track if first metric format has been used
        
    Returns:
        Formatted insight string or None if no data
    """
    line_outliers = stats['line_outliers']
    strengths = line_outliers['strengths']
    weaknesses = line_outliers['weaknesses']
    
    if not strengths and not weaknesses:
        return None
    
    parts = []
    
    # Add strengths
    if strengths:
        strength_parts = []
        for i, (line, avg, sr, z_score) in enumerate(strengths[:2]):
            if not first_metric_used[0]:
                metric_str = format_metric_first_occurrence(avg, sr)
                first_metric_used[0] = True
            else:
                metric_str = format_metric_subsequent(avg, sr)
            strength_parts.append(f"{line} {metric_str}")
        
        if len(strength_parts) == 1:
            parts.append(f"Excels {strength_parts[0]}")
        else:
            parts.append(f"Excels {' and '.join(strength_parts)}")
    
    # Add weaknesses
    if weaknesses:
        weakness_parts = []
        for i, (line, avg, sr, z_score) in enumerate(weaknesses[:2]):
            if not first_metric_used[0]:
                metric_str = format_metric_first_occurrence(avg, sr)
                first_metric_used[0] = True
            else:
                metric_str = format_metric_subsequent(avg, sr)
            weakness_parts.append(f"{line} {metric_str}")
        
        if len(weakness_parts) == 1:
            parts.append(f"struggles {weakness_parts[0]}")
        else:
            parts.append(f"struggles {' and '.join(weakness_parts)}")
    
    # Add bowling advice
    if weaknesses:
        weak_lines = [w[0] for w in weaknesses[:2]]
        if len(weak_lines) == 1:
            parts.append(f"Bowl {weak_lines[0]}")
        else:
            parts.append(f"Bowl {weak_lines[0]}")
    
    insight = ". ".join(parts) + "."
    return f"**Line:** {insight}"


def generate_shot_insight(batter_data: pd.Series) -> str:
    """
    Generate Insight 3: Shot selection tendencies.
    
    Args:
        batter_data: Series with batter's data
        
    Returns:
        Formatted insight string or None if no data
    """
    # Get top 2 shots for pace and spin
    pace_shots = get_top_shots(batter_data, 'pace', 2)
    spin_shots = get_top_shots(batter_data, 'spin', 2)
    
    if not pace_shots and not spin_shots:
        return None
    
    parts = []
    
    if pace_shots:
        shot_strs = [f"{shot} ({pct:.0f}%)" for shot, pct in pace_shots]
        parts.append(f"vs Pace: {', '.join(shot_strs)}")
    
    if spin_shots:
        shot_strs = [f"{shot} ({pct:.0f}%)" for shot, pct in spin_shots]
        parts.append(f"vs Spin: {', '.join(shot_strs)}")
    
    insight = "; ".join(parts) + "."
    return f"**Shots:** {insight}"


def generate_boundary_insight(batter_data: pd.Series, batting_hand: str) -> str:
    """
    Generate Insight 4: Most common boundary-scoring zones.
    
    Args:
        batter_data: Series with batter's data
        batting_hand: 'LHB' or 'RHB'
        
    Returns:
        Formatted insight string or None if no data
    """
    top_zones = get_top_zones(batter_data, 'boundaries', batting_hand, 3)
    
    if not top_zones:
        return None
    
    zone_strs = [f"{zone} ({pct:.0f}%)" for zone, pct in top_zones]
    zones_text = ", ".join(zone_strs)
    
    # Field setting advice
    top_2_zones = [zone for zone, _ in top_zones[:2]]
    if len(top_2_zones) == 2:
        advice = f"Protect {top_2_zones[0]} and {top_2_zones[1]}"
    else:
        advice = f"Protect {top_2_zones[0]}"
    
    insight = f"Top zones: {zones_text}. {advice}."
    return f"**Boundaries:** {insight}"


def generate_dismissal_insight(batter_data: pd.Series, batting_hand: str) -> str:
    """
    Generate Insight 5: Most common dismissal zones.
    
    Args:
        batter_data: Series with batter's data
        batting_hand: 'LHB' or 'RHB'
        
    Returns:
        Formatted insight string or None if no data
    """
    top_zones = get_top_zones(batter_data, 'caught_dismissals', batting_hand, 3)
    
    if not top_zones:
        return None
    
    zone_strs = [f"{zone} ({pct:.0f}%)" for zone, pct in top_zones]
    zones_text = ", ".join(zone_strs)
    
    # Field setting advice
    top_2_zones = [zone for zone, _ in top_zones[:2]]
    if len(top_2_zones) == 2:
        advice = f"Place catchers at {top_2_zones[0]} and {top_2_zones[1]}"
    else:
        advice = f"Place catcher at {top_2_zones[0]}"
    
    insight = f"Catch zones: {zones_text}. {advice}."
    return f"**Dismissals:** {insight}"


def count_words(text: str) -> int:
    """Count words in a text string."""
    return len(text.split())


def count_lines(text: str) -> int:
    """Count lines in a text string."""
    return len([line for line in text.split('\n') if line.strip()])


def generate_writeup(batting_df: pd.DataFrame, batter_data: pd.Series) -> Dict:
    """
    Generate complete tactical write-up for a batter.
    
    Args:
        batting_df: Full batting DataFrame (for z-score calculations)
        batter_data: Series with specific batter's data
        
    Returns:
        Dictionary with write-up and metadata
    """
    batter_id = batter_data['batter_id']
    batter_name = batter_data['bat']
    batting_hand = batter_data['batting_hand']
    
    # Get outlier statistics
    stats = outlier_detector.get_all_length_line_stats(batting_df, batter_id)
    
    # Track if first metric format has been used
    first_metric_used = [False]
    
    # Generate all 5 insights
    insights = []
    
    # Insight 1: Length performance
    length_insight = generate_length_insight(stats, first_metric_used)
    if length_insight:
        insights.append(length_insight)
    
    # Insight 2: Line performance
    line_insight = generate_line_insight(stats, first_metric_used)
    if line_insight:
        insights.append(line_insight)
    
    # Insight 3: Shot selection
    shot_insight = generate_shot_insight(batter_data)
    if shot_insight:
        insights.append(shot_insight)
    
    # Insight 4: Boundary zones
    boundary_insight = generate_boundary_insight(batter_data, batting_hand)
    if boundary_insight:
        insights.append(boundary_insight)
    
    # Insight 5: Dismissal zones
    dismissal_insight = generate_dismissal_insight(batter_data, batting_hand)
    if dismissal_insight:
        insights.append(dismissal_insight)
    
    # Combine all insights
    writeup_text = "\n\n".join(insights)
    
    # Count words and lines
    word_count = count_words(writeup_text)
    line_count = count_lines(writeup_text)
    
    return {
        'batter_name': batter_name,
        'batting_hand': batting_hand,
        'writeup': writeup_text,
        'insights': insights,
        'word_count': word_count,
        'line_count': line_count,
        'num_insights': len(insights)
    }


if __name__ == "__main__":
    # Test write-up generation
    import data_loader
    
    batting_df, merged_df, teams = data_loader.load_all_data(
        'Batting_data_IPL__2123.csv',
        'IPL_top7_run_scorers_by_team_2021_2023.csv'
    )
    
    # Test with first player from Mumbai Indians
    mi_players = merged_df[merged_df['team_bat'] == 'Mumbai Indians']
    test_player = mi_players.iloc[0]
    
    writeup = generate_writeup(batting_df, test_player)
    
    print(f"=== {writeup['batter_name']} ({writeup['batting_hand']}) ===\n")
    print(writeup['writeup'])
    print(f"\n--- Stats: {writeup['num_insights']} insights, {writeup['word_count']} words, {writeup['line_count']} lines ---")
