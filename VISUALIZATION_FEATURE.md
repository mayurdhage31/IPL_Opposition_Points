# Visualization Feature Documentation

## Overview
Added a color-coded performance table and toggle functionality to switch between text analysis and visualizations for each batter.

## New Features

### 1. Color-Coded Performance vs Bowling Types Table
- Displays batter's performance against different bowling types
- **Columns:**
  - Bowler Type (Left arm pace, Right arm pace, Leg spin, Off spin, etc.)
  - Balls Faced
  - Strike Rate (calculated from runs/balls * 100)
  - Average
  - Dot Ball %
  - Boundary %

### 2. Color Coding Logic
The table uses intelligent color coding to highlight performance metrics:

#### For Strike Rate, Average, and Boundary %:
- **Green (#22c55e)**: Good performance
  - Strike Rate ≥ 140
  - Average ≥ 40
  - Boundary % ≥ 20%
- **Yellow (#facc15)**: Medium performance
  - Strike Rate ≥ 120
  - Average ≥ 25
  - Boundary % ≥ 15%
- **Red (#ef4444)**: Poor performance
  - Below medium thresholds

#### For Dot Ball % (Reverse Logic):
- **Green**: Dot Ball % ≤ 30% (Good - fewer dot balls)
- **Yellow**: Dot Ball % ≤ 40% (Medium)
- **Red**: Dot Ball % > 40% (Bad - too many dot balls)

### 3. Toggle Button
- Located in the top right corner of each batter's tab
- **"📊 Show Visualizations"**: Switch from text analysis to visualizations
- **"📝 Show Text"**: Switch back to text analysis
- State is preserved per player using session state
- Styled to match the app's dark theme

## Data Sources
1. `Batters_StrikeRateVSBowlerTypeNew.csv`: Contains batter performance vs different bowling types
2. `batter_fours_sixes_by_zone_wide_2021_2023.csv`: Zone-based boundary data (for future implementation)

## Technical Implementation

### New Module: `bowler_type_table.py`
Contains three main functions:
1. `get_color_for_metric()`: Determines color based on metric value and type
2. `generate_bowler_type_table()`: Generates the performance table for a specific batter
3. `display_bowler_type_table_html()`: Renders the table with HTML/CSS styling
4. `display_zone_analysis()`: Placeholder for future zone visualization

### Updated: `app.py`
- Added import for `bowler_type_table` module
- Updated `load_data()` to include new CSV files
- Modified player tab section to include toggle button
- Added conditional rendering based on toggle state
- Enhanced CSS with toggle button styling

## Usage
1. Select an opposition team from the sidebar
2. Navigate to any player's tab
3. Click the **"📊 Show Visualizations"** button in the top right corner
4. View the color-coded performance table
5. Click **"📝 Show Text"** to return to the text analysis

## Future Enhancements
- Zone-based boundary visualization (wagon wheel)
- Additional performance metrics
- Downloadable visualization reports
- Comparison between multiple batters

## Testing
Tested with Jos Buttler's data:
- ✓ Table generation working correctly
- ✓ Color coding logic functioning as expected
- ✓ Toggle functionality smooth and responsive
- ✓ Data loading and caching efficient

## GitHub Repository
All changes have been pushed to: https://github.com/mayurdhage31/IPL_Opposition_Points.git

## Screenshots
The visualization matches the design shown in the provided images with:
- Professional dark theme table design
- Clear color indicators for performance metrics
- Responsive layout
- Smooth toggle transitions
