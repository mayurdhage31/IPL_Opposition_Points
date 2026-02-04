"""
Module to generate wagon wheel visualizations for boundary distribution
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np


def create_wagon_wheel(zone_df: pd.DataFrame, batter_name: str) -> go.Figure:
    """
    Create a wagon wheel visualization showing fours and sixes distribution by zone.
    
    Zone layout (as per the reference image):
    Zone 1: Fine Leg (45-90 degrees from straight)
    Zone 2: Square Leg (0-45 degrees, right side)
    Zone 3: Mid Wicket (315-360 degrees)
    Zone 4: Mid On (270-315 degrees)
    Zone 5: Mid Off (225-270 degrees)
    Zone 6: Covers (180-225 degrees)
    Zone 7: Point (135-180 degrees)
    Zone 8: Third Man (90-135 degrees)
    
    Args:
        zone_df: DataFrame with zone boundary data
        batter_name: Name of the batter
    
    Returns:
        Plotly figure object
    """
    # Filter for the batter
    batter_zone = zone_df[zone_df['bat'] == batter_name]
    
    if batter_zone.empty:
        # Return empty figure
        fig = go.Figure()
        fig.add_annotation(
            text="No data available",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="#9ca3af")
        )
        return fig
    
    # Extract zone data
    batter_data = batter_zone.iloc[0]
    
    # Zone angle mappings (center angle for each zone in degrees)
    # Zones are arranged clockwise from the top (straight down the ground)
    zone_angles = {
        1: 67.5,   # Fine Leg
        2: 22.5,   # Square Leg
        3: 337.5,  # Mid Wicket
        4: 292.5,  # Mid On
        5: 247.5,  # Mid Off
        6: 202.5,  # Covers
        7: 157.5,  # Point
        8: 112.5   # Third Man
    }
    
    # Prepare data for all 8 zones
    fours_data = []
    sixes_data = []
    zone_names = {
        1: "Fine Leg",
        2: "Square Leg",
        3: "Mid Wicket",
        4: "Mid On",
        5: "Mid Off",
        6: "Covers",
        7: "Point",
        8: "Third Man"
    }
    
    for zone in range(1, 9):
        fours_col = f'fours_wagonZone{zone}'
        sixes_col = f'sixes_wagonZone{zone}'
        
        fours_count = int(batter_data[fours_col]) if fours_col in batter_data else 0
        sixes_count = int(batter_data[sixes_col]) if sixes_col in batter_data else 0
        
        angle = zone_angles[zone]
        
        fours_data.append({
            'zone': zone,
            'zone_name': zone_names[zone],
            'count': fours_count,
            'angle': angle
        })
        
        sixes_data.append({
            'zone': zone,
            'zone_name': zone_names[zone],
            'count': sixes_count,
            'angle': angle
        })
    
    # Create figure
    fig = go.Figure()
    
    # Add pitch representation (rectangle in center)
    pitch_length = 0.3
    pitch_width = 0.08
    fig.add_shape(
        type="rect",
        x0=-pitch_width/2, y0=-pitch_length/2,
        x1=pitch_width/2, y1=pitch_length/2,
        line=dict(color="#64748b", width=2),
        fillcolor="#475569",
        opacity=0.3
    )
    
    # Add batting crease indicator
    fig.add_shape(
        type="circle",
        x0=-0.05, y0=-0.05,
        x1=0.05, y1=0.05,
        line=dict(color="#00d9c0", width=2),
        fillcolor="#1e293b"
    )
    
    # Add zone division lines (8 zones, 45 degrees each)
    max_radius = 2.5
    for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
        rad = np.radians(angle)
        x_end = max_radius * np.sin(rad)
        y_end = max_radius * np.cos(rad)
        
        fig.add_shape(
            type="line",
            x0=0, y0=0,
            x1=x_end, y1=y_end,
            line=dict(color="#475569", width=1, dash="dot"),
            opacity=0.5
        )
    
    # Add boundary circle
    theta_circle = np.linspace(0, 2*np.pi, 100)
    x_circle = max_radius * np.cos(theta_circle)
    y_circle = max_radius * np.sin(theta_circle)
    
    fig.add_trace(go.Scatter(
        x=x_circle, y=y_circle,
        mode='lines',
        line=dict(color='#475569', width=2, dash='solid'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Plot fours (as lines from center)
    fours_x = []
    fours_y = []
    fours_text = []
    fours_counts = []
    
    for data in fours_data:
        if data['count'] > 0:
            angle_rad = np.radians(data['angle'])
            # Scale radius based on count (minimum 0.5, maximum 2.0)
            radius = min(0.5 + (data['count'] / 10) * 1.5, 2.0)
            
            x = radius * np.sin(angle_rad)
            y = radius * np.cos(angle_rad)
            
            fours_x.append(x)
            fours_y.append(y)
            fours_text.append(f"{data['zone_name']}<br>Fours: {data['count']}")
            fours_counts.append(data['count'])
    
    # Plot sixes (as lines from center, slightly offset angle)
    sixes_x = []
    sixes_y = []
    sixes_text = []
    sixes_counts = []
    
    for data in sixes_data:
        if data['count'] > 0:
            # Offset angle by 5 degrees to avoid overlap with fours
            angle_rad = np.radians(data['angle'] + 8)
            # Scale radius based on count (minimum 0.5, maximum 2.3)
            radius = min(0.5 + (data['count'] / 10) * 1.8, 2.3)
            
            x = radius * np.sin(angle_rad)
            y = radius * np.cos(angle_rad)
            
            sixes_x.append(x)
            sixes_y.append(y)
            sixes_text.append(f"{data['zone_name']}<br>Sixes: {data['count']}")
            sixes_counts.append(data['count'])
    
    # Add fours as scatter + lines
    if fours_x:
        # Add lines from center to each point
        for i in range(len(fours_x)):
            fig.add_trace(go.Scatter(
                x=[0, fours_x[i]],
                y=[0, fours_y[i]],
                mode='lines',
                line=dict(color='#3b82f6', width=3 + fours_counts[i]/2),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Add markers at endpoints
        fig.add_trace(go.Scatter(
            x=fours_x,
            y=fours_y,
            mode='markers',
            marker=dict(
                size=[8 + count*1.5 for count in fours_counts],
                color='#3b82f6',
                line=dict(color='#1e40af', width=2)
            ),
            text=fours_text,
            hovertemplate='%{text}<extra></extra>',
            name='Fours',
            showlegend=True
        ))
    
    # Add sixes as scatter + lines
    if sixes_x:
        # Add lines from center to each point
        for i in range(len(sixes_x)):
            fig.add_trace(go.Scatter(
                x=[0, sixes_x[i]],
                y=[0, sixes_y[i]],
                mode='lines',
                line=dict(color='#ef4444', width=3 + sixes_counts[i]/2),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        # Add markers at endpoints
        fig.add_trace(go.Scatter(
            x=sixes_x,
            y=sixes_y,
            mode='markers',
            marker=dict(
                size=[8 + count*1.5 for count in sixes_counts],
                color='#ef4444',
                line=dict(color='#b91c1c', width=2)
            ),
            text=sixes_text,
            hovertemplate='%{text}<extra></extra>',
            name='Sixes',
            showlegend=True
        ))
    
    # Add zone labels at the perimeter
    label_radius = max_radius + 0.3
    for zone, angle in zone_angles.items():
        angle_rad = np.radians(angle)
        x = label_radius * np.sin(angle_rad)
        y = label_radius * np.cos(angle_rad)
        
        fig.add_annotation(
            x=x, y=y,
            text=zone_names[zone],
            showarrow=False,
            font=dict(size=11, color='#94a3b8', family='Inter'),
            bgcolor='rgba(30, 41, 59, 0.8)',
            bordercolor='#475569',
            borderwidth=1,
            borderpad=4
        )
    
    # Update layout
    fig.update_layout(
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
        xaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-3, 3]
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            range=[-3, 3],
            scaleanchor="x",
            scaleratio=1
        ),
        margin=dict(l=40, r=40, t=80, b=40),
        height=600,
        hovermode='closest'
    )
    
    return fig
