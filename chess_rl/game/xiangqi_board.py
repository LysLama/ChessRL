"""
Xiangqi Board module - Core representation of a Xiangqi (Chinese chess) board with game rules
"""

import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from game.board_base import BoardBase


# Định nghĩa hằng số cho cờ tướng
RED = True   # RED là người chơi đầu tiên, tương đương WHITE trong cờ vua
BLACK = False

# Định nghĩa các loại quân cờ
GENERAL = 1   # Tướng/Đại tướng
ADVISOR = 2   # Sĩ
ELEPHANT = 3  # Tượng
HORSE = 4     # Mã
CHARIOT = 5   # Xe
CANNON = 6    # Pháo
SOLDIER = 7   # Tốt/Binh


class XiangqiMove:
    """
    Representation of a move in Xiangqi.
    
    Attributes:
        from_pos: Starting position (row, col)
        to_pos: Destination position (row, col)
        piece_type: Type of the piece being moved
        piece_color: Color of the piece being moved (RED or BLACK)
    """
    def __init__(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], 
                 piece_type: int, piece_color: bool):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.piece_type = piece_type
        self.piece_color = piece_color
    
    def __eq__(self, other):
        if not isinstance(other, XiangqiMove):
            return False
        return (self.from_pos == other.from_pos and 
                self.to_pos == other.to_pos and 
                self.piece_type == other.piece_type and 
                self.piece_color == other.piece_color)
    
    def __hash__(self):
        return hash((self.from_pos, self.to_pos, self.piece_type, self.piece_color))
    
    def __str__(self):
        from_r, from_c = self.from_pos
        to_r, to_c = self.to_pos
        color = "Red" if self.piece_color == RED else "Black"
        piece_names = {
            GENERAL: "General", ADVISOR: "Advisor", ELEPHANT: "Elephant",
            HORSE: "Horse", CHARIOT: "Chariot", CANNON: "Cannon", SOLDIER: "Soldier"
        }
        piece = piece_names.get(self.piece_type, "Unknown")
        return f"{color} {piece} {from_r},{from_c} -> {to_r},{to_c}"


class XiangqiBoard(BoardBase[XiangqiMove]):
    """
    Xiangqi (Chinese chess) board implementation with standardized interface for RL environments.
    
    This class provides a standardized API for:
    - Board state representation
    - Move generation and validation
    - Move application
    - Game termination detection
    - Serialization for hashing states
    - Observation tensor generation
    """
    
    # Kích thước bàn cờ tướng: 9 cột x 10 hàng
    BOARD_WIDTH = 9
    BOARD_HEIGHT = 10
    
    # Số loại quân cờ khác nhau
    NUM_PIECE_TYPES = 7  # General, Advisor, Elephant, Horse, Chariot, Cannon, Soldier
    NUM_COLORS = 2       # RED và BLACK
    
    # Tổng số lớp cho tensor observation
    NUM_PLANES = NUM_PIECE_TYPES * NUM_COLORS  # 14 planes
    
    def __init__(self):
        """Initialize a Xiangqi board in the starting position."""
        # Khởi tạo bàn cờ trống
        # 0 = ô trống, số dương = quân đỏ, số âm = quân đen
        # Các giá trị tuyệt đối: 1=Tướng, 2=Sĩ, 3=Tượng, 4=Mã, 5=Xe, 6=Pháo, 7=Tốt
        self.board = np.zeros((self.BOARD_HEIGHT, self.BOARD_WIDTH), dtype=np.int8)
        
        # Khởi tạo vị trí ban đầu
        self._setup_initial_position()
        
        # Lưu trữ lịch sử nước đi
        self.move_history = []
        
        # Lượt đi (RED đi trước)
        self.current_player = RED
        
        # Kết quả trò chơi
        self.result = None
        
        # Bộ đếm nửa nước đi (cho luật hòa)
        self.halfmove_clock = 0
    
    def _setup_initial_position(self):
        """Set up the initial position of pieces on the board."""
        # Đặt quân đỏ (giá trị dương)
        # Hàng cuối (hàng 9, index 0)
        self.board[0, 0] = CHARIOT    # Xe
        self.board[0, 1] = HORSE      # Mã
        self.board[0, 2] = ELEPHANT   # Tượng
        self.board[0, 3] = ADVISOR    # Sĩ
        self.board[0, 4] = GENERAL    # Tướng
        self.board[0, 5] = ADVISOR    # Sĩ
        self.board[0, 6] = ELEPHANT   # Tượng
        self.board[0, 7] = HORSE      # Mã
        self.board[0, 8] = CHARIOT    # Xe
        
        # Pháo (hàng 7, index 2)
        self.board[2, 1] = CANNON
        self.board[2, 7] = CANNON
        
        # Tốt (hàng 6, index 3)
        self.board[3, 0] = SOLDIER
        self.board[3, 2] = SOLDIER
        self.board[3, 4] = SOLDIER
        self.board[3, 6] = SOLDIER
        self.board[3, 8] = SOLDIER
        
        # Đặt quân đen (giá trị âm)
        # Hàng đầu (hàng 0, index 9)
        self.board[9, 0] = -CHARIOT   # Xe
        self.board[9, 1] = -HORSE     # Mã
        self.board[9, 2] = -ELEPHANT  # Tượng
        self.board[9, 3] = -ADVISOR   # Sĩ
        self.board[9, 4] = -GENERAL   # Tướng
        self.board[9, 5] = -ADVISOR   # Sĩ
        self.board[9, 6] = -ELEPHANT  # Tượng
        self.board[9, 7] = -HORSE     # Mã
        self.board[9, 8] = -CHARIOT   # Xe
        
        # Pháo (hàng 2, index 7)
        self.board[7, 1] = -CANNON
        self.board[7, 7] = -CANNON
        
        # Tốt (hàng 3, index 6)
        self.board[6, 0] = -SOLDIER
        self.board[6, 2] = -SOLDIER
        self.board[6, 4] = -SOLDIER
        self.board[6, 6] = -SOLDIER
        self.board[6, 8] = -SOLDIER
    
    def reset(self) -> None:
        """Reset the board to initial position."""
        # Khởi tạo bàn cờ trống
        self.board = np.zeros((self.BOARD_HEIGHT, self.BOARD_WIDTH), dtype=np.int8)
        
        # Thiết lập vị trí ban đầu
        self._setup_initial_position()
        
        # Reset các biến trạng thái
        self.move_history = []
        self.current_player = RED
        self.result = None
        self.halfmove_clock = 0
    
    def get_legal_moves(self, player: Optional[bool] = None) -> List[XiangqiMove]:
        """
        Get all legal moves for the current position.
        
        Args:
            player: Optional player color (True for RED, False for BLACK)
                   If None, returns moves for current player
        
        Returns:
            List of legal XiangqiMove objects
        """
        # Xác định người chơi
        player_to_move = self.current_player if player is None else player
        
        # Nếu không phải lượt của người chơi được chỉ định, trả về danh sách rỗng
        if player is not None and player != self.current_player:
            return []
        
        # TODO: Triển khai thuật toán tạo nước đi hợp lệ cho cờ tướng
        # Đây là một phiên bản giả định đơn giản
        legal_moves = []
        
        # Sẽ triển khai chi tiết sau
        return legal_moves
    
    def apply_move(self, move: XiangqiMove) -> Tuple[float, bool]:
        """
        Apply a move to the board.
        
        Args:
            move: A XiangqiMove object to apply
            
        Returns:
            tuple of (reward, done)
            - reward is 0 for regular moves
            - reward is 1 for winning moves
            - reward is -1 for losing moves
            - reward is 0 for draw
            - done is True if the game is over
        """
        # TODO: Triển khai logic áp dụng nước đi
        # Đây là phiên bản giả định đơn giản
        
        # Lưu lại người chơi trước khi thực hiện nước đi
        player_before = self.current_player
        
        # Kiểm tra tính hợp lệ của nước đi
        if move not in self.get_legal_moves():
            raise ValueError(f"Illegal move: {move}")
        
        # Lấy thông tin vị trí
        from_row, from_col = move.from_pos
        to_row, to_col = move.to_pos
        
        # Thực hiện nước đi
        piece = self.board[from_row, from_col]
        captured_piece = self.board[to_row, to_col]
        
        # Di chuyển quân cờ
        self.board[to_row, to_col] = piece
        self.board[from_row, from_col] = 0
        
        # Lưu nước đi vào lịch sử
        self.move_history.append(move)
        
        # Chuyển lượt
        self.current_player = not self.current_player
        
        # Kiểm tra kết thúc trò chơi
        reward = 0.0
        done = False
        
        # TODO: Triển khai logic kiểm tra kết thúc trò chơi
        
        return reward, done
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        # TODO: Triển khai logic kiểm tra kết thúc trò chơi
        return False
    
    def to_observation(self) -> np.ndarray:
        """
        Convert the board state to a tensor observation.
        
        Returns:
            Numpy array with shape (NUM_PLANES, BOARD_HEIGHT, BOARD_WIDTH)
            where NUM_PLANES=14 (7 piece types x 2 colors)
        """
        # Khởi tạo tensor observation với toàn số 0
        observation = np.zeros((self.NUM_PLANES, self.BOARD_HEIGHT, self.BOARD_WIDTH), 
                              dtype=np.float32)
        
        # Điền thông tin vào tensor
        for r in range(self.BOARD_HEIGHT):
            for c in range(self.BOARD_WIDTH):
                piece = self.board[r, c]
                if piece != 0:
                    # Xác định loại quân và màu sắc
                    piece_type = abs(piece)
                    color = piece > 0  # True nếu là quân đỏ
                    
                    # Tính chỉ số lớp trong tensor
                    plane_idx = piece_type - 1 if color else piece_type + 6
                    
                    # Đặt giá trị vào tensor
                    observation[plane_idx, r, c] = 1.0
        
        return observation
    
    def get_state_hash(self) -> str:
        """
        Get a compact representation of the board state for hashing.
        
        Returns:
            String representation of the current board state
        """
        # Đơn giản hóa bằng cách chuyển bàn cờ thành chuỗi
        return str(self.board.tolist()) + f"|{self.current_player}"
    
    def get_result(self) -> Dict[str, Any]:
        """
        Get the game result if the game is over.
        
        Returns:
            Dictionary containing:
            - winner: 'red', 'black', or None for draw
            - termination: reason for game ending
            - moves: number of moves played
        """
        # Nếu trò chơi chưa kết thúc, trả về dict rỗng
        if not self.is_game_over():
            return {}
        
        # TODO: Triển khai logic xác định kết quả trò chơi
        
        # Đây là một phiên bản giả định
        return {
            'winner': None,
            'termination': 'UNKNOWN',
            'moves': len(self.move_history)
        }
    
    def __str__(self) -> str:
        """String representation of the board."""
        result = ""
        piece_symbols = {
            0: ".",
            GENERAL: "G", -GENERAL: "g",
            ADVISOR: "A", -ADVISOR: "a",
            ELEPHANT: "E", -ELEPHANT: "e",
            HORSE: "H", -HORSE: "h",
            CHARIOT: "R", -CHARIOT: "r",
            CANNON: "C", -CANNON: "c",
            SOLDIER: "S", -SOLDIER: "s"
        }
        
        # Thêm chỉ số cột ở đầu
        result += "  "
        for c in range(self.BOARD_WIDTH):
            result += f"{c} "
        result += "\n"
        
        # In bàn cờ với các ký hiệu
        for r in range(self.BOARD_HEIGHT - 1, -1, -1):  # In từ trên xuống dưới
            result += f"{r} "
            for c in range(self.BOARD_WIDTH):
                piece = self.board[r, c]
                result += piece_symbols.get(piece, "?") + " "
            result += "\n"
        
        # Thêm thông tin lượt đi
        result += f"\nTurn: {'Red' if self.current_player == RED else 'Black'}"
        
        return result


if __name__ == "__main__":
    # Mã thử nghiệm đơn giản
    board = XiangqiBoard()
    print("=== Xiangqi Board ===")
    print(board)
    
    # TODO: Thêm mã kiểm tra khi hoàn thiện các phương thức