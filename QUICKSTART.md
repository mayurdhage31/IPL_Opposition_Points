# Quick Start Guide

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

**Option A - Using the run script (recommended):**
```bash
./run.sh
```

**Option B - Direct command:**
```bash
streamlit run app.py
```

### Step 3: Use the Application

1. Your browser will automatically open to `http://localhost:8501`
2. Select an opposition team from the dropdown (e.g., "Mumbai Indians")
3. All top 7 players are pre-selected - deselect any if needed
4. Click through the player tabs to view tactical write-ups

## 📊 What You'll See

Each write-up contains up to 5 insights:

1. **Length Performance**: Strong/weak against different ball lengths
2. **Line Performance**: Strong/weak against different ball lines  
3. **Shot Selection**: Preferred shots vs pace and spin
4. **Boundary Zones**: Where they score boundaries (with fielding advice)
5. **Dismissal Zones**: Where they get caught (with fielding advice)

## 💡 Example Usage

**Scenario**: You're playing against Mumbai Indians tomorrow.

1. Select "Mumbai Indians" from dropdown
2. View Suryakumar Yadav's write-up:
   - **Strong vs short (60 avg; 286 SR)** → Avoid short balls
   - **Flick (19%) vs pace** → Watch for flick shots
   - **Boundaries: Mid Wicket (17%)** → Protect mid wicket

3. Use these insights to:
   - Plan bowling strategy (lengths/lines to bowl)
   - Set field placements (protect scoring zones)
   - Position catchers (high dismissal zones)

## 🎯 Key Features

- ✅ All 10 IPL teams available
- ✅ Top 7 run-scorers per team (70 players total)
- ✅ Statistical outlier detection for key insights
- ✅ Mobile-responsive design
- ✅ LHB/RHB zone mapping
- ✅ Direct, actionable advice (no fluff)

## 🔧 Troubleshooting

**Issue**: "Module not found" error
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: CSV file not found
- **Solution**: Ensure both CSV files are in the same directory as app.py

**Issue**: No insights showing for a player
- **Solution**: Limited data available for that player - this is expected

## 📝 Data Requirements

The application requires two CSV files (already included):
- `Batting_data_IPL__2123.csv` - Batting statistics
- `IPL_top7_run_scorers_by_team_2021_2023.csv` - Team rosters

## 🧪 Testing

Validate the application:
```bash
python3 test_validation.py
```

Expected output: 100% success rate with all write-ups validated.

## 📱 Viewing on Mobile

The application is fully responsive. Simply:
1. Start the app on your computer
2. Note the local IP (shown in terminal)
3. Access from phone: `http://YOUR_IP:8501`

## ⚡ Performance

- Data loads instantly (cached)
- Write-ups generate in < 1 second
- Supports 70+ players across 10 teams

## 🎓 Understanding the Metrics

**First metric mention**: "44 avg; 156 SR"
- **avg** = Batting average (runs per dismissal)
- **SR** = Strike rate (runs per 100 balls)

**Subsequent mentions**: "(19; 112)"
- First number = average
- Second number = strike rate

**Percentages**: "(24%)" = frequency of that shot/zone

## 📚 Learn More

For detailed documentation, see [README.md](README.md)

---

**Ready to analyze your opposition? Run the app now!**

```bash
streamlit run app.py
```
