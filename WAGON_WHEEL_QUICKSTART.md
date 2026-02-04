# Wagon Wheel Quick Start Guide

## 🚀 Get Started in 30 Seconds

### Option 1: Interactive Demo (Recommended)

```bash
python demo_wagon_wheel.py
```

Then type a batter name when prompted (e.g., `Virat Kohli`)

### Option 2: Direct Generation

```bash
# Generate wagon wheel for a specific batter
python demo_wagon_wheel.py "Shubman Gill"

# Open the generated HTML file
open wagon_wheel_Shubman_Gill.html  # Mac
# or
start wagon_wheel_Shubman_Gill.html  # Windows
# or
xdg-open wagon_wheel_Shubman_Gill.html  # Linux
```

### Option 3: Streamlit App

```bash
streamlit run app.py
```

1. Select a team from the sidebar
2. Click on a player's tab
3. Click **"📊 Show Visualizations"**
4. Scroll to **"Boundary Distribution by Zone"**

## 📊 What You'll See

- **Blue spokes** = Fours hit in each zone
- **Red spokes** = Sixes hit in each zone
- **Marker size** = Number of boundaries (bigger = more boundaries)
- **Hover** over markers to see exact counts

## 🎯 Zone Layout (Clockwise from Top)

```
        TOP
         |
    [Third Man]  [Fine Leg]
        \          /
 [Point] \        / [Square Leg]
          \      /
           \    /
    -------- X --------  (Batter)
           /    \
          /      \
 [Covers]/        \ [Mid Wicket]
        /          \
   [Mid Off]    [Mid On]
```

## 📋 Example Batters to Try

**High Boundary Scorers** (2021-2023 IPL):
- Shubman Gill (229 boundaries)
- Faf du Plessis (225 boundaries)
- Jos Buttler (201 boundaries)
- Virat Kohli (159 boundaries)
- Rohit Sharma (138 boundaries)

**Power Hitters** (Most Sixes):
- Jos Buttler (67 sixes)
- Glenn Maxwell (65 sixes)
- Faf du Plessis (64 sixes)
- KL Rahul (63 sixes)

**Boundary Machines** (Most Fours):
- Shubman Gill (176 fours)
- Faf du Plessis (161 fours)
- Shikhar Dhawan (144 fours)

## 🔍 Validation

Check that zone positions are correct:

```bash
python demo_wagon_wheel.py --validate
```

Open `wagon_wheel_validation.html` to verify:
- ✅ Fine Leg is top-right
- ✅ Third Man is top-left
- ✅ Square Leg is on the right
- ✅ Point is on the left
- ✅ Mid Off is at bottom

## 📝 Command Cheat Sheet

```bash
# List all batters
python demo_wagon_wheel.py --list

# Validate zone positions
python demo_wagon_wheel.py --validate

# Generate for specific batter
python demo_wagon_wheel.py "Aaron Finch"

# Interactive mode
python demo_wagon_wheel.py

# Help
python demo_wagon_wheel.py --help
```

## ❓ Troubleshooting

**"Batter not found"**
- Use exact spelling: `"Aaron Finch"` not `"aaron finch"`
- Use quotes for names with spaces
- Run `--list` to see available names

**"FileNotFoundError: batter_fours_sixes_by_zone_wide_2021_2023.csv"**
- Make sure you're in the project directory
- Check that the CSV file exists

**Can't see the wagon wheel in Streamlit**
- Click the **"📊 Show Visualizations"** button (top-right of player tab)
- Scroll down to the "Boundary Distribution by Zone" section

## 📖 Full Documentation

See `WAGON_WHEEL_DOCUMENTATION.md` for complete technical details.

---

**Ready to explore?** Try this now:

```bash
python demo_wagon_wheel.py "Virat Kohli"
```
