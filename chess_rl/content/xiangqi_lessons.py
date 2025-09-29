"""
Xiangqi lessons module containing educational content about Chinese Chess (Xiangqi).
"""

# Dictionary of xiangqi lessons organized by lesson ID
XIANGQI_LESSONS = {
    "xiangqi-basics-001": {
        "id": "xiangqi-basics-001",
        "title": "Introduction to Xiangqi",
        "difficulty": "beginner",
        "topics": ["basics", "introduction"],
        "content": {
            "introduction": "Xiangqi, also known as Chinese Chess, is a traditional board game that originated in China over 2,000 years ago. It's one of the most popular board games in the world, especially in East Asia.",
            "objective": "The objective of Xiangqi is to checkmate (capture) the opponent's General (similar to the King in Western chess).",
            "board_setup": "The Xiangqi board consists of a 9×10 grid with pieces placed on the intersections rather than within the squares. The board is divided by a river in the middle, separating the two sides."
        },
        "sections": [
            {
                "title": "The Xiangqi Board",
                "content": "The Xiangqi board consists of 9 files (columns) and 10 ranks (rows). Unlike Western chess, pieces are placed on the intersections of the lines rather than within squares. The board includes a 'river' across the middle and two 'palaces' (3×3 squares) where the Generals and Advisors must remain."
            },
            {
                "title": "Xiangqi Pieces",
                "content": "Each player starts with 16 pieces: 1 General, 2 Advisors, 2 Elephants, 2 Horses, 2 Chariots, 2 Cannons, and 5 Soldiers. Each piece has unique movement patterns and restrictions."
            },
            {
                "title": "Initial Setup",
                "content": "Pieces are arranged on the board with Chariots at the corners, followed by Horses and Elephants. The General is placed in the center of the palace, flanked by two Advisors. Cannons are placed in front of the Horses, and the five Soldiers are positioned across the board in front of other pieces."
            }
        ],
        "related_lessons": ["xiangqi-pieces-001", "xiangqi-rules-001"],
        "exercises": [
            {
                "type": "multiple_choice",
                "question": "How many total squares (intersections) are on a standard Xiangqi board?",
                "options": ["64", "81", "90", "100"],
                "correct_answer": "90"
            },
            {
                "type": "true_false",
                "question": "In Xiangqi, pieces are placed on the intersections of the lines.",
                "correct_answer": True
            }
        ],
        "media": {
            "board_setup": "xiangqi_initial_setup.png",
            "board_layout": "xiangqi_board_layout.png"
        },
        "created_at": "2025-07-15",
        "updated_at": "2025-09-01"
    },
    
    "xiangqi-pieces-001": {
        "id": "xiangqi-pieces-001",
        "title": "Xiangqi Pieces and Movement",
        "difficulty": "beginner",
        "topics": ["basics", "pieces", "movement"],
        "content": {
            "introduction": "Each Xiangqi piece has a unique way of moving and special restrictions. Understanding these movements is essential to playing the game.",
            "overview": "Xiangqi has seven types of pieces: General, Advisors, Elephants, Horses, Chariots, Cannons, and Soldiers. Each has distinct movement patterns and strategic value."
        },
        "sections": [
            {
                "title": "The General (将/帅)",
                "content": "The General moves one point horizontally or vertically but cannot leave the palace (3×3 grid at each end of the board). Generals cannot face each other directly on the same file without intervening pieces (the 'flying general' rule)."
            },
            {
                "title": "The Advisors (士/仕)",
                "content": "Advisors move one point diagonally and must remain within the palace. Each player has two Advisors, whose primary role is to protect the General."
            },
            {
                "title": "The Elephants (象/相)",
                "content": "Elephants move exactly two points diagonally and cannot cross the river. They can be blocked if there is a piece at the intervening point. Each player has two Elephants, primarily serving defensive roles."
            },
            {
                "title": "The Horses (马/傌)",
                "content": "Horses move one point orthogonally followed by one point diagonally outward (similar to the Knight in Western chess but can be blocked by a piece adjacent to it). Each player has two Horses."
            },
            {
                "title": "The Chariots (车/俥)",
                "content": "Chariots move any number of points horizontally or vertically, similar to the Rook in Western chess. They are the most powerful pieces in Xiangqi. Each player has two Chariots."
            },
            {
                "title": "The Cannons (炮/砲)",
                "content": "Cannons move like Chariots but must jump over exactly one piece (of either color) to capture. For non-capturing moves, they move like Chariots. Each player has two Cannons."
            },
            {
                "title": "The Soldiers (卒/兵)",
                "content": "Soldiers move one point forward before crossing the river. After crossing the river, they can also move one point horizontally. Unlike pawns in Western chess, they never promote and cannot move backward. Each player has five Soldiers."
            }
        ],
        "related_lessons": ["xiangqi-basics-001", "xiangqi-rules-001"],
        "exercises": [
            {
                "type": "multiple_choice",
                "question": "Which piece in Xiangqi must jump over exactly one piece to capture?",
                "options": ["General", "Horse", "Chariot", "Cannon"],
                "correct_answer": "Cannon"
            },
            {
                "type": "true_false",
                "question": "The Elephant in Xiangqi can cross the river.",
                "correct_answer": False
            }
        ],
        "media": {
            "general_movement": "xiangqi_general_movement.png",
            "advisor_movement": "xiangqi_advisor_movement.png",
            "elephant_movement": "xiangqi_elephant_movement.png",
            "horse_movement": "xiangqi_horse_movement.png",
            "chariot_movement": "xiangqi_chariot_movement.png",
            "cannon_movement": "xiangqi_cannon_movement.png",
            "soldier_movement": "xiangqi_soldier_movement.png"
        },
        "created_at": "2025-07-16",
        "updated_at": "2025-09-02"
    },
    
    "xiangqi-rules-001": {
        "id": "xiangqi-rules-001",
        "title": "Basic Xiangqi Rules",
        "difficulty": "beginner",
        "topics": ["basics", "rules"],
        "content": {
            "introduction": "Xiangqi has a unique set of rules that govern gameplay, some similar to Western chess and others distinctly different.",
            "overview": "This lesson covers the basic rules of Xiangqi, including turn order, movement restrictions, check, checkmate, and special rules like the flying general."
        },
        "sections": [
            {
                "title": "Turn Order and Movement",
                "content": "Red typically moves first, followed by Black, with players alternating turns. On each turn, a player must move one piece according to its movement rules."
            },
            {
                "title": "Capture",
                "content": "A piece captures an opponent's piece by moving to its position according to its normal movement rules (with the exception of the Cannon, which requires jumping over another piece to capture)."
            },
            {
                "title": "Check and Checkmate",
                "content": "When a General is under direct attack, it is in 'check' and the player must move to eliminate the threat. If there is no legal move to escape check, it is 'checkmate' and the game is lost."
            },
            {
                "title": "The Flying General Rule",
                "content": "The two Generals may not face each other along the same file with no pieces between them. This would constitute an illegal position."
            },
            {
                "title": "Perpetual Check and Chasing",
                "content": "Perpetually checking or chasing the same piece without progress is not allowed. After a certain number of repetitions (typically three), the player causing the repetition must make a different move."
            },
            {
                "title": "Stalemate and Draws",
                "content": "If a player has no legal moves but their General is not in check, the game is a draw. Games can also be drawn by agreement or if neither player has sufficient material to force a win."
            }
        ],
        "related_lessons": ["xiangqi-basics-001", "xiangqi-pieces-001", "xiangqi-strategy-001"],
        "exercises": [
            {
                "type": "true_false",
                "question": "In Xiangqi, the Generals can face each other directly on the same file if there are no pieces between them.",
                "correct_answer": False
            },
            {
                "type": "multiple_choice",
                "question": "What happens if a player has no legal moves but their General is not in check?",
                "options": ["The player loses", "The player wins", "The game is drawn", "The player must forfeit a piece"],
                "correct_answer": "The game is drawn"
            }
        ],
        "media": {
            "check_example": "xiangqi_check_example.png",
            "flying_general": "xiangqi_flying_general.png",
            "stalemate_example": "xiangqi_stalemate_example.png"
        },
        "created_at": "2025-07-17",
        "updated_at": "2025-09-03"
    },
    
    "xiangqi-strategy-001": {
        "id": "xiangqi-strategy-001",
        "title": "Basic Xiangqi Strategy",
        "difficulty": "intermediate",
        "topics": ["strategy", "tactics"],
        "content": {
            "introduction": "Xiangqi strategy involves understanding piece coordination, board control, and tactical patterns unique to the game.",
            "overview": "This lesson covers fundamental strategic principles and common tactical motifs in Xiangqi."
        },
        "sections": [
            {
                "title": "Opening Principles",
                "content": "In the opening, focus on developing Horses and Chariots, controlling central files, protecting your General with Advisors and Elephants, and preparing Cannon positions for attack."
            },
            {
                "title": "Middlegame Concepts",
                "content": "During the middlegame, coordinate your pieces for attack, maintain defensive structures around your General, advance Soldiers across the river to gain mobility, and look for tactical opportunities with Cannons and Chariots."
            },
            {
                "title": "Endgame Principles",
                "content": "In the endgame, activate your General when safe to do so, advance Soldiers toward promotion files, utilize the unique attacking patterns of Horses and Cannons, and understand basic checkmate patterns with reduced material."
            },
            {
                "title": "Common Tactics",
                "content": "Tactical motifs include: using the Cannon to pin pieces, creating double attacks with Horses, exploiting the 'flying general' rule to restrict opponent's General, and setting up discovered attacks with Chariots."
            },
            {
                "title": "River Crossing",
                "content": "Strategically advancing pieces across the river is crucial. Soldiers gain horizontal movement, while maintaining control of key crossing points denies mobility to the opponent."
            }
        ],
        "related_lessons": ["xiangqi-rules-001", "xiangqi-openings-001"],
        "exercises": [
            {
                "type": "multiple_choice",
                "question": "Why is it advantageous to move Soldiers across the river?",
                "options": ["They can capture more pieces", "They gain horizontal movement", "They can move backward", "They get promoted"],
                "correct_answer": "They gain horizontal movement"
            },
            {
                "type": "true_false",
                "question": "In Xiangqi, Cannons are typically more valuable in the endgame than in the opening.",
                "correct_answer": False
            }
        ],
        "media": {
            "central_control": "xiangqi_central_control.png",
            "cannon_tactics": "xiangqi_cannon_tactics.png",
            "horse_tactics": "xiangqi_horse_tactics.png"
        },
        "created_at": "2025-07-21",
        "updated_at": "2025-09-06"
    }
}