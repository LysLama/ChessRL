"""
Comprehensive test script for pyffish API - exploring Xiangqi capabilities and move applications
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
        print("\nXiangqi is NOT supported")
        return
    
    # Get start FEN for xiangqi
    variant = "xiangqi"
    start_fen = sf.start_fen(variant)
    print(f"\nStart FEN for {variant}: {start_fen}")
    
    # Get legal moves from starting position
    legal_moves = sf.legal_moves(variant, start_fen, [])
    print(f"\nNumber of legal moves from starting position: {len(legal_moves)}")
    print(f"First 10 legal moves: {legal_moves[:10]}")
    
    # Test FEN validation
    print("\nTesting FEN validation...")
    is_valid = sf.validate_fen(start_fen, variant)
    print(f"Is start FEN valid? {is_valid}")
    
    # Test invalid FEN
    invalid_fen = "invalid fen"
    is_valid = sf.validate_fen(invalid_fen, variant)
    print(f"Is '{invalid_fen}' valid? {is_valid}")
    
    # Test board visualization if available
    print("\nBoard representation:")
    if hasattr(sf, 'get_fen_board'):
        try:
            board = sf.get_fen_board(variant, start_fen)
            print(board)
        except Exception as e:
            print(f"Error using get_fen_board: {e}")
    else:
        print("Function get_fen_board not available in this pyffish version")


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
    if moves:
        move = moves[0]
        print(f"\nMaking move: {move}")
        
        # Apply the move using pyffish
        new_fen = sf.get_fen(variant, init_fen, [move])
        print(f"New FEN: {new_fen}")
        
        # Get legal moves from new position
        new_moves = sf.legal_moves(variant, new_fen, [])
        print(f"Legal moves after {move}: {len(new_moves)}")
        print(f"Sample new moves: {new_moves[:5]}")
        
        # Test move sequence
        print("\nTesting move sequence...")
        if new_moves:
            move_sequence = [move, new_moves[0]]
            resulting_fen = sf.get_fen(variant, init_fen, move_sequence)
            print(f"After moves {move_sequence}: {resulting_fen}")
            
            # Check if the position is a game end state
            if hasattr(sf, 'is_game_end'):
                is_game_end = sf.is_game_end(variant, init_fen, move_sequence)
                print(f"Is game end? {is_game_end}")
            else:
                print("Function is_game_end not available in this pyffish version")


def test_additional_functionality():
    """Test additional pyffish functionality specific to Xiangqi."""
    if not has_pyffish:
        return
    
    print("\n=== Testing additional pyffish functionality ===")
    
    variant = "xiangqi"
    init_fen = sf.start_fen(variant)
    
    # Test move representation if available
    if hasattr(sf, "get_san"):
        moves = sf.legal_moves(variant, init_fen, [])
        if moves:
            move = moves[0]
            try:
                # Try different forms since the API might differ between versions
                try:
                    san = sf.get_san(variant, init_fen, "", move)
                except:
                    san = sf.get_san(variant, init_fen, move)
                print(f"\nUCI move: {move}, SAN representation: {san}")
            except Exception as e:
                print(f"\nError getting SAN representation: {e}")
    else:
        print("\nFunction get_san not available in this pyffish version")
    
    # Test checking detection if available
    if hasattr(sf, "gives_check"):
        moves = sf.legal_moves(variant, init_fen, [])
        for move in moves[:5]:  # Check first 5 moves
            gives_check = sf.gives_check(variant, init_fen, [move])
            print(f"Move {move} gives check: {gives_check}")
    else:
        print("\nFunction gives_check not available in this pyffish version")


if __name__ == "__main__":
    print("Running pyffish tests...")
    test_pyffish_xiangqi()
    test_make_moves()
    test_additional_functionality()
    print("Tests complete!")