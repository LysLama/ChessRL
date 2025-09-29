"""
Board Base module - Abstract base class for board game implementations
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import List, Tuple, Dict, Any, Optional, Generic, TypeVar

# Định nghĩa kiểu chung cho nước đi, sẽ được định rõ trong các lớp con
M = TypeVar('M')


class BoardBase(Generic[M], ABC):
    """
    Abstract base class for board games.
    
    This class defines the common interface for different board games like Chess and Xiangqi.
    Implementations should inherit from this class and implement all abstract methods.
    """
    
    @abstractmethod
    def reset(self) -> None:
        """Reset the board to initial position."""
        pass
    
    @abstractmethod
    def get_legal_moves(self, player: Optional[bool] = None) -> List[M]:
        """
        Get all legal moves for the current position.
        
        Args:
            player: Optional player color (True for first player, False for second player)
                   If None, returns moves for current player
        
        Returns:
            List of legal moves
        """
        pass
    
    @abstractmethod
    def apply_move(self, move: M) -> Tuple[float, bool]:
        """
        Apply a move to the board.
        
        Args:
            move: A move object to apply
            
        Returns:
            tuple of (reward, done)
            - reward is 0 for regular moves
            - reward is 1 for winning moves
            - reward is -1 for losing moves
            - reward is 0 for draw
            - done is True if the game is over
        """
        pass
    
    @abstractmethod
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        pass
    
    @abstractmethod
    def to_observation(self) -> np.ndarray:
        """
        Convert the board state to a tensor observation.
        
        Returns:
            Numpy array with appropriate shape for the specific game
        """
        pass
    
    @abstractmethod
    def get_state_hash(self) -> str:
        """
        Get a compact representation of the board state for hashing.
        
        Returns:
            String representation of the current board state
        """
        pass
    
    @abstractmethod
    def get_result(self) -> Dict[str, Any]:
        """
        Get the game result if the game is over.
        
        Returns:
            Dictionary containing game result information
        """
        pass