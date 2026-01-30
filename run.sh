#!/bin/bash

# Run script for Cricket Tactical Write-ups Application

echo "🏏 Starting Cricket Tactical Write-ups Application..."
echo ""

# Check if required files exist
if [ ! -f "Batting_data_IPL__2123.csv" ]; then
    echo "❌ Error: Batting_data_IPL__2123.csv not found!"
    exit 1
fi

if [ ! -f "IPL_top7_run_scorers_by_team_2021_2023.csv" ]; then
    echo "❌ Error: IPL_top7_run_scorers_by_team_2021_2023.csv not found!"
    exit 1
fi

echo "✓ Data files found"
echo ""

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✓ Dependencies ready"
echo ""
echo "🚀 Launching application..."
echo ""

# Run streamlit
streamlit run app.py
