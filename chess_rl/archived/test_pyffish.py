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
    # Tham số thứ 3 phải là list, không phải string
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
    
    # Get legal moves from new position - tham số thứ 3 phải là list
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
    
    # Try to get a board representation
    try:
        # Get the board FEN (piece positions)
        board_repr = sf.board_fen("xiangqi", new_fen, [])
        print("\nBoard FEN (just piece positions):")
        print(board_repr)
        
        # Try to get a visual representation
        try:
            visual_repr = sf.get_san_moves("xiangqi", init_fen, [move])
            print("\nSAN notation for moves:")
            print(visual_repr)
        except Exception as e:
            print(f"\nCouldn't get SAN notation: {e}")
    except Exception as e:
        print(f"\nCouldn't get board visual: {e}")
    
    # Check additional functions
    print("\nAdditional functions:")
    
    try:
        # Get legal moves for new position
        new_legal_moves = sf.legal_moves("xiangqi", new_fen, [])
        
        if new_legal_moves:
            # Check if a move is legal
            check_move = new_legal_moves[0]
            is_legal = sf.is_legal("xiangqi", new_fen, [], check_move)
            print(f"Is move {check_move} legal: {is_legal}")
            
            # Try other API functions if available
            try:
                # Check nếu nước đi là hợp lệ để người còn lại đi tiếp
                if new_legal_moves:
                    # Thử nước đi thứ hai
                    second_move = new_legal_moves[0]
                    next_fen = sf.get_fen("xiangqi", new_fen, [second_move])
                    print(f"After second move {second_move}, new FEN:")
                    print(next_fen)
            except Exception as e:
                print(f"Error making second move: {e}")
            
            # Try to get visual representation if available
            try:
                # Generate SVG if available
                svg = sf.board_svg("xiangqi", new_fen, [], 8)
                print("SVG generation successful")
                with open("xiangqi_board.svg", "w") as f:
                    f.write(svg)
                print("SVG saved to xiangqi_board.svg")
            except Exception as e:
                print(f"SVG generation not available: {e}")
        
    except Exception as e:
        print(f"Error testing additional functions: {e}")
    
    print("\n=== Pyffish testing completed ===")

if __name__ == "__main__":
    test_pyffish_xiangqi()