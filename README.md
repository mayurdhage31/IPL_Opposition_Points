# Cricket Tactical Write-ups Application

A Streamlit-based application that generates tactical cricket write-ups for opposition batters, providing actionable insights for bowlers and fielding strategies.

## Features

- **Opposition Team Selection**: Choose from 10 IPL teams
- **Player Analysis**: Automatic selection of top 7 run-scorers per team with option to deselect
- **Tactical Insights**: Generates up to 5 key insights per batter:
  1. Performance vs different pitch lengths (with outlier detection)
  2. Performance vs different pitch lines (with outlier detection)
  3. Shot selection tendencies (vs pace and spin)
  4. Boundary-scoring zones with fielding recommendations
  5. Dismissal zones with catching position advice
- **Statistical Analysis**: Uses z-score outlier detection to identify strengths and weaknesses
- **Mobile-Responsive**: Clean, readable design optimized for all devices
- **LHB/RHB Handling**: Correctly maps wagon zones with lateral flipping for left-handed batters

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository to your local machine

2. Navigate to the project directory:
```bash
cd NewProject3001
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

Start the Streamlit app:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Application

1. **Select Opposition Team**: Use the dropdown in the sidebar to choose a team
2. **Select Players**: All top 7 players are pre-selected. Deselect any players you don't want to analyze
3. **View Write-ups**: Navigate through player tabs to view tactical insights
4. **Review Insights**: Each write-up contains actionable bowling and fielding strategies

## Data Files

The application requires two CSV files:

1. **Batting_data_IPL__2123.csv**: Contains detailed batting statistics
   - Performance metrics vs different lengths and lines
   - Shot selection percentages vs pace and spin
   - Boundary and dismissal zone distributions

2. **IPL_top7_run_scorers_by_team_2021_2023.csv**: Contains team rosters
   - Top 7 run-scorers per team
   - Team identification
   - Player ranking by runs scored

## Project Structure

```
NewProject3001/
├── app.py                                      # Main Streamlit application
├── data_loader.py                             # CSV data loading and merging
├── zone_mapper.py                             # Wagon zone to field position mapping
├── outlier_detector.py                        # Statistical outlier detection
├── writeup_generator.py                       # Tactical write-up generation
├── utils.py                                   # Utility functions
├── test_validation.py                         # Validation test script
├── requirements.txt                           # Python dependencies
├── README.md                                  # This file
├── Batting_data_IPL__2123.csv                # Batting statistics data
└── IPL_top7_run_scorers_by_team_2021_2023.csv # Team selection data
```

## Module Documentation

### data_loader.py
Handles loading and merging of CSV data files. Infers batting hand (LHB/RHB) for each player.

### zone_mapper.py
Maps wagon zone numbers (1-8) to field position names:
- **RHB**: Standard mapping (Zone 1 = Fine Leg, Zone 5 = Mid Off, etc.)
- **LHB**: Laterally flipped (Zone 5 = Mid On for LHB)

### outlier_detector.py
Uses z-score statistical analysis to identify:
- Strong performance areas (z-score > 1.5)
- Weak performance areas (z-score < -1.5)
- Applied to both pitch lengths and pitch lines

### writeup_generator.py
Generates tactical write-ups following strict formatting rules:
- Maximum 150 words
- Maximum 10 lines
- First metric occurrence: "44 avg; 156 SR"
- Subsequent occurrences: "(19; 112)"
- Skips insights with insufficient data (N/A values)

### utils.py
Provides validation and helper functions for write-up generation.

## Testing

Run the validation test suite:
```bash
python3 test_validation.py
```

This tests write-up generation for 9 batters across 3 teams and validates:
- Word count limits
- Line count recommendations
- Number of insights generated
- Error handling

## Technical Details

### Statistical Methodology

**Outlier Detection**: Uses z-score approach
```
z-score = (value - mean) / standard_deviation
Threshold: |z-score| > 1.5
```

- Calculated across all batters for each length/line combination
- Positive z-scores indicate strengths
- Negative z-scores indicate weaknesses

### Wagon Zone Mapping

Based on the cricket field diagram provided:
- Zone 1: Fine Leg
- Zone 2: Square Leg
- Zone 3: Mid Wicket
- Zone 4: Mid On (RHB) / Mid Off (LHB)
- Zone 5: Mid Off (RHB) / Mid On (LHB)
- Zone 6: Covers
- Zone 7: Point
- Zone 8: Third Man

### Data Processing

1. **Length Categories**: full, good_length, short, short_of_a_good_length, yorker, full_toss
2. **Line Categories**: down_leg, on_the_stumps, outside_offstump, wide_outside_offstump, wide_down_leg
3. **Shot Types**: 30+ shot types tracked separately for pace and spin bowling
4. **Boundary Zones**: 8 wagon zones with percentage distribution
5. **Dismissal Zones**: 8 wagon zones for caught dismissals

## Write-up Format Example

```
Virat Kohli (RHB)

Length: Strong vs full (61 avg; 175 SR) and good length (44; 112). 
Vulnerable to short balls (22; 225). Target: yorkers and short of good length.

Line: Excels outside off (65; 159) but struggles on the stumps (17; 147). 
Bowl: tight line on stumps.

Shots: vs Pace: cut (24%), pull (20%); vs Spin: flick (30%), sweep (25%).

Boundaries: Covers (40%), midwicket (20%), third man (15%). 
Protect covers boundary.

Dismissals: Square leg (20%), point (15%), fine leg (10%). 
Set catchers at square leg.

Stats: 5 insights | 142 words | 9 lines
```

## Requirements

- streamlit >= 1.28.0
- pandas >= 2.0.0
- numpy >= 1.24.0

## Data Coverage

- **IPL Seasons**: 2021-2023
- **Teams**: 10 IPL teams
- **Players**: 70+ players (top 7 per team)
- **Batters in Database**: 262 total

## Validation Results

Test suite results:
- Total batters tested: 9
- Valid write-ups: 9
- Success rate: 100%
- All constraints satisfied (word count, line count, formatting)

## Known Limitations

1. **Data Availability**: Some players may have limited data for certain metrics (N/A values)
2. **Outlier Detection**: Requires sufficient sample size for accurate z-score calculation
3. **Batting Hand**: Inferred from cricket knowledge, not always from data source
4. **Export Feature**: Currently not implemented (coming soon)

## Future Enhancements

- PDF/Image export functionality
- Comparative analysis between multiple batters
- Historical performance trends
- Opposition-specific insights (e.g., vs particular bowlers)
- Custom metric thresholds for outlier detection
- Match-specific filtering

## Support

For issues or questions, please refer to the validation test results or check the console output for error messages.

## License

This project is intended for cricket analysis and tactical preparation purposes.

## Credits

Data source: IPL statistics 2021-2023
Developed using Streamlit, Pandas, and NumPy
