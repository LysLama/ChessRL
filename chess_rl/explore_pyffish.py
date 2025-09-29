"""
Test additional functions of pyffish API
"""

try:
    import pyffish as sf
    has_pyffish = True
except ImportError:
    has_pyffish = False
    print("pyffish not installed. Please install with: pip install pyffish")

def explore_pyffish_api():
    """Explore the full API of pyffish."""
    if not has_pyffish:
        return
    
    print("=== Exploring pyffish API ===")
    
    # Get all attributes of the module
    attrs = dir(sf)
    
    # Filter out private attributes
    public_attrs = [attr for attr in attrs if not attr.startswith('_')]
    
    print(f"\nFound {len(public_attrs)} public functions/attributes:")
    for attr in sorted(public_attrs):
        try:
            # Get docstring if available
            doc = getattr(sf, attr).__doc__
            print(f"- {attr}: {doc if doc else 'No documentation'}")
        except:
            print(f"- {attr}")
    
    print("\n=== API exploration completed ===")

if __name__ == "__main__":
    explore_pyffish_api()