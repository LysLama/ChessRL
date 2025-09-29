"""
Comprehensive demo for Xiangqi implementations comparing different approaches
"""

import sys
import os

# Add parent directory to path to ensure imports work
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    import pyffish as sf
    has_pyffish = True
except ImportError:
    has_pyffish = False
    print("WARNING: pyffish not installed. Some demos will be skipped.")
    print("Please install with: pip install pyffish")

# Import local modules only if they exist
try:
    from game.game_factory import GameFactory
    from game.xiangqi_pyffish_board import XiangqiPyffishMove
    has_game_factory = True
except ImportError:
    has_game_factory = False
    print("WARNING: game_factory module not found. Some demos will be skipped.")

try:
    from game.simple_xiangqi_board import SimpleXiangqiBoard
    has_simple_xiangqi = True
except ImportError:
    has_simple_xiangqi = False
    print("WARNING: simple_xiangqi_board module not found. Some demos will be skipped.")


def direct_pyffish_demo():
    """Demo for direct pyffish API usage with Xiangqi."""
    if not has_pyffish:
        print("Skipping direct pyffish demo: pyffish not installed")
        return
    
    print("\n" + "="*50)
    print("DIRECT PYFFISH API DEMO")
    print("="*50)
    
    # Basic pyffish usage
    print(f"Pyffish version: {sf.version()}")
    variant = "xiangqi"
    init_fen = sf.start_fen(variant)
    print(f"Initial FEN: {init_fen}")
    
    # Get legal moves
    moves = sf.legal_moves(variant, init_fen, [])
    print(f"Legal moves count: {len(moves)}")
    print(f"Sample moves: {moves[:5]}")
    
    # Display board if the function is available
    print("\nBoard representation:")
    if hasattr(sf, 'get_fen_board'):
        try:
            board = sf.get_fen_board(variant, init_fen)
            print(board)
        except Exception as e:
            print(f"Error displaying board: {e}")
    else:
        print("Function get_fen_board not available in this pyffish version")
    
    # Make a move
    if moves:
        move = moves[0]
        print(f"\nApplying move: {move}")
        try:
            # Apply move directly with pyffish
            new_fen = sf.get_fen(variant, init_fen, [move])
            print(f"New FEN: {new_fen}")
            
            # Show new board
            new_board = sf.get_fen_board(variant, new_fen)
            print("\nBoard after move:")
            print(new_board)
            
            # Get new legal moves
            new_moves = sf.legal_moves(variant, new_fen, [])
            print(f"New legal moves count: {len(new_moves)}")
            print(f"Sample new moves: {new_moves[:5]}")
        except Exception as e:
            print(f"Error applying move: {e}")
    
    # Example of a simple game simulation
    print("\n--- Simple game simulation ---")
    
    try:
        # Reset for clean simulation
        position = init_fen
        
        # Play alternating moves
        print("Move 1: a1a2")
        position1 = sf.get_fen(variant, position, ["a1a2"])
        print(f"Position after move 1: {position1}")
        
        print("Move 2: a10a9")
        position2 = sf.get_fen(variant, position1, ["a10a9"])
        print(f"Position after move 2: {position2}")
        
        print("Move 3: i1i2")
        position3 = sf.get_fen(variant, position2, ["i1i2"])
        print(f"Position after move 3: {position3}")
        
        print("Final position after 3 moves shown above")
        
        # Display final board if the function is available
        if hasattr(sf, 'get_fen_board'):
            try:
                final_board = sf.get_fen_board(variant, position3)
                print(final_board)
            except Exception as e:
                print(f"Error displaying final board: {e}")
    except Exception as e:
        print(f"Error during game simulation: {e}")


def xiangqi_pyffish_wrapper_demo():
    """Demo for Xiangqi board implementation using pyffish wrapper."""
    if not has_pyffish or not has_game_factory:
        print("Skipping pyffish wrapper demo: required modules not available")
        return
    
    print("\n" + "="*50)
    print("XIANGQI PYFFISH WRAPPER DEMO")
    print("="*50)
    
    # Create board through game factory
    game_factory = GameFactory()
    board = game_factory.create_board("xiangqi_pyffish")
    
    # Access the current FEN if possible - handle both interfaces
    try:
        if hasattr(board, 'current_fen'):
            print(f"Current FEN: {board.current_fen}")
        else:
            print("FEN not directly accessible through current_fen attribute")
    except Exception as e:
        print(f"Error accessing FEN: {e}")
    
    # Get legal moves
    legal_moves = board.get_legal_moves()
    print(f"Legal moves count: {len(legal_moves)}")
    print(f"Sample moves: {[str(move) for move in legal_moves[:5]] if legal_moves else 'None'}")
    
    # Make a move
    if legal_moves:
        move_obj = legal_moves[0]
        print(f"\nMaking move: {str(move_obj)}")
            
        # Apply the move
        try:
            reward, done = board.apply_move(move_obj)
            print(f"Reward: {reward}, Game over: {done}")
        except AttributeError:
            # Try alternative method name
            if hasattr(board, 'make_move'):
                reward, done = board.make_move(move_obj)
                print(f"Reward: {reward}, Game over: {done}")
            else:
                print("Error: Neither apply_move nor make_move method found")
        
        # Access updated FEN
        try:
            if hasattr(board, 'current_fen'):
                print(f"New FEN: {board.current_fen}")
            else:
                print("Updated FEN not directly accessible")
        except Exception as e:
            print(f"Error accessing updated FEN: {e}")
        
        # Check new legal moves
        new_legal_moves = board.get_legal_moves()
        print(f"New legal moves count: {len(new_legal_moves)}")
        print(f"Sample new moves: {[str(move) for move in new_legal_moves[:5]] if new_legal_moves else 'None'}")


def simple_xiangqi_demo():
    """Demo for the simplified Xiangqi implementation."""
    if not has_simple_xiangqi:
        print("Skipping simple xiangqi demo: required module not available")
        return
    
    print("\n" + "="*50)
    print("SIMPLE XIANGQI BOARD DEMO")
    print("="*50)
    
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
        print(f"New legal moves count: {len(new_legal_moves)}")
        print(f"Sample new moves: {new_legal_moves[:5]}")
    
    # Reset board
    print("\nResetting board...")
    board.reset()
    print(f"Board reset to: {board.current_fen}")


def comparison_demo():
    """Compare different implementations side by side."""
    if not (has_pyffish and has_game_factory and has_simple_xiangqi):
        print("Skipping comparison demo: some required modules not available")
        return
    
    print("\n" + "="*50)
    print("IMPLEMENTATION COMPARISON DEMO")
    print("="*50)
    
    # Create instances
    direct_fen = sf.start_fen("xiangqi")
    
    game_factory = GameFactory()
    wrapper_board = game_factory.create_board("xiangqi_pyffish")
    
    simple_board = SimpleXiangqiBoard()
    
    # Compare FENs
    print("\n--- Initial FEN Comparison ---")
    print(f"Direct pyffish:   {direct_fen}")
    
    # Get FEN from wrapper board - handle possible interface differences
    wrapper_fen = "FEN not directly accessible"
    try:
        if hasattr(wrapper_board, 'current_fen'):
            wrapper_fen = wrapper_board.current_fen
    except Exception:
        pass
    print(f"Pyffish wrapper:  {wrapper_fen}")
    
    print(f"Simple xiangqi:   {simple_board.current_fen}")
    
    # Compare legal moves
    print("\n--- Legal Moves Comparison ---")
    direct_moves = sf.legal_moves("xiangqi", direct_fen, [])
    wrapper_moves = wrapper_board.get_legal_moves()
    simple_moves = simple_board.get_legal_moves()
    
    print(f"Direct pyffish:  {len(direct_moves)} moves")
    print(f"Pyffish wrapper: {len(wrapper_moves)} moves")
    print(f"Simple xiangqi:  {len(simple_moves)} moves")
    
    # Make same move in all implementations if possible
    print("\n--- Making a move in all implementations ---")
    if direct_moves:
        move = direct_moves[0]
        print(f"Selected move: {move}")
        
        # Direct pyffish
        new_fen = sf.get_fen("xiangqi", direct_fen, [move])
        print(f"Direct pyffish new FEN:   {new_fen}")
        
        # Wrapper - handle possible interface differences
        wrapper_move = wrapper_moves[0] if wrapper_moves else None
        if wrapper_move:
            try:
                # Try apply_move first
                if hasattr(wrapper_board, 'apply_move'):
                    wrapper_board.apply_move(wrapper_move)
                # Fall back to make_move if needed
                elif hasattr(wrapper_board, 'make_move'):
                    wrapper_board.make_move(wrapper_move)
                else:
                    print("No apply_move or make_move method found on wrapper board")
                
                # Get updated FEN
                updated_wrapper_fen = "Updated FEN not directly accessible"
                if hasattr(wrapper_board, 'current_fen'):
                    updated_wrapper_fen = wrapper_board.current_fen
                print(f"Pyffish wrapper new FEN:  {updated_wrapper_fen}")
            except Exception as e:
                print(f"Error making move with wrapper: {e}")
        
        # Simple xiangqi
        simple_move = simple_moves[0] if simple_moves else None
        if simple_move:
            try:
                simple_board.make_move(simple_move)
                print(f"Simple xiangqi new FEN:   {simple_board.current_fen}")
            except Exception as e:
                print(f"Error making move with simple board: {e}")


if __name__ == "__main__":
    print("Running Xiangqi demos...")
    direct_pyffish_demo()
    xiangqi_pyffish_wrapper_demo()
    simple_xiangqi_demo()
    comparison_demo()
    print("\nAll demos complete!")