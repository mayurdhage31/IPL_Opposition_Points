"""
Test Script for Write-up Validation
Tests write-up generation and validation for multiple batters.
"""

import data_loader
import writeup_generator
import utils


def test_writeups():
    """Test write-up generation for sample batters from different teams."""
    print("=" * 80)
    print("CRICKET TACTICAL WRITE-UPS VALIDATION TEST")
    print("=" * 80)
    
    # Load data
    print("\n1. Loading data...")
    batting_df, merged_df, teams = data_loader.load_all_data(
        'Batting_data_IPL__2123.csv',
        'IPL_top7_run_scorers_by_team_2021_2023.csv'
    )
    print(f"   ✓ Loaded {len(batting_df)} batters and {len(teams)} teams")
    
    # Test with 3 different teams
    test_teams = ['Mumbai Indians', 'Chennai Super Kings', 'Royal Challengers Bangalore']
    
    total_tested = 0
    valid_writeups = 0
    warnings_count = 0
    errors_count = 0
    
    for team in test_teams:
        print(f"\n{'=' * 80}")
        print(f"TEAM: {team}")
        print('=' * 80)
        
        team_players = merged_df[merged_df['team_bat'] == team].sort_values('team_runs_rank')
        
        # Test first 3 players from each team
        for idx, (_, player_row) in enumerate(team_players.head(3).iterrows()):
            total_tested += 1
            
            batter_name = player_row['bat']
            batting_hand = player_row['batting_hand']
            
            print(f"\n{idx + 1}. {batter_name} ({batting_hand})")
            print("-" * 80)
            
            try:
                # Generate write-up
                writeup = writeup_generator.generate_writeup(batting_df, player_row)
                
                # Validate
                validation = utils.validate_writeup(writeup)
                
                # Display write-up
                print(f"\n{writeup['writeup']}\n")
                
                # Display stats
                print(f"Stats: {writeup['num_insights']} insights | "
                      f"{writeup['word_count']} words | {writeup['line_count']} lines")
                
                # Display validation results
                if validation['valid']:
                    print("✓ VALIDATION: PASSED")
                    valid_writeups += 1
                else:
                    print("✗ VALIDATION: FAILED")
                    errors_count += len(validation['errors'])
                
                if validation['errors']:
                    for error in validation['errors']:
                        print(f"  ✗ ERROR: {error}")
                
                if validation['warnings']:
                    warnings_count += len(validation['warnings'])
                    for warning in validation['warnings']:
                        print(f"  ⚠ WARNING: {warning}")
                
            except Exception as e:
                print(f"✗ ERROR generating write-up: {str(e)}")
                errors_count += 1
    
    # Summary
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print('=' * 80)
    print(f"Total batters tested: {total_tested}")
    print(f"Valid write-ups: {valid_writeups}")
    print(f"Warnings: {warnings_count}")
    print(f"Errors: {errors_count}")
    print(f"Success rate: {(valid_writeups/total_tested)*100:.1f}%")
    print('=' * 80)


if __name__ == "__main__":
    test_writeups()
