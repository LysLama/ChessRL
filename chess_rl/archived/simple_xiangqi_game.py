"""
Simplified demo for multiple board game types
"""

import argparse
from game.simple_xiangqi_board import SimpleXiangqiBoard


def main():
    """Run a simplified game demonstration."""
    parser = argparse.ArgumentParser(description="Simple Xiangqi Demo")
    parser.add_argument(
        "--moves", type=int, default=5,
        help="Number of moves to play (for each side)"
    )
    args = parser.parse_args()
    
    print("=== Simple Xiangqi Demo ===")
    
    try:
        # Create board
        board = SimpleXiangqiBoard()
        
        # Play moves
        move_count = 0
        done = False
        
        # Print initial board state
        print(f"Initial state: {board.get_state_hash()}")
        
        while move_count < args.moves * 2 and not done:
            # Get legal moves
            legal_moves = board.get_legal_moves()
            
            if not legal_moves:
                print("Game over: No legal moves")
                break
            
            # Choose first legal move
            move = legal_moves[0]
            
            # Print the move
            print(f"Move {move_count + 1}: {move}")
            
            # Apply move
            reward, done = board.make_move(move)
            
            # Print board state after move
            print(f"State after move: {board.get_state_hash()}")
            print(f"Reward: {reward}, Done: {done}")
            print()
            
            move_count += 1
        
        # Game result
        if done:
            result = board.get_result()
            print(f"Game over! Result: {result}")
        else:
            print(f"Game stopped after {move_count} moves")
    
    except ImportError:
        print("Error: pyffish library is required")
        print("Install it with: pip install pyffish")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()