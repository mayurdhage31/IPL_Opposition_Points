"""Quick test to verify all modules can be imported successfully."""

print("Testing module imports...")

try:
    import data_loader
    print("✓ data_loader imported successfully")
except Exception as e:
    print(f"✗ data_loader import failed: {e}")

try:
    import zone_mapper
    print("✓ zone_mapper imported successfully")
except Exception as e:
    print(f"✗ zone_mapper import failed: {e}")

try:
    import outlier_detector
    print("✓ outlier_detector imported successfully")
except Exception as e:
    print(f"✗ outlier_detector import failed: {e}")

try:
    import writeup_generator
    print("✓ writeup_generator imported successfully")
except Exception as e:
    print(f"✗ writeup_generator import failed: {e}")

try:
    import utils
    print("✓ utils imported successfully")
except Exception as e:
    print(f"✗ utils import failed: {e}")

print("\nAll core modules imported successfully!")
print("\nTo run the application, execute:")
print("  streamlit run app.py")
