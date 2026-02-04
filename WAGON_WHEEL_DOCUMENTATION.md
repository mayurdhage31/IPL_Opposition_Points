# Cricket Wagon Wheel - Boundary Distribution Visualization

## Overview

This implementation provides a **correct cricket wagon-wheel** visualization using Plotly, showing boundary distribution across 8 fielding zones. The visualization follows the exact zone positions from standard cricket field diagrams.

## Key Features

### ✅ CRITICAL REQUIREMENTS MET

1. **Exact Zone Mapping** (as per reference diagram):
   - Zone 1 = Fine Leg (22.5°)
   - Zone 2 = Square Leg (67.5°)
   - Zone 3 = Mid Wicket (112.5°)
   - Zone 4 = Mid On (157.5°)
   - Zone 5 = Mid Off (202.5°)
   - Zone 6 = Covers (247.5°)
   - Zone 7 = Point (292.5°)
   - Zone 8 = Third Man (337.5°)

2. **Polar Orientation**:
   - 0° at TOP (North) - represents straight down the ground
   - Angles increase CLOCKWISE (matching cricket field convention)
   - Uses Plotly's `scatterpolar` with `rotation=90` and `direction="clockwise"`

3. **Boundary Rope Contact**:
   - **ALL spokes reach the boundary rope** (constant radius = 100.0)
   - Spoke length is NOT proportional to boundary count
   - Instead, counts are shown via:
     - Marker size at spoke endpoints (scales from 8 to 40 pixels)
     - Hover text showing exact counts
     - Color coding: Blue for Fours, Red for Sixes

4. **Visual Design**:
   - Boundary rope drawn as outer circle
   - Zone division lines at 45° intervals
   - Separate spokes for fours and sixes (slightly offset to avoid overlap)
   - Dark theme matching the app's design system

## Files

### Core Implementation
- **`wagon_wheel.py`** - Main visualization module with three functions:
  - `create_wagon_wheel(zone_df, batter_name)` - Core visualization function
  - `plot_wagon_wheel(df, batter_name)` - Main entry point
  - `validate_zone_positions()` - Sanity-check function to verify zone layout

### Demo & Testing
- **`demo_wagon_wheel.py`** - Standalone interactive demo script
- **`wagon_wheel_validation.html`** - Zone position validation chart (auto-generated)

### Integration
- **`bowler_type_table.py`** - Contains `display_zone_analysis()` which integrates wagon wheel into Streamlit app
- **`app.py`** - Main Streamlit app (wagon wheel appears in "Show Visualizations" mode)

## Usage

### 1. Standalone Script (Command Line)

```bash
# Generate wagon wheel for a specific batter
python wagon_wheel.py "Aaron Finch"

# Outputs:
# - wagon_wheel_Aaron_Finch.html
# - wagon_wheel_validation.html
```

### 2. Interactive Demo

```bash
# Run interactive mode
python demo_wagon_wheel.py

# Options:
# - Enter batter name to generate wagon wheel
# - Type 'list' to see all batters
# - Type 'validate' to check zone positions
# - Type 'quit' to exit
```

```bash
# List top batters by boundary count
python demo_wagon_wheel.py --list

# Validate zone positions
python demo_wagon_wheel.py --validate

# Generate for specific batter
python demo_wagon_wheel.py "Shubman Gill"
```

### 3. Streamlit App Integration

The wagon wheel is automatically integrated into the main Streamlit app:

```bash
# Run the app
streamlit run app.py
```

**Steps to view wagon wheel:**
1. Select an opposition team from sidebar
2. Select player(s) to analyze
3. Click on a player's tab
4. Click **"📊 Show Visualizations"** button (top right)
5. Scroll down to **"Boundary Distribution by Zone"** section

### 4. Programmatic Usage

```python
import pandas as pd
from wagon_wheel import plot_wagon_wheel

# Load data
df = pd.read_csv('batter_fours_sixes_by_zone_wide_2021_2023.csv')

# Generate wagon wheel
fig = plot_wagon_wheel(df, "Virat Kohli")

# Save to HTML
fig.write_html('my_wagon_wheel.html')

# Or display in Streamlit
import streamlit as st
st.plotly_chart(fig, use_container_width=True)
```

## Data Format

### Required CSV Columns

```
bat                    # Batter name (string)
p_bat                  # Batter ID (integer)
fours_wagonZone1       # Fours in Zone 1 (integer)
fours_wagonZone2       # Fours in Zone 2 (integer)
...
fours_wagonZone8       # Fours in Zone 8 (integer)
sixes_wagonZone1       # Sixes in Zone 1 (integer)
sixes_wagonZone2       # Sixes in Zone 2 (integer)
...
sixes_wagonZone8       # Sixes in Zone 8 (integer)
```

### Example Data

```csv
p_bat,bat,fours_wagonZone1,fours_wagonZone2,...,sixes_wagonZone8
5334,"Aaron Finch",2,0,2,2,1,1,2,0,0,0,0,1,1,1,0,0
8917,"Moeen Ali",9,4,16,4,7,12,5,3,0,0,1,5,7,11,9,1
```

## Implementation Details

### Zone Position Mapping

The implementation uses a dictionary to ensure exact zone positions:

```python
ZONE_MAPPING = {
    1: {"label": "Fine Leg",    "theta": 22.5},
    2: {"label": "Square Leg",  "theta": 67.5},
    3: {"label": "Mid Wicket",  "theta": 112.5},
    4: {"label": "Mid On",      "theta": 157.5},
    5: {"label": "Mid Off",     "theta": 202.5},
    6: {"label": "Covers",      "theta": 247.5},
    7: {"label": "Point",       "theta": 292.5},
    8: {"label": "Third Man",   "theta": 337.5},
}
```

### Constant Spoke Length

All spokes reach the boundary rope:

```python
ROPE_RADIUS = 100.0

# For each zone (both fours and sixes):
# Spoke: r goes from [0, ROPE_RADIUS]
# Marker: placed at r = ROPE_RADIUS
```

### Marker Size Scaling

Marker sizes are proportional to boundary counts:

```python
# Minimum size: 8 pixels (for 1 boundary)
# Scaling: +2 pixels per boundary
# Maximum size: 40 pixels (capped)

marker_size = min(8 + count * 2, 40)
```

### Polar Layout Configuration

```python
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            range=[0, ROPE_RADIUS],
            showticklabels=False  # Hide radial tick labels
        ),
        angularaxis=dict(
            rotation=90,           # Puts 0° at TOP
            direction="clockwise", # Angles increase clockwise
            tickmode="array",
            tickvals=[22.5, 67.5, 112.5, ...],  # Zone center angles
            ticktext=["Fine Leg", "Square Leg", ...]  # Zone labels
        )
    )
)
```

## Validation

### Zone Position Validation

Run the validation function to verify zone positions:

```bash
python demo_wagon_wheel.py --validate
```

This generates a wagon wheel with constant boundaries in all zones, allowing you to visually confirm:
- ✅ Fine Leg is at top-right (22.5°)
- ✅ Third Man is at top-left (337.5°)
- ✅ Square Leg is on the right (67.5°)
- ✅ Point is on the left (292.5°)
- ✅ Mid Off is at bottom (202.5°)

### Expected Layout (Clockwise from Top)

```
             TOP (0°)
              |
              | Straight
              |
    Third Man * Fine Leg
    (337.5°)     (22.5°)
         \         /
          \       /
   Point   \     /   Square Leg
  (292.5°)  \   /    (67.5°)
             \ /
              X (Batter)
             / \
  (247.5°) /   \   (112.5°)
   Covers /     \ Mid Wicket
         /       \
        /         \
   Mid Off    Mid On
   (202.5°)  (157.5°)
```

## Visual Examples

### Spoke Rendering

Each boundary type (fours/sixes) is rendered as:
1. **Spoke line**: From center (r=0) to rope (r=100) at zone angle
2. **End marker**: Circle at rope (r=100) with size proportional to count
3. **Hover text**: Shows zone name, boundary type, and count

### Color Scheme

- **Fours**: Blue (#3b82f6) with dark blue border (#1e40af)
- **Sixes**: Red (#ef4444) with dark red border (#b91c1c)
- **Boundary Rope**: Gray (#475569)
- **Zone Divisions**: Dotted gray (#475569, opacity 40%)
- **Background**: Dark slate (#1e293b)

### Offset for Overlap Prevention

Sixes spokes are offset by +5° to prevent overlap with fours:

```python
# Fours: exact zone angle
fours_theta = zone_theta

# Sixes: slight offset
sixes_theta = zone_theta + 5
```

## Troubleshooting

### Issue: Wrong Zone Positions

**Solution**: Make sure you're using `rotation=90` and `direction="clockwise"` in polar layout:

```python
polar=dict(
    angularaxis=dict(
        rotation=90,          # Critical!
        direction="clockwise" # Critical!
    )
)
```

### Issue: Spokes Not Reaching Rope

**Problem**: Using variable radius based on counts

**Solution**: Always use constant radius:

```python
# WRONG
radius = count * scale_factor

# CORRECT
radius = ROPE_RADIUS  # Always 100.0
```

### Issue: Batter Not Found

**Check**:
1. Exact spelling (case-sensitive)
2. Use quotes for names with spaces: `"Aaron Finch"`
3. Run `--list` to see available batters

```bash
# List batters
python demo_wagon_wheel.py --list

# Use exact name
python demo_wagon_wheel.py "Aaron Finch"
```

### Issue: Zones Appear Mirrored/Rotated

**Cause**: Incorrect angular axis configuration

**Fix**: Verify these settings:
- `rotation=90` (not 0, 180, or 270)
- `direction="clockwise"` (not "counterclockwise")

## Technical Specifications

### Dependencies

```txt
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
streamlit>=1.28.0  (for app integration)
```

### Performance

- **Load time**: ~2-3 seconds for 259 batters
- **Render time**: ~0.5 seconds per wagon wheel
- **File size**: ~500KB per HTML output

### Browser Compatibility

Generated HTML files work in all modern browsers:
- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## Future Enhancements

Potential improvements (not currently implemented):

1. **Animation**: Animate spokes drawing from center to rope
2. **Comparison Mode**: Side-by-side wagon wheels for multiple batters
3. **Interactive Filtering**: Toggle fours/sixes visibility
4. **Zone Statistics**: Summary table showing top zones
5. **Export Options**: PNG/SVG export in addition to HTML
6. **Pitch Overlay**: Add cricket pitch graphic in center
7. **Match Filter**: Filter by specific matches/seasons

## License & Credits

**Implementation**: Cricket Opposition Planning Tool  
**Visualization Library**: Plotly (https://plotly.com/)  
**Data Format**: IPL 2021-2023 Boundary Distribution  

---

## Quick Reference

```bash
# Validate zone positions
python demo_wagon_wheel.py --validate

# List all batters
python demo_wagon_wheel.py --list

# Generate wagon wheel
python demo_wagon_wheel.py "Batter Name"

# Interactive mode
python demo_wagon_wheel.py

# Streamlit app
streamlit run app.py
```

**Zone Quick Reference**:
- Z1=22.5° (Fine Leg) | Z2=67.5° (Square Leg)
- Z3=112.5° (Mid Wicket) | Z4=157.5° (Mid On)
- Z5=202.5° (Mid Off) | Z6=247.5° (Covers)
- Z7=292.5° (Point) | Z8=337.5° (Third Man)

---

**Last Updated**: 2026-02-04  
**Version**: 1.0.0
