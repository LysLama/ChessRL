"""
Unit tests for the Xiangqi board implementation.

This module contains tests for basic moves, captures, and other Xiangqi rules.
"""

import pytest
import sys
import os
import numpy as np

# Add the parent directory to path so we can import from game module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game.xiangqi_board import XiangqiBoard, XiangqiMove, RED, BLACK
from game.xiangqi_board import GENERAL, ADVISOR, ELEPHANT, HORSE, CHARIOT, CANNON, SOLDIER


class TestXiangqiBoard:
    """Test suite for XiangqiBoard class."""
    
    def test_init(self):
        """Test board initialization."""
        board = XiangqiBoard()
        assert board.current_player == RED
        assert len(board.move_history) == 0
    
    def test_board_dimensions(self):
        """Test board dimensions."""
        board = XiangqiBoard()
        observation = board.to_observation()
        assert observation.shape == (board.NUM_PLANES, board.BOARD_HEIGHT, board.BOARD_WIDTH)
        assert board.BOARD_HEIGHT == 10
        assert board.BOARD_WIDTH == 9
    
    def test_initial_pieces(self):
        """Test initial piece positions."""
        board = XiangqiBoard()
        
        # Kiểm tra vị trí quân Tướng đỏ
        assert board.board[0, 4] == GENERAL
        
        # Kiểm tra vị trí quân Tướng đen
        assert board.board[9, 4] == -GENERAL
        
        # Kiểm tra vị trí quân Pháo đỏ
        assert board.board[2, 1] == CANNON
        assert board.board[2, 7] == CANNON
        
        # Kiểm tra vị trí quân Xe đen
        assert board.board[9, 0] == -CHARIOT
        assert board.board[9, 8] == -CHARIOT
    
    def test_str_representation(self):
        """Test string representation of the board."""
        board = XiangqiBoard()
        str_rep = str(board)
        
        # Kiểm tra rằng đầu ra có định dạng đúng
        assert "Turn: Red" in str_rep
        # Check that the board representation contains the expected row format
        lines = str_rep.replace("  ", "").split("\n")
        assert "9 r h e a g a e h r " in lines
    
    # Các test khác sẽ được bổ sung khi hoàn thiện logic luật chơi