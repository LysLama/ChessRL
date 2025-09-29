"""
Chess Board module - Core representation of a chess board with chess rules
"""

import numpy as np
import chess
from typing import List, Tuple, Optional, Dict, Any
from game.board_base import BoardBase


class ChessBoard(BoardBase[chess.Move]):
    """
    Chess board implementation with standardized interface for RL environments.
    
    This class wraps python-chess library and provides a standardized API for:
    - Board state representation
    - Move generation and validation
    - Move application
    - Game termination detection
    - Serialization for hashing states
    - Observation tensor generation
    """
    
    # Mapping piece types to plane indices (for observation tensor)
    # 12 planes: 6 piece types x 2 colors
    PIECE_TO_PLANE = {
        (chess.PAWN, chess.WHITE): 0,
        (chess.KNIGHT, chess.WHITE): 1,
        (chess.BISHOP, chess.WHITE): 2,
        (chess.ROOK, chess.WHITE): 3,
        (chess.QUEEN, chess.WHITE): 4,
        (chess.KING, chess.WHITE): 5,
        (chess.PAWN, chess.BLACK): 6,
        (chess.KNIGHT, chess.BLACK): 7,
        (chess.BISHOP, chess.BLACK): 8,
        (chess.ROOK, chess.BLACK): 9,
        (chess.QUEEN, chess.BLACK): 10,
        (chess.KING, chess.BLACK): 11,
    }
    
    # Board dimensions
    BOARD_SIZE = 8
    NUM_SQUARES = 64
    NUM_PIECE_TYPES = 6
    NUM_COLORS = 2
    NUM_PLANES = NUM_PIECE_TYPES * NUM_COLORS  # 12 planes
    
    def __init__(self, fen: Optional[str] = None):
        """
        Initialize a chess board, optionally from a given FEN string.
        
        Args:
            fen: Optional FEN string to initialize the board
        """
        self.board = chess.Board(fen) if fen else chess.Board()
        self.move_history = []
        self.result = None
    
    def reset(self) -> None:
        """Reset the board to initial position."""
        self.board.reset()
        self.move_history = []
        self.result = None
    
    def get_legal_moves(self, player: Optional[bool] = None) -> List[chess.Move]:
        """
        Get all legal moves for the current position.
        
        Args:
            player: Optional player color (True for white, False for black)
                   If None, returns moves for current player
        
        Returns:
            List of legal chess.Move objects
        """
        # If player is specified and it's not their turn, return empty list
        if player is not None and player != self.board.turn:
            return []
        
        return list(self.board.legal_moves)
    
    def apply_move(self, move: chess.Move) -> Tuple[float, bool]:
        """
        Apply a move to the board.
        
        Args:
            move: A chess.Move object to apply
            
        Returns:
            tuple of (reward, done)
            - reward is 0 for regular moves
            - reward is 1 for winning moves
            - reward is -1 for losing moves
            - reward is 0 for draw
            - done is True if the game is over
        """
        # Check if move is legal
        if move not in self.board.legal_moves:
            raise ValueError(f"Illegal move: {move}")
        
        # Keep track of game state before the move
        is_check_before = self.board.is_check()
        player_before = self.board.turn
        
        # Apply the move
        self.move_history.append(move)
        self.board.push(move)
        
        # Check game termination
        reward = 0.0
        done = False
        
        if self.board.is_game_over():
            done = True
            result = self.board.outcome()
            self.result = result
            
            if result is not None and result.winner is not None:
                # Assign rewards based on who won
                reward = 1.0 if result.winner == player_before else -1.0
            else:
                # Draw or unknown result
                reward = 0.0
        
        return reward, done
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.board.is_game_over()
    
    def to_observation(self) -> np.ndarray:
        """
        Convert the board state to a tensor observation.
        
        Returns:
            Numpy array with shape (NUM_PLANES, BOARD_SIZE, BOARD_SIZE)
            where NUM_PLANES=12 (6 piece types x 2 colors)
        """
        observation = np.zeros((self.NUM_PLANES, self.BOARD_SIZE, self.BOARD_SIZE), dtype=np.float32)
        
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece is not None:
                # Get row and column from square index
                row, col = divmod(square, self.BOARD_SIZE)
                row = 7 - row  # Flip rows to match chess coordinate system
                
                # Set the corresponding plane
                plane_idx = self.PIECE_TO_PLANE[(piece.piece_type, piece.color)]
                observation[plane_idx, row, col] = 1.0
                
        return observation
    
    def get_state_hash(self) -> str:
        """
        Get a compact representation of the board state for hashing.
        
        Returns:
            FEN string representing the current board state
        """
        return self.board.fen()
    
    def get_result(self) -> Dict[str, Any]:
        """
        Get the game result if the game is over.
        
        Returns:
            Dictionary containing:
            - winner: 'white', 'black', or None for draw
            - termination: reason for game ending
            - moves: number of moves played
            - or empty dictionary if game is not over
        """
        if not self.is_game_over():
            return {}
        
        result = self.board.outcome()
        if result is None:
            return {
                'winner': None,
                'termination': 'UNKNOWN',
                'moves': len(self.move_history)
            }
        
        winner = None
        if result.winner is not None:
            winner = 'white' if result.winner else 'black'
        
        return {
            'winner': winner,
            'termination': result.termination.name if result.termination else 'UNKNOWN',
            'moves': len(self.move_history)
        }
    
    def __str__(self) -> str:
        """String representation of the board."""
        return str(self.board)


# Mã thử nghiệm chỉ chạy khi file được thực thi trực tiếp
if __name__ == "__main__":
    print("=== Kiểm tra ChessBoard ===")
    
    # Khởi tạo board mới
    board = ChessBoard()
    print("Board mới:")
    print(board)
    print()
    
    # Kiểm tra các nước đi hợp lệ
    legal_moves = board.get_legal_moves()
    print(f"Số nước đi hợp lệ: {len(legal_moves)}")
    print(f"Các nước đi mẫu: {list(legal_moves)[:5]}")
    print()
    
    # Thực hiện một nước đi
    if legal_moves:
        move = legal_moves[0]
        print(f"Thực hiện nước đi: {move}")
        reward, done = board.apply_move(move)
        print(f"Sau khi đi: reward={reward}, done={done}")
        print(board)
        print()
    
    # Kiểm tra observation shape
    observation = board.to_observation()
    print(f"Observation shape: {observation.shape}")
    print(f"Tổng số quân trên bàn cờ: {observation.sum()}")