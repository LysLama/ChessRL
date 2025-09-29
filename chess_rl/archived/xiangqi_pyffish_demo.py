"""
Demo script for comparing Chess and Xiangqi implementations with pyffish
"""

import pyffish as sf
from game.game_factory import GameFactory
from game.xiangqi_pyffish_board import XiangqiPyffishMove


def xiangqi_pyffish_demo():
    """Demo for Xiangqi board implementation using pyffish."""
    print("\n=== Pyffish Xiangqi Demo ===")
    
    # Use pyffish directly to avoid any issues with wrapper
    print("Testing direct pyffish API...")
    variant = "xiangqi"
    init_fen = sf.start_fen(variant)
    print(f"Initial FEN: {init_fen}")
    
    # Get legal moves
    moves = sf.legal_moves(variant, init_fen, [])
    print(f"Legal moves count: {len(moves)}")
    print(f"Sample moves: {moves[:5]}")
    
    # Make a move
    if moves:
        move = moves[0]
        print(f"\nApplying move: {move}")
        try:
            # Apply move directly with pyffish
            new_fen = sf.get_fen(variant, init_fen, [move])
            print(f"New FEN: {new_fen}")
            
            # Try to get new legal moves
            try:
                new_moves = sf.legal_moves(variant, new_fen, [])
                print(f"Legal moves after {move}: {len(new_moves)}")
                print(f"Sample moves: {new_moves[:5]}")
                
                # Try special move h3h10 (Cannon takes Rook)
                special_move = "h3h10"
                if special_move in moves:
                    print(f"\nTrying special move: {special_move}")
                    special_fen = sf.get_fen(variant, init_fen, [special_move])
                    print(f"FEN after special move: {special_fen}")
                    
                    # Create observation tensor from FEN
                    print("Creating observation tensor from FEN...")
                    board_part = special_fen.split(' ')[0]
                    ranks = board_part.split('/')
                    print(f"Board has {len(ranks)} ranks")
                    
            except Exception as e:
                print(f"Error getting legal moves after first move: {e}")
        except Exception as e:
            print(f"Error applying move: {e}")
    
    # Now try with the wrapper class
    print("\n\nNow trying XiangqiPyffishBoard wrapper...")
    try:
        from game.xiangqi_pyffish_board import XiangqiPyffishBoard, XiangqiPyffishMove
        xiangqi_board = XiangqiPyffishBoard()
        
        print(f"Initial FEN: {xiangqi_board.current_fen}")
        print(f"Move history: {xiangqi_board.move_history}")
        
        # Get legal moves without using get_legal_moves method
        raw_moves = sf.legal_moves(variant, xiangqi_board.current_fen, [])
        print(f"Raw legal moves: {len(raw_moves)}")
        print(f"Sample moves: {raw_moves[:5]}")
        
        # Try making a move with raw API
        if raw_moves:
            raw_move = raw_moves[0]
            print(f"\nApplying raw move: {raw_move}")
            
            # Apply move directly
            xiangqi_board.move_history.append(raw_move)
            xiangqi_board.current_fen = sf.get_fen(variant, xiangqi_board.current_fen, [raw_move])
            
            print(f"New FEN: {xiangqi_board.current_fen}")
            print(f"Move history: {xiangqi_board.move_history}")
            
            # Try getting new moves
            try:
                new_raw_moves = sf.legal_moves(variant, xiangqi_board.current_fen, [])
                print(f"New raw legal moves: {len(new_raw_moves)}")
                print(f"Sample moves: {new_raw_moves[:5]}")
            except Exception as e:
                print(f"Error getting new legal moves: {e}")
    except Exception as e:
        print(f"Error with XiangqiPyffishBoard: {e}")
        

def compare_xiangqi_implementations():
    """Compare the two Xiangqi implementations."""
    print("\n=== Comparing Xiangqi Implementations ===")
    
    print("\n1. Using pyffish directly:")
    variant = "xiangqi"
    init_fen = sf.start_fen(variant)
    print(f"Initial FEN: {init_fen}")
    moves = sf.legal_moves(variant, init_fen, [])
    print(f"Legal moves count: {len(moves)}")
    print(f"Sample moves: {moves[:5]}")
    
    print("\n2. Using XiangqiPyffishBoard:")
    from game.xiangqi_pyffish_board import XiangqiPyffishBoard
    xiangqi_board = XiangqiPyffishBoard()
    legal_moves = xiangqi_board.get_legal_moves()
    print(f"Legal moves count: {len(legal_moves)}")
    print(f"Sample moves: {[str(move) for move in legal_moves[:5]]}")


def main():
    """Main entry point."""
    try:
        # Check if pyffish is available
        import pyffish
        has_pyffish = True
    except ImportError:
        has_pyffish = False
        print("pyffish not installed. Please install with: pip install pyffish")
    
    print("=== Xiangqi Pyffish Demo ===")
    print("This script demonstrates Xiangqi implementation with pyffish")
    
    if has_pyffish:
        xiangqi_pyffish_demo()
        compare_xiangqi_implementations()
    else:
        print("\nSkipping pyffish-based demos due to missing dependency.")
        
    print("\n=== Demo Completed ===")


if __name__ == "__main__":
    main()