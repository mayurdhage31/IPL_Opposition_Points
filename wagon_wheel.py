"""
Module to generate wagon wheel visualizations for boundary distribution.

CRITICAL REQUIREMENTS:
- Zone mapping (EXACT positions from reference diagram):
  Zone 1 = Fine Leg (22.5°)
  Zone 2 = Square Leg (67.5°)
  Zone 3 = Mid Wicket (112.5°)
  Zone 4 = Mid On (157.5°)
  Zone 5 = Mid Off (202.5°)
  Zone 6 = Covers (247.5°)
  Zone 7 = Point (292.5°)
  Zone 8 = Third Man (337.5°)

- Polar orientation: 0° at TOP (North), angles increase CLOCKWISE
- ALL spokes MUST reach the boundary rope (constant radius)
- Counts are shown via marker size, not spoke length
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np


# Boundary rope radius (constant for all spokes)
ROPE_RADIUS = 100.0

# EXACT zone mapping per reference diagram
ZONE_MAPPING = {
    1: {"label": "Fine Leg", "theta": 22.5},
    2: {"label": "Square Leg", "theta": 67.5},
    3: {"label": "Mid Wicket", "theta": 112.5},
    4: {"label": "Mid On", "theta": 157.5},
    5: {"label": "Mid Off", "theta": 202.5},
    6: {"label": "Covers", "theta": 247.5},
    7: {"label": "Point", "theta": 292.5},
    8: {"label": "Third Man", "theta": 337.5},
}


def create_wagon_wheel(zone_df: pd.DataFrame, batter_name: str) -> go.Figure:
    """
    Create a polar wagon wheel visualization showing boundary distribution.
    
    ALL spokes reach the boundary rope (constant radius). Counts are shown
    via marker size at the rope endpoints.
    
    Args:
        zone_df: DataFrame with columns 'bat', 'fours_wagonZone1-8', 'sixes_wagonZone1-8'
        batter_name: Name of the batter (exact match with 'bat' column)
    
    Returns:
        Plotly figure object with polar scatterpolar chart
    """
    # Filter for the batter
    batter_zone = zone_df[zone_df['bat'] == batter_name]
    
    if batter_zone.empty:
        # Return empty figure with error message
        fig = go.Figure()
        fig.add_annotation(
            text=f"No data found for batter: {batter_name}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#ef4444")
        )
        fig.update_layout(
            plot_bgcolor='#1e293b',
            paper_bgcolor='#1e293b',
            height=600
        )
        return fig
    
    # Extract zone data
    batter_data = batter_zone.iloc[0]
    
    # Build zone data for all 8 zones
    zone_data = []
    for zone_num in range(1, 9):
        fours_col = f'fours_wagonZone{zone_num}'
        sixes_col = f'sixes_wagonZone{zone_num}'
        
        fours_count = int(batter_data.get(fours_col, 0))
        sixes_count = int(batter_data.get(sixes_col, 0))
        
        zone_data.append({
            'zone': zone_num,
            'label': ZONE_MAPPING[zone_num]['label'],
            'theta': ZONE_MAPPING[zone_num]['theta'],
            'fours': fours_count,
            'sixes': sixes_count
        })
    
    # Create figure with polar subplot
    fig = go.Figure()
    
    # ===== 1. Draw boundary rope (outer circle) =====
    rope_theta = list(range(0, 361, 5))  # 0 to 360 degrees
    rope_r = [ROPE_RADIUS] * len(rope_theta)
    
    fig.add_trace(go.Scatterpolar(
        r=rope_r,
        theta=rope_theta,
        mode='lines',
        line=dict(color='#475569', width=3),
        showlegend=False,
        hoverinfo='skip',
        name='Boundary Rope'
    ))
    
    # ===== 2. Draw zone division lines (8 spokes at 0, 45, 90, ..., 315 degrees) =====
    for division_angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        fig.add_trace(go.Scatterpolar(
            r=[0, ROPE_RADIUS],
            theta=[division_angle, division_angle],
            mode='lines',
            line=dict(color='#475569', width=1, dash='dot'),
            showlegend=False,
            hoverinfo='skip',
            opacity=0.4
        ))
    
    # ===== 3. Draw FOURS spokes (all reach boundary rope) =====
    # Build arrays for spokes: [theta1, theta1, None, theta2, theta2, None, ...]
    fours_theta = []
    fours_r = []
    fours_marker_theta = []
    fours_marker_r = []
    fours_marker_size = []
    fours_marker_text = []
    
    for zd in zone_data:
        if zd['fours'] > 0:
            # Spoke from center to rope
            fours_theta.extend([zd['theta'], zd['theta'], None])
            fours_r.extend([0, ROPE_RADIUS, None])
            
            # End marker at rope
            fours_marker_theta.append(zd['theta'])
            fours_marker_r.append(ROPE_RADIUS)
            
            # Marker size: scale from count (min=8, max=40)
            marker_size = min(8 + zd['fours'] * 2, 40)
            fours_marker_size.append(marker_size)
            
            fours_marker_text.append(
                f"<b>{zd['label']}</b><br>Fours: {zd['fours']}"
            )
    
    # Add fours spoke lines
    if fours_theta:
        fig.add_trace(go.Scatterpolar(
            r=fours_r,
            theta=fours_theta,
            mode='lines',
            line=dict(color='#3b82f6', width=4),
            showlegend=True,
            name='Fours',
            hoverinfo='skip'
        ))
        
        # Add fours end markers
        fig.add_trace(go.Scatterpolar(
            r=fours_marker_r,
            theta=fours_marker_theta,
            mode='markers',
            marker=dict(
                size=fours_marker_size,
                color='#3b82f6',
                line=dict(color='#1e40af', width=2),
                symbol='circle'
            ),
            text=fours_marker_text,
            hovertemplate='%{text}<extra></extra>',
            showlegend=False,
            name='Fours'
        ))
    
    # ===== 4. Draw SIXES spokes (all reach boundary rope) =====
    sixes_theta = []
    sixes_r = []
    sixes_marker_theta = []
    sixes_marker_r = []
    sixes_marker_size = []
    sixes_marker_text = []
    
    for zd in zone_data:
        if zd['sixes'] > 0:
            # Offset angle slightly to avoid overlap with fours
            offset_theta = zd['theta'] + 5
            
            # Spoke from center to rope
            sixes_theta.extend([offset_theta, offset_theta, None])
            sixes_r.extend([0, ROPE_RADIUS, None])
            
            # End marker at rope
            sixes_marker_theta.append(offset_theta)
            sixes_marker_r.append(ROPE_RADIUS)
            
            # Marker size: scale from count (min=8, max=40)
            marker_size = min(8 + zd['sixes'] * 2, 40)
            sixes_marker_size.append(marker_size)
            
            sixes_marker_text.append(
                f"<b>{zd['label']}</b><br>Sixes: {zd['sixes']}"
            )
    
    # Add sixes spoke lines
    if sixes_theta:
        fig.add_trace(go.Scatterpolar(
            r=sixes_r,
            theta=sixes_theta,
            mode='lines',
            line=dict(color='#ef4444', width=4),
            showlegend=True,
            name='Sixes',
            hoverinfo='skip'
        ))
        
        # Add sixes end markers
        fig.add_trace(go.Scatterpolar(
            r=sixes_marker_r,
            theta=sixes_marker_theta,
            mode='markers',
            marker=dict(
                size=sixes_marker_size,
                color='#ef4444',
                line=dict(color='#b91c1c', width=2),
                symbol='circle'
            ),
            text=sixes_marker_text,
            hovertemplate='%{text}<extra></extra>',
            showlegend=False,
            name='Sixes'
        ))
    
    # ===== 5. Configure polar layout =====
    # CRITICAL: rotation=90 puts 0° at TOP, direction="clockwise" for proper orientation
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                range=[0, ROPE_RADIUS],
                showticklabels=False,
                ticks="",
                showline=False,
                showgrid=False
            ),
            angularaxis=dict(
                rotation=90,          # Puts 0° at TOP (North)
                direction="clockwise",  # Angles increase clockwise
                tickmode="array",
                tickvals=[22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5],
                ticktext=[
                    "Fine Leg",
                    "Square Leg", 
                    "Mid Wicket",
                    "Mid On",
                    "Mid Off",
                    "Covers",
                    "Point",
                    "Third Man"
                ],
                tickfont=dict(size=11, color='#94a3b8'),
                showline=False,
                showgrid=False
            ),
            bgcolor='#1e293b'
        ),
        plot_bgcolor='#1e293b',
        paper_bgcolor='#1e293b',
        font=dict(color='#e2e8f0', family='Inter'),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='#475569',
            borderwidth=1,
            font=dict(size=12, color='#e2e8f0')
        ),
        margin=dict(l=80, r=80, t=100, b=80),
        height=650,
        hovermode='closest'
    )
    
    return fig


def plot_wagon_wheel(df: pd.DataFrame, batter_name: str) -> go.Figure:
    """
    Main entry point for creating wagon wheel visualization.
    
    Args:
        df: DataFrame with boundary zone data
        batter_name: Name of the batter
    
    Returns:
        Plotly figure object
    """
    return create_wagon_wheel(df, batter_name)


def validate_zone_positions():
    """
    Sanity-check function to visualize zone positions.
    Creates a wagon wheel with all zones showing constant spokes to verify layout.
    """
    # Create dummy data with 1 boundary in each zone
    dummy_data = {
        'bat': ['Test Batter'],
        'p_bat': [99999]
    }
    
    for zone in range(1, 9):
        dummy_data[f'fours_wagonZone{zone}'] = [5]
        dummy_data[f'sixes_wagonZone{zone}'] = [3]
    
    df = pd.DataFrame(dummy_data)
    fig = create_wagon_wheel(df, 'Test Batter')
    
    print("\n" + "="*60)
    print("ZONE POSITION VALIDATION")
    print("="*60)
    for zone, info in ZONE_MAPPING.items():
        print(f"Zone {zone}: {info['label']:15s} at {info['theta']:6.1f}°")
    print("="*60)
    print("\nExpected layout (clockwise from top):")
    print("  TOP (0°):     Straight down the ground")
    print("  22.5°:        Fine Leg (Zone 1)")
    print("  67.5°:        Square Leg (Zone 2)")
    print("  112.5°:       Mid Wicket (Zone 3)")
    print("  157.5°:       Mid On (Zone 4)")
    print("  202.5°:       Mid Off (Zone 5)")
    print("  247.5°:       Covers (Zone 6)")
    print("  292.5°:       Point (Zone 7)")
    print("  337.5°:       Third Man (Zone 8)")
    print("="*60 + "\n")
    
    return fig


if __name__ == "__main__":
    """
    Example usage and validation
    """
    import sys
    
    # Validate zone positions
    print("Running zone position validation...")
    val_fig = validate_zone_positions()
    val_fig.write_html('wagon_wheel_validation.html')
    print("✓ Validation chart saved to: wagon_wheel_validation.html")
    
    # Example with real data
    csv_path = 'batter_fours_sixes_by_zone_wide_2021_2023.csv'
    
    try:
        df = pd.read_csv(csv_path)
        print(f"\n✓ Loaded data: {len(df)} batters")
        
        # Get batter name from command line or use default
        if len(sys.argv) > 1:
            batter = sys.argv[1]
        else:
            # Use first batter with significant data
            batter = "Moeen Ali"  # From the sample data shown
        
        print(f"\nGenerating wagon wheel for: {batter}")
        fig = plot_wagon_wheel(df, batter)
        
        output_file = f'wagon_wheel_{batter.replace(" ", "_")}.html'
        fig.write_html(output_file)
        print(f"✓ Wagon wheel saved to: {output_file}")
        
        # Show available batters
        print(f"\nAvailable batters ({len(df)} total):")
        for idx, bat in enumerate(df['bat'].head(10), 1):
            print(f"  {idx}. {bat}")
        if len(df) > 10:
            print(f"  ... and {len(df) - 10} more")
        
        print("\nUsage: python wagon_wheel.py \"<batter_name>\"")
        
    except FileNotFoundError:
        print(f"\n✗ Error: Could not find {csv_path}")
        print("  Make sure the CSV file is in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
