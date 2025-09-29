"""
Base Environment module for RL environments
"""

from typing import Tuple, Dict, Any, Optional
import numpy as np
from abc import ABC, abstractmethod


class BaseEnv(ABC):
    """
    Abstract base class for RL environments.
    
    This class defines the standard Gym-compatible interface for
    environments in this project.
    """
    
    @abstractmethod
    def reset(self, seed: Optional[int] = None) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Reset the environment to an initial state.
        
        Args:
            seed: Optional random seed for reproducibility
            
        Returns:
            observation: Initial observation
            info: Additional information
        """
        pass
    
    @abstractmethod
    def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict[str, Any]]:
        """
        Take a step in the environment.
        
        Args:
            action: Action to take (usually an integer index)
            
        Returns:
            observation: Next state observation
            reward: Reward signal
            terminated: Whether the episode has terminated
            truncated: Whether the episode was truncated (e.g., due to time limit)
            info: Additional information
        """
        pass
    
    @abstractmethod
    def render(self, mode: str = "human") -> Optional[np.ndarray]:
        """
        Render the environment.
        
        Args:
            mode: Rendering mode ('human' for visualization, 'rgb_array' for array)
            
        Returns:
            If mode is 'rgb_array', returns an RGB image as a numpy array
            If mode is 'human', renders to a display and returns None
        """
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Clean up resources used by the environment."""
        pass
    
    @abstractmethod
    def seed(self, seed: Optional[int] = None) -> None:
        """
        Set the random seed for the environment.
        
        Args:
            seed: The random seed to use
        """
        pass