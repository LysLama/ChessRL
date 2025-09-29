"""
Content module initialization file.
This module contains educational content for chess and xiangqi,
as well as history tracking and quiz functionality.
"""

# Import content management components
from content.content_manager import ContentManager, ContentSystem
from content.chess_lessons import CHESS_LESSONS
from content.xiangqi_lessons import XIANGQI_LESSONS

# Import history components
try:
    from content.history import GameHistory, HistoryManager
except ImportError:
    GameHistory = None
    HistoryManager = None

# Import quiz components
try:
    from content.quiz import (
        Question, 
        MultipleChoiceQuestion,
        TrueFalseQuestion,
        BoardPositionQuestion,
        Quiz,
        QuizSession,
        QuizManager
    )
except ImportError:
    Question = None
    MultipleChoiceQuestion = None
    TrueFalseQuestion = None
    BoardPositionQuestion = None
    Quiz = None
    QuizSession = None
    QuizManager = None

__all__ = [
    # Content management
    'ContentManager',
    'ContentSystem',
    'CHESS_LESSONS',
    'XIANGQI_LESSONS',
    
    # History
    'GameHistory',
    'HistoryManager',
    
    # Quiz
    'Question',
    'MultipleChoiceQuestion',
    'TrueFalseQuestion',
    'BoardPositionQuestion',
    'Quiz',
    'QuizSession',
    'QuizManager'
]