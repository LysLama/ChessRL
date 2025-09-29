"""
Test script for pyffish API - focusing on move application
"""

try:
    import pyffish as sf
    has_pyffish = True
except ImportError:
    has_pyffish = False
    print("pyffish not installed. Please install with: pip install pyffish")


def test_make_moves():
    """Test making moves with pyffish."""
    if not has_pyffish:
        return
    
    print("=== Testing pyffish move application ===")
    
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
    try:
        new_fen = sf.get_fen(variant, init_fen, [first_move])
        print(f"New FEN: {new_fen}")
        print("Move application successful!")
        
        # Try to get legal moves from new position
        try:
            new_moves = sf.legal_moves(variant, new_fen, [])
            print(f"Legal moves after {first_move}: {len(new_moves)}")
            print(f"Sample moves: {new_moves[:5]}")
            
            # Try a second move
            if new_moves:
                second_move = new_moves[0]
                print(f"\nTrying to apply second move: {second_move}")
                try:
                    # Method 1: Pass all moves in history
                    newer_fen1 = sf.get_fen(variant, init_fen, [first_move, second_move])
                    print(f"New FEN (with full history): {newer_fen1}")
                    
                    # Method 2: Pass only the new move with new position
                    newer_fen2 = sf.get_fen(variant, new_fen, [second_move])
                    print(f"New FEN (from current position): {newer_fen2}")
                    
                    # Compare results
                    print(f"Results match: {newer_fen1 == newer_fen2}")
                except Exception as e:
                    print(f"Error making second move: {e}")
        except Exception as e:
            print(f"Error getting legal moves after first move: {e}")
    except Exception as e:
        print(f"Error making first move: {e}")
    
    print("\n=== Testing complete ===")


if __name__ == "__main__":
    test_make_moves()