"""
Chess lessons module containing educational content about chess.
"""

# Dictionary of chess lessons organized by lesson ID
CHESS_LESSONS = {
    "chess-basics-001": {
        "id": "chess-basics-001",
        "title": "Introduction to Chess",
        "difficulty": "beginner",
        "topics": ["basics", "introduction"],
        "content": {
            "introduction": "Chess is a strategic board game played between two players on a checkered board with 64 squares. It has a rich history dating back to the 6th century in India.",
            "objective": "The objective of chess is to checkmate your opponent's king, which means the king is under attack (in check) and has no legal move to escape.",
            "board_setup": "The chess board consists of 8×8 grid of squares, alternating between light and dark colors. Players face each other with a light square in the bottom right corner."
        },
        "sections": [
            {
                "title": "The Chess Board",
                "content": "The chess board is an 8x8 grid of alternating light and dark squares. The board is set up so that each player has a light square in the bottom right corner. The vertical columns are called 'files' and labeled a through h from left to right. The horizontal rows are called 'ranks' and numbered 1 through 8 from bottom to top."
            },
            {
                "title": "Chess Pieces",
                "content": "Each player begins with 16 pieces: 1 king, 1 queen, 2 rooks, 2 bishops, 2 knights, and 8 pawns. Each piece moves differently, which determines its power and strategic value."
            },
            {
                "title": "Initial Setup",
                "content": "The back rank (row) for each player is set up with rooks on the corners, followed by knights, then bishops. The queen is placed on its matching color (white queen on light square, black queen on dark square), and the king occupies the remaining square."
            }
        ],
        "related_lessons": ["chess-pieces-001", "chess-rules-001"],
        "exercises": [
            {
                "type": "multiple_choice",
                "question": "How many squares are on a standard chess board?",
                "options": ["36", "49", "64", "81"],
                "correct_answer": "64"
            },
            {
                "type": "true_false",
                "question": "In the starting position, the queen is always placed on a square matching her color.",
                "correct_answer": True
            }
        ],
        "media": {
            "board_setup": "chess_initial_setup.png",
            "piece_movement": "chess_piece_movement.gif"
        },
        "created_at": "2025-07-15",
        "updated_at": "2025-09-01"
    },
    
    "chess-pieces-001": {
        "id": "chess-pieces-001",
        "title": "Chess Pieces and Movement",
        "difficulty": "beginner",
        "topics": ["basics", "pieces", "movement"],
        "content": {
            "introduction": "Each chess piece moves in a specific way and has a different relative value. Understanding how pieces move is fundamental to playing chess.",
            "overview": "There are six different types of chess pieces: King, Queen, Rook, Bishop, Knight, and Pawn. Each has unique movement patterns and strategic value."
        },
        "sections": [
            {
                "title": "The King",
                "content": "The king is the most important piece, but one of the weakest in terms of movement. The king can move one square in any direction: horizontally, vertically, or diagonally. The game ends when a king is checkmated."
            },
            {
                "title": "The Queen",
                "content": "The queen is the most powerful piece. It can move any number of squares along a rank, file, or diagonal, combining the powers of the rook and bishop."
            },
            {
                "title": "The Rook",
                "content": "Rooks move any number of squares along a rank or file. They are particularly powerful in the endgame and are valued at approximately 5 pawns."
            },
            {
                "title": "The Bishop",
                "content": "Bishops move any number of squares diagonally. Each player has two bishops, one moving on light squares and one on dark squares. A bishop is valued at approximately 3 pawns."
            },
            {
                "title": "The Knight",
                "content": "Knights move in an 'L' shape: two squares in one direction (horizontally or vertically) and then one square perpendicular to that direction. Knights are the only pieces that can jump over other pieces. A knight is valued at approximately 3 pawns."
            },
            {
                "title": "The Pawn",
                "content": "Pawns move forward one square, but capture diagonally. On their first move, they may advance two squares. When a pawn reaches the opposite end of the board, it is promoted to another piece (usually a queen). A pawn is valued at 1 pawn."
            }
        ],
        "related_lessons": ["chess-basics-001", "chess-rules-001"],
        "exercises": [
            {
                "type": "multiple_choice",
                "question": "Which piece can move in an L-shape?",
                "options": ["King", "Queen", "Rook", "Knight"],
                "correct_answer": "Knight"
            },
            {
                "type": "multiple_choice",
                "question": "How many squares can a pawn move forward on its first move?",
                "options": ["One", "Two", "Three", "Any number"],
                "correct_answer": "Two"
            }
        ],
        "media": {
            "king_movement": "king_movement.png",
            "queen_movement": "queen_movement.png",
            "rook_movement": "rook_movement.png",
            "bishop_movement": "bishop_movement.png",
            "knight_movement": "knight_movement.png",
            "pawn_movement": "pawn_movement.png"
        },
        "created_at": "2025-07-15",
        "updated_at": "2025-09-01"
    },
    
    "chess-rules-001": {
        "id": "chess-rules-001",
        "title": "Basic Chess Rules",
        "difficulty": "beginner",
        "topics": ["basics", "rules"],
        "content": {
            "introduction": "Chess is governed by a set of rules that determine how the game is played. Understanding these rules is essential for playing chess correctly.",
            "overview": "This lesson covers the basic rules of chess, including how to move pieces, capture, check, checkmate, and special moves like castling and en passant."
        },
        "sections": [
            {
                "title": "Turn Order and Movement",
                "content": "White always moves first, and then players alternate turns. On each turn, a player must move one piece (except for the special move called 'castling', where the king and a rook move simultaneously)."
            },
            {
                "title": "Capture",
                "content": "When a piece moves to a square occupied by an opponent's piece, the opponent's piece is captured and removed from the board. All pieces capture in the same way they move, except pawns, which capture diagonally forward."
            },
            {
                "title": "Check",
                "content": "A king is in check when it is under attack by one or more opponent pieces. If your king is in check, you must get out of check immediately by: moving the king, capturing the checking piece, or blocking the check."
            },
            {
                "title": "Checkmate",
                "content": "Checkmate occurs when a king is in check and there is no legal move to escape the check. When a player is checkmated, they lose the game."
            },
            {
                "title": "Castling",
                "content": "Castling is a special move involving the king and either rook. If neither the king nor the chosen rook has moved, the squares between them are empty, and the king is not in check, the king can move two squares toward the rook, and the rook moves to the square the king crossed."
            },
            {
                "title": "En Passant",
                "content": "En passant is a special pawn capture. If a pawn advances two squares from its starting position and lands beside an opponent's pawn, the opponent's pawn can capture it as if it had only moved one square. This capture must be made immediately after the two-square advance."
            },
            {
                "title": "Pawn Promotion",
                "content": "When a pawn reaches the opposite end of the board, it is promoted to another piece (queen, rook, bishop, or knight) of the same color."
            },
            {
                "title": "Draw",
                "content": "A game can end in a draw by stalemate (when a player has no legal moves but is not in check), threefold repetition, the 50-move rule, or by agreement between players."
            }
        ],
        "related_lessons": ["chess-basics-001", "chess-pieces-001", "chess-strategy-001"],
        "exercises": [
            {
                "type": "true_false",
                "question": "A player can move any number of pieces in a single turn.",
                "correct_answer": False
            },
            {
                "type": "multiple_choice",
                "question": "What is it called when the king is under attack?",
                "options": ["Checkmate", "Check", "Stalemate", "Draw"],
                "correct_answer": "Check"
            }
        ],
        "media": {
            "castling": "castling_example.gif",
            "en_passant": "en_passant_example.gif",
            "checkmate_example": "checkmate_example.png"
        },
        "created_at": "2025-07-16",
        "updated_at": "2025-09-02"
    },
    
    "chess-strategy-001": {
        "id": "chess-strategy-001",
        "title": "Basic Chess Strategy",
        "difficulty": "intermediate",
        "topics": ["strategy", "tactics"],
        "content": {
            "introduction": "Chess strategy involves long-term planning and positioning, while tactics are short-term maneuvers. Both are essential for playing good chess.",
            "overview": "This lesson covers fundamental strategic principles and common tactical patterns in chess."
        },
        "sections": [
            {
                "title": "Opening Principles",
                "content": "In the opening, aim to: control the center with pawns or pieces, develop your knights and bishops quickly, castle early to protect your king, and connect your rooks."
            },
            {
                "title": "Middlegame Concepts",
                "content": "During the middlegame, focus on piece activity, king safety, pawn structure, and creating or exploiting weaknesses in your opponent's position."
            },
            {
                "title": "Endgame Principles",
                "content": "In the endgame, activate your king, push passed pawns toward promotion, and understand basic checkmate patterns with reduced material."
            },
            {
                "title": "Common Tactics",
                "content": "Tactical motifs include: forks (attacking two pieces simultaneously), pins (immobilizing a piece because moving it would expose a more valuable piece), skewers (forcing a valuable piece to move, exposing a less valuable piece behind it), and discovered attacks (moving one piece to reveal an attack from another)."
            }
        ],
        "related_lessons": ["chess-rules-001", "chess-openings-001"],
        "exercises": [
            {
                "type": "multiple_choice",
                "question": "Which of these is NOT a fundamental opening principle?",
                "options": ["Control the center", "Develop knights and bishops", "Advance all pawns first", "Castle early"],
                "correct_answer": "Advance all pawns first"
            },
            {
                "type": "true_false",
                "question": "The king should remain passive throughout the entire game.",
                "correct_answer": False
            }
        ],
        "media": {
            "center_control": "center_control_example.png",
            "knight_fork": "knight_fork_example.png",
            "pin_example": "pin_example.png"
        },
        "created_at": "2025-07-20",
        "updated_at": "2025-09-05"
    }
}