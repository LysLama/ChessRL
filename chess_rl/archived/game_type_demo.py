"""
Run a demo game between Chess and Xiangqi with pyffish
"""

import argparse
from game.game_factory import GameFactory


def main():
    """Entry point of the application."""
    parser = argparse.ArgumentParser(description="Xiangqi with pyffish Demo")
    parser.add_argument(
        "--game", type=str,
        choices=["chess", "xiangqi", "xiangqi_pyffish", "xiangqi_simple"],
        default="xiangqi_simple",
        help="Type of game to play (chess, xiangqi, xiangqi_pyffish, xiangqi_simple)"
    )
    parser.add_argument(
        "--moves", type=int, default=10,
        help="Number of moves to play (for each side)"
    )
    args = parser.parse_args()
    
    print(f"=== {args.game.upper()} Demo ===")
    
    try:
        # Create board based on game type
        board = GameFactory.create_board(args.game)
        
        # Use different API depending on the board type
        is_simple_xiangqi = args.game == "xiangqi_simple"
        
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
            
            # Choose first legal move (could be random, but keeping it simple)
            move = legal_moves[0]
            
            # Print the move
            print(f"Move {move_count + 1}: {move}")
            
            # Apply move - handle different API for SimpleXiangqiBoard
            if is_simple_xiangqi:
                # SimpleXiangqiBoard uses move_str directly
                reward, done = board.make_move(str(move))
            elif args.game == "xiangqi_pyffish":
                # For XiangqiPyffishBoard, the move is already a XiangqiPyffishMove object
                from game.xiangqi_pyffish_board import XiangqiPyffishMove
                if isinstance(move, XiangqiPyffishMove):
                    reward, done = board.apply_move(move)
                else:
                    # If it's not already the right type, convert it
                    reward, done = board.apply_move(XiangqiPyffishMove(str(move)))
            else:
                # For standard ChessBoard and XiangqiBoard
                reward, done = board.apply_move(move)
            
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
    
    except ImportError as e:
        if "pyffish" in str(e):
            print("Error: pyffish library is required for xiangqi_pyffish and xiangqi_simple")
            print("Install it with: pip install pyffish")
        else:
            print(f"Import error: {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()