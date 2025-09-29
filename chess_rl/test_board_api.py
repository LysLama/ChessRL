"""
Script nhỏ để kiểm tra ChessBoard API hoạt động đúng.
"""

import sys
import os

# Thêm thư mục gốc vào path để import từ module game
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import chess
from game.chess_board import ChessBoard


def test_board_api():
    """Kiểm tra các chức năng cơ bản của ChessBoard API."""
    print("=== Kiểm tra ChessBoard API ===")
    
    # 1. Tạo board mới
    board = ChessBoard()
    print(f"Khởi tạo board mới:")
    print(board)
    print()
    
    # 2. Lấy các nước đi hợp lệ
    legal_moves = board.get_legal_moves()
    print(f"Số nước đi hợp lệ: {len(legal_moves)}")
    print(f"5 nước đi đầu tiên: {list(legal_moves)[:5]}")
    print()
    
    # 3. Thực hiện một nước đi
    move = chess.Move.from_uci("e2e4")
    reward, done = board.apply_move(move)
    print(f"Sau khi đi nước e2e4:")
    print(f"Reward: {reward}, Done: {done}")
    print(board)
    print()
    
    # 4. Chuyển đổi board thành observation tensor
    observation = board.to_observation()
    print(f"Observation tensor shape: {observation.shape}")
    print(f"Tổng số quân trên bàn cờ: {observation.sum()}")
    print()
    
    # 5. Thử một nước bắt quân
    board = ChessBoard("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    print("Board với nước đi bắt quân:")
    print(board)
    
    capture_move = chess.Move.from_uci("e4d5")
    reward, done = board.apply_move(capture_move)
    print(f"Sau khi bắt quân e4d5:")
    print(f"Reward: {reward}, Done: {done}")
    print(board)
    
    # Kiểm tra quân ở d5
    piece = board.board.piece_at(chess.parse_square("d5"))
    print(f"Quân ở d5: {piece}, Color: {'Trắng' if piece and piece.color == chess.WHITE else 'Đen' if piece else 'Không có quân'}")
    print()
    
    print("=== Kiểm tra hoàn tất ===")


if __name__ == "__main__":
    test_board_api()