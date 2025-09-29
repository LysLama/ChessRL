"""
Test script for pyffish API - exploring Xiangqi capabilities
"""

try:
    import pyffish as sf
    has_pyffish = True
except ImportError:
    has_pyffish = False
    print("pyffish not installed. Please install with: pip install pyffish")

def test_pyffish_xiangqi():
    """Test basic pyffish functionality with Xiangqi."""
    if not has_pyffish:
        return
    
    print("=== Testing pyffish with Xiangqi ===")
    
    # Initialize pyffish
    print("Pyffish version:", sf.version())
    
    # List supported variants
    print("\nSupported variants:")
    variants = sf.variants()
    print(variants)
    
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
    print(legal_moves)
    
    # Make a move and get resulting FEN
    if legal_moves:
        move = "h3h10" if "h3h10" in legal_moves else legal_moves[0]
        # Sử dụng list cho moves history
        new_fen = sf.get_fen("xiangqi", init_fen, [move])
        print(f"\nAfter move {move}, new FEN:")
        print(new_fen)
    
    # Get legal moves from new position
    legal_moves = sf.legal_moves("xiangqi", new_fen, [])
    print(f"\nLegal moves after {move} ({len(legal_moves)}):")
    print(legal_moves)
    
    # Check game result
    try:
        # Sử dụng sf.game_result thay vì is_game_over
        result = sf.game_result("xiangqi", new_fen, [])
        print(f"\nGame result: {result}") # 1-0, 0-1, or 1/2-1/2 if game is over, * if not
        print(f"Is game over: {result != '*'}")
    except Exception as e:
        print(f"\nError checking game result: {e}")
    
    # Try to get SAN notation for moves
    try:
        san_moves = sf.get_san_moves("xiangqi", init_fen, [move])
        print("\nSAN notation for the move:")
        print(san_moves)
    except Exception as e:
        print(f"\nCouldn't get SAN notation: {e}")
    
    # Check additional functions
    print("\nAdditional functions:")
    
    try:
        # Get legal moves for new position
        new_legal_moves = sf.legal_moves("xiangqi", new_fen, [])
        
        if new_legal_moves:
            # Make a second move
            second_move = new_legal_moves[0]
            next_fen = sf.get_fen("xiangqi", new_fen, [second_move])
            print(f"After second move {second_move}, new FEN:")
            print(next_fen)
            
            # Check if the move gives check
            try:
                gives_check = sf.gives_check("xiangqi", new_fen, [second_move])
                print(f"Move {second_move} gives check: {gives_check}")
            except Exception as e:
                print(f"Error checking if move gives check: {e}")
            
            # Check if the move is a capture
            try:
                is_capture = sf.is_capture("xiangqi", new_fen, second_move)
                print(f"Move {second_move} is a capture: {is_capture}")
            except Exception as e:
                print(f"Error checking if move is capture: {e}")
                
            # Check for insufficient material
            try:
                insufficient = sf.has_insufficient_material("xiangqi", new_fen, [])
                print(f"Position has insufficient material: {insufficient}")
            except Exception as e:
                print(f"Error checking insufficient material: {e}")
                
            # Check for immediate game end
            try:
                immediate_end = sf.is_immediate_game_end("xiangqi", new_fen, [])
                print(f"Position has immediate game end: {immediate_end}")
            except Exception as e:
                print(f"Error checking immediate game end: {e}")
                
            # Check for optional game end
            try:
                optional_end = sf.is_optional_game_end("xiangqi", new_fen, [])
                print(f"Position has optional game end: {optional_end}")
            except Exception as e:
                print(f"Error checking optional game end: {e}")
    
    except Exception as e:
        print(f"Error testing additional functions: {e}")
    
    print("\n=== Pyffish testing completed ===")

if __name__ == "__main__":
    test_pyffish_xiangqi()