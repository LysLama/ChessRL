"""
Simple demo for testing the SimpleXiangqiBoard implementation
"""

from game.simple_xiangqi_board import SimpleXiangqiBoard


def simple_xiangqi_demo():
    """Demo for the simplified Xiangqi implementation."""
    print("\n=== Simple Xiangqi Demo ===")
    
    # Create a board
    board = SimpleXiangqiBoard()
    print(f"Initial FEN: {board.current_fen}")
    
    # Get legal moves
    legal_moves = board.get_legal_moves()
    print(f"Number of legal moves: {len(legal_moves)}")
    print(f"Sample moves: {legal_moves[:5]}")
    
    # Make a move
    if legal_moves:
        move = legal_moves[0]  # e.g., "a1a2"
        print(f"\nMaking move: {move}")
        reward, done = board.make_move(move)
        print(f"Reward: {reward}, Game over: {done}")
        
        # Check new position
        print(f"New FEN: {board.current_fen}")
        
        # Get new legal moves
        new_legal_moves = board.get_legal_moves()
        print(f"Number of legal moves after {move}: {len(new_legal_moves)}")
        print(f"Sample moves: {new_legal_moves[:5]}")
        
        # Make a second move
        if new_legal_moves:
            move2 = new_legal_moves[0]
            print(f"\nMaking second move: {move2}")
            reward, done = board.make_move(move2)
            print(f"Reward: {reward}, Game over: {done}")
            print(f"New FEN: {board.current_fen}")
    
    # Test special moves
    print("\nTesting special moves...")
    board.reset()
    
    # Try the special move h3h10 (Cannon takes Rook)
    special_move = "h3h10"
    if special_move in board.get_legal_moves():
        print(f"Making special move: {special_move}")
        reward, done = board.make_move(special_move)
        print(f"Reward: {reward}, Game over: {done}")
        print(f"New FEN: {board.current_fen}")
        
        # Get observation tensor
        obs = board.get_observation()
        print(f"Observation tensor shape: {obs.shape}")
    else:
        print(f"Special move {special_move} is not legal")
        
    print("\n=== Demo completed ===")


if __name__ == "__main__":
    try:
        import pyffish
        has_pyffish = True
    except ImportError:
        has_pyffish = False
        print("pyffish is not installed. Please install with: pip install pyffish")
    
    if has_pyffish:
        simple_xiangqi_demo()
    else:
        print("Skipping demo due to missing pyffish dependency.")