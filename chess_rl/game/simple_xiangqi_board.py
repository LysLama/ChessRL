"""
Simple Xiangqi Board implementation using pyffish API
"""

import numpy as np
import pyffish as sf
from typing import List, Tuple, Optional, Dict, Any

# Constants for piece representation
RED = True    # RED là người chơi đầu tiên, tương đương WHITE trong cờ vua
BLACK = False

class SimpleXiangqiBoard:
    """
    A simple implementation of Xiangqi board using pyffish API directly.
    This class avoids complex inheritance or type annotations to ensure it works correctly.
    """
    
    def __init__(self):
        """Initialize a new Xiangqi board."""
        self.variant = "xiangqi"
        self.current_fen = sf.start_fen(self.variant)
        self.move_history = []
        self.result = None
    
    def reset(self):
        """Reset the board to the starting position."""
        self.current_fen = sf.start_fen(self.variant)
        self.move_history = []
        self.result = None
    
    def get_legal_moves(self):
        """Get a list of legal moves in the current position."""
        try:
            return sf.legal_moves(self.variant, self.current_fen, [])
        except Exception as e:
            print(f"Error getting legal moves: {e}")
            return []
    
    def make_move(self, move_str):
        """
        Make a move on the board.
        
        Args:
            move_str: String representation of the move (e.g., "h3h10")
            
        Returns:
            Tuple of (reward, is_done)
        """
        # Check if move is legal
        legal_moves = self.get_legal_moves()
        if move_str not in legal_moves:
            raise ValueError(f"Illegal move: {move_str}")
        
        # Update move history
        self.move_history.append(move_str)
        
        # Apply the move
        try:
            self.current_fen = sf.get_fen(self.variant, self.current_fen, [move_str])
        except Exception as e:
            # Revert move history if error
            self.move_history.pop()
            raise ValueError(f"Error making move: {e}")
        
        # Check if game is over (no legal moves for opponent)
        try:
            opponent_moves = sf.legal_moves(self.variant, self.current_fen, [])
            is_done = len(opponent_moves) == 0
        except Exception:
            is_done = False
        
        # Determine reward
        reward = 0
        if is_done:
            # The player who just moved wins
            reward = 1
        
        return reward, is_done
    
    def is_game_over(self):
        """Check if the game is over."""
        try:
            return len(sf.legal_moves(self.variant, self.current_fen, [])) == 0
        except Exception:
            return False
    
    def get_observation(self):
        """
        Convert the current board state to a tensor observation.
        
        Returns:
            Numpy array with shape (14, 10, 9) representing the board
            - 14 planes for 7 piece types x 2 colors
            - 10 ranks (rows)
            - 9 files (columns)
        """
        # Constants
        BOARD_SIZE_X = 9
        BOARD_SIZE_Y = 10
        NUM_PIECE_TYPES = 7
        NUM_PLANES = NUM_PIECE_TYPES * 2  # 7 piece types x 2 colors
        
        # Piece mapping (FEN character to (piece_type, color))
        piece_mapping = {
            'P': (0, True),  # Red Pawn
            'N': (1, True),  # Red Horse/Knight
            'B': (2, True),  # Red Elephant
            'A': (3, True),  # Red Advisor
            'R': (4, True),  # Red Rook
            'C': (5, True),  # Red Cannon
            'K': (6, True),  # Red King
            'p': (0, False), # Black Pawn
            'n': (1, False), # Black Horse/Knight
            'b': (2, False), # Black Elephant
            'a': (3, False), # Black Advisor
            'r': (4, False), # Black Rook
            'c': (5, False), # Black Cannon
            'k': (6, False), # Black King
        }
        
        # Initialize empty tensor
        obs = np.zeros((NUM_PLANES, BOARD_SIZE_Y, BOARD_SIZE_X), dtype=np.float32)
        
        # Parse FEN to fill the tensor
        board_part = self.current_fen.split(' ')[0]
        ranks = board_part.split('/')
        
        # Fill the tensor with pieces from FEN
        for rank_idx, rank in enumerate(ranks):
            file_idx = 0
            for char in rank:
                if char.isdigit():
                    # Skip empty squares
                    file_idx += int(char)
                else:
                    # Place piece on board
                    if char in piece_mapping:
                        piece_type, is_red = piece_mapping[char]
                        plane_idx = piece_type if is_red else piece_type + NUM_PIECE_TYPES // 2
                        obs[plane_idx, rank_idx, file_idx] = 1.0
                    file_idx += 1
        
        return obs
    
    def get_state_hash(self):
        """Get a string representation of the current position (FEN)."""
        return self.current_fen
    
    def get_result(self):
        """Get the result of the game if it's over."""
        if not self.is_game_over():
            return {"winner": None, "termination": None}
        
        # Determine winner based on who has no legal moves
        current_player = self.current_fen.split(' ')[1] == 'w'  # True if red to move
        
        return {
            "winner": "black" if current_player else "red",
            "termination": "checkmate"
        }