"""
Xiangqi Environment module - Gym-compatible Chinese chess environment
"""

import random
import numpy as np
from typing import Tuple, Dict, Any, List, Optional
from environments.base_env import BaseEnv
from game.xiangqi_board import XiangqiBoard, XiangqiMove, RED, BLACK


class XiangqiEnv(BaseEnv):
    """
    Xiangqi (Chinese chess) environment implementing the Gym interface.
    
    This class wraps a XiangqiBoard and provides conversion between
    move indices and XiangqiMove objects.
    """
    
    # Default settings
    DEFAULT_MAX_STEPS = 400  # Maximum steps before episode truncation
    
    def __init__(self, max_steps: int = DEFAULT_MAX_STEPS):
        """
        Initialize the Xiangqi environment.
        
        Args:
            max_steps: Maximum number of steps per episode
        """
        self.board = XiangqiBoard()
        self.max_steps = max_steps
        self.steps = 0
        self.current_player = RED  # Red starts
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
        self.current_player = RED
        
        # Return initial observation and info
        info = {
            "legal_moves": self._get_legal_move_indices(),
            "action_mask": self._get_action_mask(),
            "turn": "red",
            "board_str": str(self.board)
        }
        
        return self.board.to_observation(), info
    
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Take a step in the environment.
        
        Args:
            action: Action index to take (maps to a legal Xiangqi move)
            
        Returns:
            observation: Next state observation
            reward: Reward signal
            terminated: Whether the episode has terminated
            truncated: Whether the episode was truncated (time limit)
            info: Additional information
        """
        # Convert action index to XiangqiMove
        legal_moves = self.board.get_legal_moves()
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
            "turn": "red" if self.board.current_player == RED else "black",
            "board_str": str(self.board)
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
            # TODO: Implement proper rendering for Xiangqi board
            raise NotImplementedError(
                "rgb_array rendering mode not implemented for Xiangqi. Use 'human' mode."
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
            Binary array where 1 indicates a legal move
        """
        # Xiangqi có tối đa 90*90 = 8100 nước đi có thể (9x10 bàn cờ)
        mask = np.zeros(8100, dtype=np.int8)
        legal_moves = self.board.get_legal_moves()
        
        for i, move in enumerate(legal_moves):
            # Chuyển đổi từ vị trí (row, col) sang index phẳng
            from_idx = move.from_pos[0] * self.board.BOARD_WIDTH + move.from_pos[1]
            to_idx = move.to_pos[0] * self.board.BOARD_WIDTH + move.to_pos[1]
            move_idx = from_idx * 90 + to_idx  # 90 = 9 * 10 (kích thước bàn cờ)
            mask[move_idx] = 1
        
        return mask
    
    def move_to_action(self, move: XiangqiMove) -> int:
        """
        Convert a XiangqiMove to action index.
        
        Args:
            move: Move to convert
            
        Returns:
            Action index
            
        Raises:
            ValueError: If the move is not legal
        """
        legal_moves = self.board.get_legal_moves()
        try:
            return legal_moves.index(move)
        except ValueError:
            raise ValueError(f"Move {move} is not legal in current position")
    
    def action_to_move(self, action: int) -> XiangqiMove:
        """
        Convert action index to XiangqiMove.
        
        Args:
            action: Action index
            
        Returns:
            XiangqiMove object
            
        Raises:
            ValueError: If the action index is invalid
        """
        legal_moves = self.board.get_legal_moves()
        if action >= len(legal_moves):
            raise ValueError(f"Invalid action index: {action}. Only {len(legal_moves)} legal moves.")
        
        return legal_moves[action]