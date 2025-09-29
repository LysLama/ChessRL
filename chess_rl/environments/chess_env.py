"""
Chess Environment module - Gym-compatible chess environment
"""

import random
import numpy as np
import chess
from typing import Tuple, Dict, Any, List, Optional, Union
from environments.base_env import BaseEnv
from game.chess_board import ChessBoard
from game.move import Move


class ChessEnv(BaseEnv):
    """
    Chess environment implementing the Gym interface.
    
    This class wraps a ChessBoard and provides conversion between
    move indices and Move objects.
    """
    
    # Default settings
    DEFAULT_MAX_STEPS = 400  # Maximum steps before episode truncation
    
    def __init__(self, max_steps: int = DEFAULT_MAX_STEPS):
        """
        Initialize the chess environment.
        
        Args:
            max_steps: Maximum number of steps per episode
        """
        self.board = ChessBoard()
        self.max_steps = max_steps
        self.steps = 0
        self.current_player = chess.WHITE  # White starts
        self.rng = random.Random()
    
    def reset(self, seed: Optional[int] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Reset the environment to an initial state.
        
        Args:
            seed: Random seed for reproducibility
            
        Returns:
            observation: Initial observation
            info: Additional information
        """
        # Set random seed if provided
        if seed is not None:
            self.seed(seed)
        
        # Reset board
        self.board.reset()
        self.steps = 0
        self.current_player = chess.WHITE
        
        # Return initial observation and info
        info = {
            "legal_moves": self._get_legal_move_indices(),
            "action_mask": self._get_action_mask(),
            "turn": "white",
            "fen": self.board.board.fen()
        }
        
        return self.board.to_observation(), info
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Take a step in the environment.
        
        Args:
            action: Action index to take (maps to a legal chess move)
            
        Returns:
            observation: Next state observation
            reward: Reward signal
            terminated: Whether the episode has terminated
            truncated: Whether the episode was truncated (time limit)
            info: Additional information
        """
        # Convert action index to Move
        legal_moves = list(self.board.get_legal_moves())
        if action >= len(legal_moves):
            raise ValueError(f"Invalid action index: {action}. Only {len(legal_moves)} legal moves.")
        
        move = legal_moves[action]
        
        # Apply the move
        reward, game_over = self.board.apply_move(move)
        self.steps += 1
        
        # Switch player
        self.current_player = not self.current_player
        
        # Check for termination
        terminated = game_over
        truncated = self.steps >= self.max_steps
        
        # Build info dict
        info = {
            "legal_moves": self._get_legal_move_indices(),
            "action_mask": self._get_action_mask(),
            "turn": "white" if self.board.board.turn else "black",
            "fen": self.board.board.fen()
        }
        
        if terminated:
            result = self.board.get_result()
            info["result"] = result
        
        return self.board.to_observation(), reward, terminated, truncated, info
    
    def render(self, mode: str = "human") -> Optional[np.ndarray]:
        """
        Render the environment.
        
        Args:
            mode: Rendering mode ('human' for display, 'rgb_array' for array)
            
        Returns:
            If mode is 'rgb_array', returns an RGB image as numpy array
            If mode is 'human', renders to a display and returns None
        """
        if mode == "human":
            print(self.board)
            return None
        elif mode == "rgb_array":
            # This is a placeholder - would need to implement board visualization
            # that returns an RGB numpy array
            raise NotImplementedError(
                "rgb_array rendering mode not implemented. Use 'human' mode."
            )
        else:
            raise ValueError(f"Unsupported render mode: {mode}")
    
    def close(self) -> None:
        """Clean up resources used by the environment."""
        pass
    
    def seed(self, seed: Optional[int] = None) -> None:
        """
        Set the random seed for the environment.
        
        Args:
            seed: The random seed to use
        """
        self.rng = random.Random(seed)
    
    def _get_legal_move_indices(self) -> List[int]:
        """
        Return indices corresponding to legal moves.
        
        Returns:
            List of valid action indices
        """
        return list(range(len(self.board.get_legal_moves())))
    
    def _get_action_mask(self) -> np.ndarray:
        """
        Generate a binary mask for valid actions.
        
        Returns:
            Binary array of shape (4096,) where 1 indicates a legal move
        """
        # Chess has a maximum of 64*64 = 4096 possible moves (all squares to all squares)
        mask = np.zeros(4096, dtype=np.int8)
        legal_moves = self.board.get_legal_moves()
        
        for move in legal_moves:
            # Convert move to index in 4096 space
            from_sq = move.from_square
            to_sq = move.to_square
            move_idx = from_sq * 64 + to_sq
            mask[move_idx] = 1
        
        return mask
    
    def move_to_action(self, move: Union[chess.Move, Move, str]) -> int:
        """
        Convert a chess.Move, Move, or UCI string to action index.
        
        Args:
            move: Move to convert
            
        Returns:
            Action index
            
        Raises:
            ValueError: If the move is not legal
        """
        if isinstance(move, str):
            move = chess.Move.from_uci(move)
        elif isinstance(move, Move):
            move = chess.Move(move.from_sq, move.to_sq, move.promotion)
        
        legal_moves = list(self.board.get_legal_moves())
        try:
            return legal_moves.index(move)
        except ValueError:
            raise ValueError(f"Move {move} is not legal in current position")
    
    def action_to_move(self, action: int) -> chess.Move:
        """
        Convert action index to chess.Move.
        
        Args:
            action: Action index
            
        Returns:
            chess.Move object
            
        Raises:
            ValueError: If the action index is invalid
        """
        legal_moves = list(self.board.get_legal_moves())
        if action >= len(legal_moves):
            raise ValueError(f"Invalid action index: {action}. Only {len(legal_moves)} legal moves.")
        
        return legal_moves[action]