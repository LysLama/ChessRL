"""
Unit tests for the chess board implementation.

This module contains tests for basic moves, captures, check/checkmate detection,
and other chess rules.
"""

import pytest
import chess
import numpy as np
import sys
import os

# Add the parent directory to path so we can import from game module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from game.chess_board import ChessBoard
from game.move import Move


class TestChessBoard:
    """Test suite for ChessBoard class."""
    
    def test_init(self):
        """Test board initialization."""
        board = ChessBoard()
        assert not board.is_game_over()
        assert board.board.turn == chess.WHITE
        assert len(board.get_legal_moves()) == 20  # Standard initial position has 20 legal moves
    
    def test_init_from_fen(self):
        """Test board initialization from FEN string."""
        fen = "rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2"
        board = ChessBoard(fen)
        assert board.board.turn == chess.BLACK
        assert not board.is_game_over()
    
    def test_reset(self):
        """Test board reset."""
        board = ChessBoard("8/8/8/8/8/8/8/8 w - - 0 1")  # Empty board
        board.reset()
        assert board.board.turn == chess.WHITE
        assert len(board.get_legal_moves()) == 20
    
    def test_get_legal_moves(self):
        """Test legal move generation."""
        board = ChessBoard()
        moves = board.get_legal_moves()
        assert len(moves) == 20
        
        # Check that all moves are legal
        for move in moves:
            assert move in board.board.legal_moves
    
    def test_get_legal_moves_for_player(self):
        """Test legal move generation for specific player."""
        board = ChessBoard()
        white_moves = board.get_legal_moves(player=chess.WHITE)
        assert len(white_moves) == 20
        
        # Black has no moves on initial position when it's White's turn
        black_moves = board.get_legal_moves(player=chess.BLACK)
        assert len(black_moves) == 0
    
    def test_apply_move_basic(self):
        """Test applying a basic move."""
        board = ChessBoard()
        e4 = chess.Move.from_uci("e2e4")
        
        reward, done = board.apply_move(e4)
        assert reward == 0  # Regular move, no reward
        assert not done  # Game not over
        assert board.board.turn == chess.BLACK  # Turn switched to black
    
    def test_apply_illegal_move(self):
        """Test applying an illegal move."""
        board = ChessBoard()
        illegal_move = chess.Move.from_uci("e2e5")  # Pawn can't move 3 squares
        
        with pytest.raises(ValueError):
            board.apply_move(illegal_move)
    
    def test_apply_capture_move(self):
        """Test applying a capture move."""
        # Set up a position with a capture
        fen = "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
        board = ChessBoard(fen)
        
        # White captures black pawn
        capture = chess.Move.from_uci("e4d5")
        reward, done = board.apply_move(capture)
        
        assert reward == 0  # Regular move, no reward yet
        assert not done  # Game not over
        
        # Kiểm tra rằng có một quân cờ ở d5 và đó là quân trắng
        piece = board.board.piece_at(chess.parse_square("d5"))
        assert piece is not None, "Phải có một quân cờ ở d5"
        assert piece.color == chess.WHITE  # White piece on d5
    
    def test_checkmate_detection(self):
        """Test checkmate detection."""
        # Scholar's mate position
        fen = "rnbqkbnr/pppp1ppp/8/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 3 3"
        board = ChessBoard(fen)
        
        # Queen captures f7 pawn, delivering checkmate
        checkmate = chess.Move.from_uci("f3f7")
        reward, done = board.apply_move(checkmate)
        
        assert reward == 1.0  # White wins, positive reward
        assert done  # Game over
        assert board.is_game_over()
        
        result = board.get_result()
        assert result["winner"] == "white"
        assert result["termination"] == "CHECKMATE"
    
    def test_stalemate_detection(self):
        """Test stalemate detection."""
        # Stalemate position
        fen = "k7/8/1Q6/8/8/8/8/7K b - - 0 1"
        board = ChessBoard(fen)
        
        # Verify it's a stalemate
        assert not board.board.is_check()
        assert len(board.get_legal_moves()) == 0
        assert board.board.is_stalemate()
        
        # No moves available, but game is over due to stalemate
        assert board.is_game_over()
        
        result = board.get_result()
        assert result["winner"] is None  # Draw
        assert result["termination"] == "STALEMATE"
    
    def test_insufficient_material_detection(self):
        """Test insufficient material detection."""
        # King vs King position
        fen = "8/8/8/4k3/8/8/8/4K3 w - - 0 1"
        board = ChessBoard(fen)
        
        assert board.is_game_over()
        result = board.get_result()
        assert result["winner"] is None  # Draw
        assert result["termination"] == "INSUFFICIENT_MATERIAL"
    
    def test_to_observation(self):
        """Test observation tensor generation."""
        board = ChessBoard()
        observation = board.to_observation()
        
        # Check shape
        assert observation.shape == (12, 8, 8)
        
        # Check data type
        assert observation.dtype == np.float32
        
        # Check white pawns are correctly placed in plane 0 (pawns, white)
        # In initial position, white pawns are on rank 2
        white_pawn_plane = observation[0]
        for col in range(8):
            assert white_pawn_plane[6, col] == 1.0  # Rank 2 is index 6 (flipped)
        
        # Check black pawns are correctly placed in plane 6 (pawns, black)
        # In initial position, black pawns are on rank 7
        black_pawn_plane = observation[6]
        for col in range(8):
            assert black_pawn_plane[1, col] == 1.0  # Rank 7 is index 1 (flipped)
    
    def test_move_history(self):
        """Test move history tracking."""
        board = ChessBoard()
        moves = [
            chess.Move.from_uci("e2e4"),
            chess.Move.from_uci("e7e5"),
            chess.Move.from_uci("g1f3"),
        ]
        
        for move in moves:
            board.apply_move(move)
        
        assert len(board.move_history) == 3
        assert board.move_history == moves
    
    def test_get_state_hash(self):
        """Test state hash generation."""
        board1 = ChessBoard()
        board2 = ChessBoard()
        
        # Same initial position should have same hash
        assert board1.get_state_hash() == board2.get_state_hash()
        
        # Different positions should have different hashes
        board1.apply_move(chess.Move.from_uci("e2e4"))
        assert board1.get_state_hash() != board2.get_state_hash()


class TestMoveConversion:
    """Test conversion between chess.Move and Move objects."""
    
    def test_move_from_uci(self):
        """Test creating Move from UCI string."""
        move = Move.from_uci("e2e4")
        assert move.from_sq == chess.parse_square("e2")
        assert move.to_sq == chess.parse_square("e4")
        assert move.promotion is None
    
    def test_move_with_promotion(self):
        """Test creating Move with promotion from UCI string."""
        move = Move.from_uci("e7e8q")
        assert move.from_sq == chess.parse_square("e7")
        assert move.to_sq == chess.parse_square("e8")
        assert move.promotion == 5  # Queen
    
    def test_move_to_uci(self):
        """Test converting Move to UCI string."""
        move = Move(from_sq=chess.parse_square("e2"), to_sq=chess.parse_square("e4"))
        assert move.to_uci() == "e2e4"
        
        move_with_promotion = Move(
            from_sq=chess.parse_square("e7"),
            to_sq=chess.parse_square("e8"),
            promotion=5  # Queen
        )
        assert move_with_promotion.to_uci() == "e7e8q"