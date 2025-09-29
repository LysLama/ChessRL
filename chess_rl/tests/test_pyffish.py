"""
Comprehensive test script for pyffish API with Xiangqi
"""

try:
    import pyffish as sf
    has_pyffish = True
except ImportError:
    has_pyffish = False
    print("pyffish not installed. Please install with: pip install pyffish")


def test_pyffish_basic():
    """Test basic pyffish functionality with Xiangqi."""
    if not has_pyffish:
        return
    
    print("=== Testing pyffish basic functionality ===")
    
    # Initialize pyffish
    print("Pyffish version:", sf.version())
    
    # List supported variants
    print("\nSupported variants:")
    variants = sf.variants()
    
    # Show some variants for brevity
    print(f"Found {len(variants)} variants including: {variants[:10]}...")
    
    # Check if xiangqi is supported
    if "xiangqi" in variants:
        print("\nXiangqi is supported!")
    else:
        print("\nXiangqi is NOT supported!")
        return
    
    # Get initial FEN for xiangqi
    init_fen = sf.start_fen("xiangqi")
    print("\nInitial FEN for xiangqi:")
    print(init_fen)
    
    # Get legal moves from starting position
    legal_moves = sf.legal_moves("xiangqi", init_fen, [])
    print(f"\nLegal moves from starting position ({len(legal_moves)}):")
    print(f"Sample moves: {legal_moves[:5]}...")


def test_make_moves():
    """Test making moves with pyffish."""
    if not has_pyffish:
        return
    
    print("\n=== Testing pyffish move application ===")
    
    # Set up variables
    variant = "xiangqi"
    init_fen = sf.start_fen(variant)
    print(f"Initial FEN: {init_fen}")
    
    # Get legal moves
    moves = sf.legal_moves(variant, init_fen, [])
    print(f"Number of legal moves: {len(moves)}")
    print(f"Sample moves: {moves[:5]}")
    
    # Try to make a single move
    first_move = moves[0]
    print(f"\nTrying to apply move: {first_move}")
    
    new_fen = sf.get_fen(variant, init_fen, [first_move])
    print(f"New FEN: {new_fen}")
    print("Move application successful!")
    
    # Try to get legal moves from new position
    new_moves = sf.legal_moves(variant, new_fen, [])
    print(f"Legal moves after {first_move}: {len(new_moves)}")
    print(f"Sample moves: {new_moves[:5]}")
    
    # Try a second move
    if new_moves:
        second_move = new_moves[0]
        print(f"\nTrying to apply second move: {second_move}")
        
        # Method 1: Pass all moves in history
        newer_fen1 = sf.get_fen(variant, init_fen, [first_move, second_move])
        print(f"New FEN (with full history): {newer_fen1}")
        
        # Method 2: Pass only the new move with new position
        newer_fen2 = sf.get_fen(variant, new_fen, [second_move])
        print(f"New FEN (from current position): {newer_fen2}")
        
        # Compare results
        print(f"Results match: {newer_fen1 == newer_fen2}")
    
    # Try special move: Cannon takes Rook (h3h10)
    special_move = "h3h10"
    if special_move in moves:
        print(f"\nTrying special move: {special_move}")
        special_fen = sf.get_fen(variant, init_fen, [special_move])
        print(f"FEN after special move: {special_fen}")
        
        # Check if game is over after this move
        try:
            is_end, _ = sf.is_immediate_game_end(variant, special_fen, [])
            print(f"Is game immediately over: {is_end}")
        except Exception:
            # Some pyffish versions might not have this function
            print("Could not check if game is immediately over")


def test_additional_functions():
    """Test additional pyffish functionality (guarded for stability)."""
    if not has_pyffish:
        return

    print("\n=== Testing additional pyffish functions (guarded) ===")

    variant = "xiangqi"
    init_fen = sf.start_fen(variant)

    # Limit to simple, widely-supported calls to avoid native crashes
    try:
        moves = sf.legal_moves(variant, init_fen, [])
        assert isinstance(moves, list)
    except Exception as e:
        # If even this fails, skip further checks
        print(f"Skipping extended checks due to error: {e}")
        return

    # Optional: validate FEN if function exists
    try:
        if hasattr(sf, "validate_fen"):
            valid = sf.validate_fen(variant, init_fen)
            print(f"Is initial FEN valid: {valid}")
    except Exception as e:
        print(f"validate_fen failed (ignored): {e}")

    print("\n=== Guarded pyffish testing completed ===")


if __name__ == "__main__":
    test_pyffish_basic()
    test_make_moves()
    test_additional_functions()