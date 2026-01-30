"""
Zone Mapper Module
Maps wagon zone numbers to field position names with LHB/RHB lateral flipping.
"""

from typing import Dict


# Zone mapping for Right-Handed Batters (RHB)
RHB_ZONES = {
    1: "Fine Leg",
    2: "Square Leg",
    3: "Mid Wicket",
    4: "Mid On",
    5: "Mid Off",
    6: "Covers",
    7: "Point",
    8: "Third Man"
}

# Zone mapping for Left-Handed Batters (LHB)
# Laterally flipped - zones 4,5 and 6 are swapped
LHB_ZONES = {
    1: "Fine Leg",
    2: "Square Leg",
    3: "Mid Wicket",
    4: "Mid Off",      # Flipped: Mid Off for LHB (Mid On for RHB)
    5: "Mid On",       # Flipped: Mid On for LHB (Mid Off for RHB)
    6: "Covers",       # Same for both
    7: "Point",        # Same for both
    8: "Third Man"     # Same for both
}


def get_zone_name(zone_number: int, batting_hand: str) -> str:
    """
    Get field position name for a wagon zone number based on batting hand.
    
    Args:
        zone_number: Wagon zone number (1-8)
        batting_hand: 'LHB' or 'RHB'
        
    Returns:
        Field position name
    """
    if batting_hand == 'LHB':
        return LHB_ZONES.get(zone_number, f"Zone {zone_number}")
    else:
        return RHB_ZONES.get(zone_number, f"Zone {zone_number}")


def get_zone_mapping(batting_hand: str) -> Dict[int, str]:
    """
    Get complete zone mapping dictionary for a batting hand.
    
    Args:
        batting_hand: 'LHB' or 'RHB'
        
    Returns:
        Dictionary mapping zone numbers to field positions
    """
    if batting_hand == 'LHB':
        return LHB_ZONES.copy()
    else:
        return RHB_ZONES.copy()


if __name__ == "__main__":
    # Test zone mapping
    print("RHB Zone Mapping:")
    for zone in range(1, 9):
        print(f"  Zone {zone}: {get_zone_name(zone, 'RHB')}")
    
    print("\nLHB Zone Mapping:")
    for zone in range(1, 9):
        print(f"  Zone {zone}: {get_zone_name(zone, 'LHB')}")
    
    print("\nDifferences (LHB vs RHB):")
    for zone in range(1, 9):
        rhb_name = get_zone_name(zone, 'RHB')
        lhb_name = get_zone_name(zone, 'LHB')
        if rhb_name != lhb_name:
            print(f"  Zone {zone}: RHB={rhb_name}, LHB={lhb_name}")
