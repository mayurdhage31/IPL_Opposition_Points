#!/usr/bin/env python3
"""
Standalone demo script for the Cricket Wagon Wheel visualization.

Usage:
    python demo_wagon_wheel.py                    # Interactive mode
    python demo_wagon_wheel.py "Aaron Finch"      # Specific batter
    python demo_wagon_wheel.py --list             # List all batters
    python demo_wagon_wheel.py --validate         # Validate zone positions
"""

import sys
import pandas as pd
from wagon_wheel import plot_wagon_wheel, validate_zone_positions

# Data file path
CSV_FILE = 'batter_fours_sixes_by_zone_wide_2021_2023.csv'


def list_batters(df: pd.DataFrame, limit: int = 20):
    """List available batters with their total boundaries."""
    print(f"\n{'='*70}")
    print(f"  Available Batters ({len(df)} total)")
    print(f"{'='*70}")
    print(f"{'No.':<5} {'Batter Name':<30} {'Fours':<8} {'Sixes':<8} {'Total':<8}")
    print(f"{'-'*70}")
    
    # Calculate total boundaries for each batter
    batter_stats = []
    for idx, row in df.iterrows():
        total_fours = sum([row.get(f'fours_wagonZone{z}', 0) for z in range(1, 9)])
        total_sixes = sum([row.get(f'sixes_wagonZone{z}', 0) for z in range(1, 9)])
        total = total_fours + total_sixes
        batter_stats.append({
            'name': row['bat'],
            'fours': int(total_fours),
            'sixes': int(total_sixes),
            'total': int(total)
        })
    
    # Sort by total boundaries
    batter_stats.sort(key=lambda x: x['total'], reverse=True)
    
    # Display top batters
    for idx, stats in enumerate(batter_stats[:limit], 1):
        print(f"{idx:<5} {stats['name']:<30} {stats['fours']:<8} {stats['sixes']:<8} {stats['total']:<8}")
    
    if len(batter_stats) > limit:
        print(f"{'-'*70}")
        print(f"... and {len(batter_stats) - limit} more batters")
    
    print(f"{'='*70}\n")


def interactive_mode(df: pd.DataFrame):
    """Interactive mode to select and visualize a batter."""
    print("\n" + "="*70)
    print("  Cricket Wagon Wheel - Interactive Mode")
    print("="*70)
    
    # Show top 10 batters
    list_batters(df, limit=10)
    
    print("\nOptions:")
    print("  1. Enter batter name to generate wagon wheel")
    print("  2. Type 'list' to see all batters")
    print("  3. Type 'validate' to check zone positions")
    print("  4. Type 'quit' to exit")
    
    while True:
        choice = input("\nYour choice: ").strip()
        
        if choice.lower() in ['quit', 'exit', 'q']:
            print("\nGoodbye! 🏏")
            break
        
        elif choice.lower() == 'list':
            list_batters(df, limit=50)
        
        elif choice.lower() == 'validate':
            print("\nGenerating zone position validation chart...")
            fig = validate_zone_positions()
            fig.write_html('wagon_wheel_validation.html')
            print("✓ Validation chart saved to: wagon_wheel_validation.html")
            print("  Open this file in your browser to verify zone positions.")
        
        elif choice:
            # Try to find the batter
            batter_match = df[df['bat'].str.lower() == choice.lower()]
            
            if batter_match.empty:
                # Try partial match
                batter_match = df[df['bat'].str.contains(choice, case=False, na=False)]
                
                if batter_match.empty:
                    print(f"\n✗ No batter found matching: '{choice}'")
                    print("  Tip: Try typing 'list' to see available batters")
                    continue
                
                elif len(batter_match) > 1:
                    print(f"\n⚠️  Multiple batters found matching '{choice}':")
                    for idx, bat in enumerate(batter_match['bat'], 1):
                        print(f"  {idx}. {bat}")
                    print("\nPlease enter the exact name from the list above.")
                    continue
            
            batter_name = batter_match.iloc[0]['bat']
            print(f"\n✓ Generating wagon wheel for: {batter_name}")
            
            try:
                fig = plot_wagon_wheel(df, batter_name)
                output_file = f"wagon_wheel_{batter_name.replace(' ', '_')}.html"
                fig.write_html(output_file)
                print(f"✓ Wagon wheel saved to: {output_file}")
                print(f"  Open this file in your browser to view the visualization.")
                
                # Show stats
                row = batter_match.iloc[0]
                total_fours = sum([row.get(f'fours_wagonZone{z}', 0) for z in range(1, 9)])
                total_sixes = sum([row.get(f'sixes_wagonZone{z}', 0) for z in range(1, 9)])
                print(f"\n  Stats: {int(total_fours)} fours, {int(total_sixes)} sixes")
                
            except Exception as e:
                print(f"\n✗ Error generating wagon wheel: {e}")


def main():
    """Main entry point."""
    # Load data
    try:
        df = pd.read_csv(CSV_FILE)
        print(f"✓ Loaded data: {len(df)} batters from {CSV_FILE}")
    except FileNotFoundError:
        print(f"\n✗ Error: Could not find '{CSV_FILE}'")
        print(f"  Please make sure the CSV file is in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error loading data: {e}")
        sys.exit(1)
    
    # Parse command line arguments
    if len(sys.argv) == 1:
        # No arguments - interactive mode
        interactive_mode(df)
    
    elif sys.argv[1] in ['--list', '-l']:
        # List all batters
        list_batters(df, limit=50)
    
    elif sys.argv[1] in ['--validate', '-v']:
        # Validate zone positions
        print("\nGenerating zone position validation chart...")
        fig = validate_zone_positions()
        fig.write_html('wagon_wheel_validation.html')
        print("✓ Validation chart saved to: wagon_wheel_validation.html")
    
    elif sys.argv[1] in ['--help', '-h']:
        # Show help
        print(__doc__)
    
    else:
        # Treat as batter name
        batter_name = ' '.join(sys.argv[1:])
        
        if batter_name not in df['bat'].values:
            print(f"\n✗ Batter not found: '{batter_name}'")
            print("\nDid you mean one of these?")
            similar = df[df['bat'].str.contains(batter_name.split()[0], case=False, na=False)]
            for bat in similar['bat'].head(5):
                print(f"  - {bat}")
            print("\nTip: Use quotes for names with spaces, e.g., python demo_wagon_wheel.py \"Aaron Finch\"")
            sys.exit(1)
        
        print(f"\n✓ Generating wagon wheel for: {batter_name}")
        fig = plot_wagon_wheel(df, batter_name)
        output_file = f"wagon_wheel_{batter_name.replace(' ', '_')}.html"
        fig.write_html(output_file)
        print(f"✓ Wagon wheel saved to: {output_file}")
        
        # Show stats
        row = df[df['bat'] == batter_name].iloc[0]
        total_fours = sum([row.get(f'fours_wagonZone{z}', 0) for z in range(1, 9)])
        total_sixes = sum([row.get(f'sixes_wagonZone{z}', 0) for z in range(1, 9)])
        print(f"  Stats: {int(total_fours)} fours, {int(total_sixes)} sixes\n")


if __name__ == "__main__":
    main()
