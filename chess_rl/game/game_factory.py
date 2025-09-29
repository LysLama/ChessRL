"""
Game Factory module - Factory pattern for creating game boards and environments
"""

from typing import Union, Optional
from game.chess_board import ChessBoard
from game.xiangqi_board import XiangqiBoard
from game.xiangqi_pyffish_board import XiangqiPyffishBoard
from game.simple_xiangqi_board import SimpleXiangqiBoard
from environments.chess_env import ChessEnv
from environments.xiangqi_env import XiangqiEnv
from game.board_base import BoardBase


class GameFactory:
    """
    Factory class to create appropriate board and environment instances.
    
    This class implements the factory pattern to create appropriate board
    and environment instances based on the game type specified.
    """
    
    # Game type constants
    CHESS = "chess"
    XIANGQI = "xiangqi"
    XIANGQI_PYFFISH = "xiangqi_pyffish"
    XIANGQI_SIMPLE = "xiangqi_simple"
    
    @staticmethod
    def create_board(game_type: str) -> Union[ChessBoard, XiangqiBoard, XiangqiPyffishBoard, SimpleXiangqiBoard]:
        """
        Create a board instance based on the game type.
        
        Args:
            game_type: Type of game ("chess", "xiangqi", "xiangqi_pyffish", or "xiangqi_simple")
            
        Returns:
            Board instance for the specified game type
            
        Raises:
            ValueError: If the game type is not supported
        """
        if game_type.lower() == GameFactory.CHESS:
            return ChessBoard()
        elif game_type.lower() == GameFactory.XIANGQI:
            return XiangqiBoard()
        elif game_type.lower() == GameFactory.XIANGQI_PYFFISH:
            return XiangqiPyffishBoard()
        elif game_type.lower() == GameFactory.XIANGQI_SIMPLE:
            return SimpleXiangqiBoard()
        else:
            raise ValueError(f"Unsupported game type: {game_type}")
    
    @staticmethod
    def create_environment(game_type: str, max_steps: Optional[int] = None) -> Union[ChessEnv, XiangqiEnv]:
        """
        Create an environment instance based on the game type.
        
        Args:
            game_type: Type of game ("chess" or "xiangqi")
            max_steps: Maximum number of steps for the environment
            
        Returns:
            Environment instance for the specified game type
            
        Raises:
            ValueError: If the game type is not supported
        """
        if game_type.lower() == GameFactory.CHESS:
            if max_steps is not None:
                return ChessEnv(max_steps=max_steps)
            return ChessEnv()
        elif game_type.lower() == GameFactory.XIANGQI:
            if max_steps is not None:
                return XiangqiEnv(max_steps=max_steps)
            return XiangqiEnv()
        else:
            raise ValueError(f"Unsupported game type: {game_type}")