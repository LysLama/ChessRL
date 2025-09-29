"""
Xiangqi Board implementation using pyffish API
"""

import numpy as np
import pyffish as sf
from typing import List, Tuple, Optional, Dict, Any
from game.board_base import BoardBase

# Xiangqi piece constants
RED = True    # RED là người chơi đầu tiên, tương đương WHITE trong cờ vua
BLACK = False


class XiangqiPyffishMove:
    """
    Represents a Xiangqi move using pyffish format.
    Xiangqi moves are represented as strings like "h3h10" (source and destination squares).
    """
    
    def __init__(self, move_str: str):
        """
        Initialize a Xiangqi move.
        
        Args:
            move_str: String representation of the move (e.g., "h3h10")
        """
        self.move_str = move_str
        
        # No validation needed - we trust pyffish to provide valid moves
        # We'll store the raw move string and use it directly
    
    def __str__(self):
        return self.move_str
    
    def __repr__(self):
        return f"XiangqiPyffishMove('{self.move_str}')"
    
    def __eq__(self, other):
        if isinstance(other, XiangqiPyffishMove):
            return self.move_str == other.move_str
        return False
    
    def __hash__(self):
        return hash(self.move_str)


class XiangqiPyffishBoard(BoardBase[XiangqiPyffishMove]):
    """
    Xiangqi (Chinese Chess) board implementation using pyffish library.
    
    This class provides a standardized API for:
    - Board state representation
    - Move generation and validation
    - Move application
    - Game termination detection
    - Serialization for hashing states
    - Observation tensor generation
    """
    
    # Mapping piece types to plane indices (for observation tensor)
    # Xiangqi has 14 planes: 7 piece types x 2 colors
    # Piece types: Pawn, Horse, Elephant, Advisor, Rook, Cannon, King
    PIECE_MAPPING = {
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
    
    # Board dimensions
    BOARD_SIZE_X = 9  # files a-i
    BOARD_SIZE_Y = 10 # ranks 1-10
    NUM_SQUARES = BOARD_SIZE_X * BOARD_SIZE_Y
    NUM_PIECE_TYPES = 7
    NUM_COLORS = 2
    NUM_PLANES = NUM_PIECE_TYPES * NUM_COLORS  # 14 planes
    
    def __init__(self, fen: Optional[str] = None):
        """
        Initialize a Xiangqi board, optionally from a given FEN string.
        
        Args:
            fen: Optional FEN string to initialize the board
        """
        self.variant = "xiangqi"
        self.current_fen = fen or sf.start_fen(self.variant)
        self.move_history = []
        self.result = None
    
    def reset(self) -> None:
        """Reset the board to initial position."""
        self.current_fen = sf.start_fen(self.variant)
        self.move_history = []
        self.result = None
    
    def get_legal_moves(self, player: Optional[bool] = None) -> List[XiangqiPyffishMove]:
        """
        Get all legal moves for the current position.
        
        Args:
            player: Optional player color (True for red, False for black)
                   If None, returns moves for current player
        
        Returns:
            List of legal XiangqiPyffishMove objects
        """
        # Determine current player from FEN
        current_player_char = self.current_fen.split(' ')[1]
        current_player = current_player_char == 'w'  # w = red (True), b = black (False)
        
        # If player is specified and it's not their turn, return empty list
        if player is not None and player != current_player:
            return []
        
        # Get legal moves from pyffish
        # Note: Using empty move history for compatibility with current pyffish version
        try:
            move_strs = sf.legal_moves(self.variant, self.current_fen, [])
        except:
            # Fallback for compatibility issues
            move_strs = sf.legal_moves(self.variant, self.current_fen)
        return [XiangqiPyffishMove(move_str) for move_str in move_strs]
    
    def apply_move(self, move: XiangqiPyffishMove) -> Tuple[float, bool]:
        """
        Apply a move to the board.
        
        Args:
            move: A XiangqiPyffishMove object to apply
            
        Returns:
            tuple of (reward, done)
            - reward is 0 for regular moves
            - reward is 1 for winning moves
            - reward is -1 for losing moves
            - reward is 0 for draw
            - done is True if the game is over
        """
        # Check if move is legal by comparing with legal moves
        try:
            legal_moves = sf.legal_moves(self.variant, self.current_fen, [])
        except:
            # Fallback for compatibility
            legal_moves = sf.legal_moves(self.variant, self.current_fen)
        if move.move_str not in legal_moves:
            raise ValueError(f"Illegal move: {move}")
        
        # Apply the move - update move history first
        self.move_history.append(move.move_str)
        
        # Update FEN
        try:
            # Get the new position after the move
            self.current_fen = sf.get_fen(self.variant, self.current_fen, [move.move_str])
        except Exception as e:
            # If there was an error, restore the state by removing the move from history
            self.move_history.pop()
            raise ValueError(f"Error applying move '{move}'") from e
        
        # Default values
        done = False
        reward = 0
        
        # Check if game is over by seeing if there are any legal moves
        try:
            try:
                next_legal_moves = sf.legal_moves(self.variant, self.current_fen, [])
            except:
                # Fallback for compatibility
                next_legal_moves = sf.legal_moves(self.variant, self.current_fen)
            done = len(next_legal_moves) == 0
            
            if done:
                # If no legal moves, the player who just moved won
                current_player_char = self.current_fen.split(' ')[1]
                # Current player has no moves (lost), previous player won
                prev_player = current_player_char != 'w'  # w = red, b = black
                
                # Set reward: 1 for winner, -1 for loser
                reward = 1 if prev_player else -1
                
                # Store result
                self.result = {
                    'winner': 'red' if prev_player else 'black',
                    'termination': 'checkmate',
                }
        except Exception:
            # If checking for game over fails, assume game continues
            pass
            
        return reward, done
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        try:
            # Check if there are legal moves
            legal_moves = sf.legal_moves(self.variant, self.current_fen, [])
            return len(legal_moves) == 0
        except Exception:
            # If the check fails, assume game is not over
            return False
    
    def to_observation(self) -> np.ndarray:
        """
        Convert the board state to a tensor observation.
        
        Returns:
            Numpy array with shape (14, 10, 9) for Xiangqi
            - 14 channels (7 piece types x 2 colors)
            - 10 ranks
            - 9 files
        """
        # Initialize observation tensor with zeros
        observation = np.zeros((self.NUM_PLANES, self.BOARD_SIZE_Y, self.BOARD_SIZE_X), dtype=np.float32)
        
        # Parse FEN to get piece positions
        board_part = self.current_fen.split(' ')[0]
        ranks = board_part.split('/')
        
        for rank_idx, rank in enumerate(ranks):
            file_idx = 0
            for char in rank:
                if char.isdigit():
                    # Skip empty squares
                    file_idx += int(char)
                else:
                    # Place piece on board
                    if char in self.PIECE_MAPPING:
                        piece_type, is_red = self.PIECE_MAPPING[char]
                        plane_idx = piece_type if is_red else piece_type + self.NUM_PIECE_TYPES
                        observation[plane_idx, rank_idx, file_idx] = 1.0
                    file_idx += 1
        
        return observation
    
    def get_state_hash(self) -> str:
        """
        Get a compact representation of the board state for hashing.
        
        Returns:
            String representation of the current board state (FEN)
        """
        return self.current_fen
    
    def get_result(self) -> Dict[str, Any]:
        """
        Get the game result if the game is over.
        
        Returns:
            Dictionary containing game result information
        """
        if not self.is_game_over():
            return {'winner': None, 'termination': None}
        
        if self.result is not None:
            return self.result
        
        # Calculate result if not stored
        try:
            # Try to determine winner from current position
            # If it's over and it's player's turn, they lost (other player won)
            current_player_char = self.current_fen.split(' ')[1]
            current_player = current_player_char == 'w'  # w = red (True), b = black (False)
            
            # If game is over and it's current player's turn, they lost
            winner = 'black' if current_player else 'red'
            
            self.result = {
                'winner': winner,
                'termination': 'checkmate',
            }
        except Exception:
            # If we can't determine the winner, default to draw
            self.result = {
                'winner': 'draw',
                'termination': 'unknown',
            }
        
        return self.result

    # --- Visualization helpers ---
    def to_pretty_string(self, use_unicode: bool = True, with_coords: bool = True) -> str:
        """
        Return a pretty, human-friendly string representation of the board.

        Args:
            use_unicode: Use Chinese chess unicode glyphs for pieces when True, else ASCII letters
            with_coords: Include file/rank coordinates and board frame

        Returns:
            Multi-line string representing current board position.
        """
        # Piece glyph maps
        ascii_map = {
            'r': 'r', 'n': 'n', 'b': 'b', 'a': 'a', 'k': 'k', 'c': 'c', 'p': 'p',
            'R': 'R', 'N': 'N', 'B': 'B', 'A': 'A', 'K': 'K', 'C': 'C', 'P': 'P'
        }
        unicode_map = {
            # black pieces (lowercase)
            'r': '車', 'n': '馬', 'b': '象', 'a': '士', 'k': '將', 'c': '砲', 'p': '卒',
            # red pieces (uppercase)
            'R': '俥', 'N': '傌', 'B': '相', 'A': '仕', 'K': '帥', 'C': '炮', 'P': '兵'
        }

        piece_map = unicode_map if use_unicode else ascii_map

        board_part = self.current_fen.split(' ')[0]
        rows = board_part.split('/')

        lines = []
        if with_coords:
            lines.append("   a b c d e f g h i")
            lines.append("  " + "-" * 19)

        for i, row in enumerate(rows):
            rank = 10 - i
            if with_coords:
                line = f"{rank:2d}|"
            else:
                line = ""

            for ch in row:
                if ch.isdigit():
                    for _ in range(int(ch)):
                        line += " ." if with_coords else ". "
                else:
                    glyph = piece_map.get(ch, ch)
                    line += f" {glyph}" if with_coords else f"{glyph} "

            if with_coords:
                line += f" |{rank}"
            lines.append(line)

            # River decoration between ranks 6 and 5 (after 5th row printed, i == 4)
            if with_coords and i == 4:
                lines.append("  |" + "-" * 17 + "|")
                lines.append("  |   SÔNG HÀN GIỚI   |")
                lines.append("  |" + "-" * 17 + "|")

        if with_coords:
            lines.append("  " + "-" * 19)
            lines.append("   a b c d e f g h i")

        # Add turn indicator
        try:
            turn = self.current_fen.split(' ')[1]
            turn_txt = "🔴 Đỏ (RED)" if turn == 'w' else "⚫ Đen (BLACK)"
            lines.append("")
            lines.append(f"   Lượt đi: {turn_txt}")
        except Exception:
            pass

        return "\n".join(lines)

    def __str__(self) -> str:  # noqa: D401
        """Default pretty string (unicode + coordinates)."""
        return self.to_pretty_string(use_unicode=True, with_coords=True)