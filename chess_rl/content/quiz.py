"""
Quiz module for creating and managing quizzes related to chess and xiangqi.
"""

from typing import Dict, List, Any, Optional, Union
import json
import os
import random
import datetime
import uuid


class Question:
    """Base class for quiz questions."""
    
    def __init__(
        self, 
        question_id: str,
        text: str,
        difficulty: str,
        category: str,
        game_type: str,
        explanation: Optional[str] = None
    ):
        """
        Initialize a question.
        
        Args:
            question_id: Unique identifier for the question
            text: The question text
            difficulty: Difficulty level (e.g., 'beginner', 'intermediate', 'advanced')
            category: Category of the question (e.g., 'rules', 'strategy', 'history')
            game_type: Type of game ('chess' or 'xiangqi')
            explanation: Explanation of the correct answer
        """
        self.question_id = question_id
        self.text = text
        self.difficulty = difficulty
        self.category = category
        self.game_type = game_type
        self.explanation = explanation or ""
        self.type = "base"
    
    def is_correct(self, answer: Any) -> bool:
        """
        Check if the given answer is correct.
        
        Args:
            answer: The answer to check
            
        Returns:
            True if the answer is correct, False otherwise
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def get_feedback(self, answer: Any) -> str:
        """
        Get feedback for the given answer.
        
        Args:
            answer: The answer to provide feedback for
            
        Returns:
            Feedback text
        """
        if self.is_correct(answer):
            return "Correct! " + self.explanation
        else:
            return "Incorrect. " + self.explanation
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert question to dictionary."""
        return {
            'question_id': self.question_id,
            'text': self.text,
            'difficulty': self.difficulty,
            'category': self.category,
            'game_type': self.game_type,
            'explanation': self.explanation,
            'type': self.type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Question':
        """Create a Question object from a dictionary."""
        question_type = data.pop('type', 'base')
        
        if question_type == 'multiple_choice':
            return MultipleChoiceQuestion.from_dict(data)
        elif question_type == 'true_false':
            return TrueFalseQuestion.from_dict(data)
        elif question_type == 'board_position':
            return BoardPositionQuestion.from_dict(data)
        else:
            # Base question
            return cls(**data)


class MultipleChoiceQuestion(Question):
    """Multiple choice question implementation."""
    
    def __init__(
        self, 
        question_id: str,
        text: str,
        options: List[str],
        correct_option: Union[int, str],
        difficulty: str,
        category: str,
        game_type: str,
        explanation: Optional[str] = None
    ):
        """
        Initialize a multiple choice question.
        
        Args:
            question_id: Unique identifier for the question
            text: The question text
            options: List of answer options
            correct_option: The correct option (index or text)
            difficulty: Difficulty level
            category: Category of the question
            game_type: Type of game
            explanation: Explanation of the correct answer
        """
        super().__init__(question_id, text, difficulty, category, game_type, explanation)
        self.options = options
        
        # Handle correct_option as index or text
        if isinstance(correct_option, int):
            self.correct_option = correct_option
        else:
            self.correct_option = self.options.index(correct_option) if correct_option in self.options else 0
        
        self.type = "multiple_choice"
    
    def is_correct(self, answer: Union[int, str]) -> bool:
        """
        Check if the given answer is correct.
        
        Args:
            answer: The selected option index or text
            
        Returns:
            True if the answer is correct, False otherwise
        """
        if isinstance(answer, str) and answer in self.options:
            return self.options.index(answer) == self.correct_option
        elif isinstance(answer, int) and 0 <= answer < len(self.options):
            return answer == self.correct_option
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert multiple choice question to dictionary."""
        data = super().to_dict()
        data.update({
            'options': self.options,
            'correct_option': self.correct_option
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MultipleChoiceQuestion':
        """Create a MultipleChoiceQuestion object from a dictionary."""
        return cls(
            question_id=data['question_id'],
            text=data['text'],
            options=data['options'],
            correct_option=data['correct_option'],
            difficulty=data['difficulty'],
            category=data['category'],
            game_type=data['game_type'],
            explanation=data.get('explanation', '')
        )


class TrueFalseQuestion(Question):
    """True/False question implementation."""
    
    def __init__(
        self, 
        question_id: str,
        text: str,
        correct_answer: bool,
        difficulty: str,
        category: str,
        game_type: str,
        explanation: Optional[str] = None
    ):
        """
        Initialize a true/false question.
        
        Args:
            question_id: Unique identifier for the question
            text: The question text
            correct_answer: The correct answer (True or False)
            difficulty: Difficulty level
            category: Category of the question
            game_type: Type of game
            explanation: Explanation of the correct answer
        """
        super().__init__(question_id, text, difficulty, category, game_type, explanation)
        self.correct_answer = correct_answer
        self.type = "true_false"
    
    def is_correct(self, answer: Union[bool, str]) -> bool:
        """
        Check if the given answer is correct.
        
        Args:
            answer: The selected answer (bool or string 'true'/'false')
            
        Returns:
            True if the answer is correct, False otherwise
        """
        if isinstance(answer, str):
            answer_lower = answer.lower()
            if answer_lower in ('true', 't', 'yes', 'y', '1'):
                return self.correct_answer is True
            elif answer_lower in ('false', 'f', 'no', 'n', '0'):
                return self.correct_answer is False
            return False
        return answer == self.correct_answer
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert true/false question to dictionary."""
        data = super().to_dict()
        data.update({
            'correct_answer': self.correct_answer
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TrueFalseQuestion':
        """Create a TrueFalseQuestion object from a dictionary."""
        return cls(
            question_id=data['question_id'],
            text=data['text'],
            correct_answer=data['correct_answer'],
            difficulty=data['difficulty'],
            category=data['category'],
            game_type=data['game_type'],
            explanation=data.get('explanation', '')
        )


class BoardPositionQuestion(Question):
    """Question about a specific board position."""
    
    def __init__(
        self, 
        question_id: str,
        text: str,
        board_position: str,
        correct_moves: List[str],
        difficulty: str,
        category: str,
        game_type: str,
        explanation: Optional[str] = None
    ):
        """
        Initialize a board position question.
        
        Args:
            question_id: Unique identifier for the question
            text: The question text
            board_position: FEN or WXF notation of the board position
            correct_moves: List of correct moves in standard notation
            difficulty: Difficulty level
            category: Category of the question
            game_type: Type of game
            explanation: Explanation of the correct answer
        """
        super().__init__(question_id, text, difficulty, category, game_type, explanation)
        self.board_position = board_position
        self.correct_moves = correct_moves
        self.type = "board_position"
    
    def is_correct(self, answer: str) -> bool:
        """
        Check if the given move is correct.
        
        Args:
            answer: The move in standard notation
            
        Returns:
            True if the move is correct, False otherwise
        """
        return answer.strip() in self.correct_moves
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert board position question to dictionary."""
        data = super().to_dict()
        data.update({
            'board_position': self.board_position,
            'correct_moves': self.correct_moves
        })
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BoardPositionQuestion':
        """Create a BoardPositionQuestion object from a dictionary."""
        return cls(
            question_id=data['question_id'],
            text=data['text'],
            board_position=data['board_position'],
            correct_moves=data['correct_moves'],
            difficulty=data['difficulty'],
            category=data['category'],
            game_type=data['game_type'],
            explanation=data.get('explanation', '')
        )


class Quiz:
    """Class to represent a collection of questions as a quiz."""
    
    def __init__(
        self, 
        quiz_id: str,
        title: str,
        description: str,
        questions: List[Question],
        game_type: str,
        difficulty: Optional[str] = None,
        time_limit: Optional[int] = None
    ):
        """
        Initialize a quiz.
        
        Args:
            quiz_id: Unique identifier for the quiz
            title: The quiz title
            description: Description of the quiz
            questions: List of Question objects
            game_type: Type of game ('chess', 'xiangqi', or 'both')
            difficulty: Overall difficulty level
            time_limit: Time limit in seconds (if any)
        """
        self.quiz_id = quiz_id
        self.title = title
        self.description = description
        self.questions = questions
        self.game_type = game_type
        self.difficulty = difficulty
        self.time_limit = time_limit
    
    def add_question(self, question: Question) -> None:
        """
        Add a question to the quiz.
        
        Args:
            question: The Question object to add
        """
        self.questions.append(question)
    
    def remove_question(self, question_id: str) -> bool:
        """
        Remove a question from the quiz.
        
        Args:
            question_id: The ID of the question to remove
            
        Returns:
            True if the question was removed, False otherwise
        """
        for i, question in enumerate(self.questions):
            if question.question_id == question_id:
                self.questions.pop(i)
                return True
        return False
    
    def get_question_count(self) -> int:
        """Get the total number of questions in the quiz."""
        return len(self.questions)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert quiz to dictionary."""
        return {
            'quiz_id': self.quiz_id,
            'title': self.title,
            'description': self.description,
            'questions': [q.to_dict() for q in self.questions],
            'game_type': self.game_type,
            'difficulty': self.difficulty,
            'time_limit': self.time_limit
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Quiz':
        """Create a Quiz object from a dictionary."""
        questions = [Question.from_dict(q) for q in data['questions']]
        return cls(
            quiz_id=data['quiz_id'],
            title=data['title'],
            description=data['description'],
            questions=questions,
            game_type=data['game_type'],
            difficulty=data.get('difficulty'),
            time_limit=data.get('time_limit')
        )


class QuizSession:
    """Class to track a user's progress through a quiz."""
    
    def __init__(self, session_id: str, quiz: Quiz, user_id: str):
        """
        Initialize a quiz session.
        
        Args:
            session_id: Unique identifier for the session
            quiz: The Quiz object being attempted
            user_id: Identifier for the user taking the quiz
        """
        self.session_id = session_id
        self.quiz = quiz
        self.user_id = user_id
        self.answers: Dict[str, Any] = {}
        self.start_time = datetime.datetime.now()
        self.end_time = None
        self.score = 0
    
    def answer_question(self, question_id: str, answer: Any) -> bool:
        """
        Record an answer to a question.
        
        Args:
            question_id: The ID of the question being answered
            answer: The user's answer
            
        Returns:
            True if the answer is correct, False otherwise
        """
        for question in self.quiz.questions:
            if question.question_id == question_id:
                is_correct = question.is_correct(answer)
                self.answers[question_id] = {
                    'answer': answer,
                    'is_correct': is_correct,
                    'timestamp': datetime.datetime.now().isoformat()
                }
                return is_correct
        return False
    
    def complete(self) -> Dict[str, Any]:
        """
        Complete the quiz session and calculate the score.
        
        Returns:
            Dictionary with session results
        """
        self.end_time = datetime.datetime.now()
        
        # Calculate score
        correct_count = sum(1 for a in self.answers.values() if a['is_correct'])
        self.score = (correct_count / self.quiz.get_question_count()) * 100 if self.quiz.get_question_count() > 0 else 0
        
        return self.get_results()
    
    def get_results(self) -> Dict[str, Any]:
        """
        Get the session results.
        
        Returns:
            Dictionary with session results
        """
        return {
            'session_id': self.session_id,
            'quiz_id': self.quiz.quiz_id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'score': self.score,
            'total_questions': self.quiz.get_question_count(),
            'answered_questions': len(self.answers),
            'correct_answers': sum(1 for a in self.answers.values() if a['is_correct'])
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert quiz session to dictionary."""
        return {
            'session_id': self.session_id,
            'quiz': self.quiz.to_dict(),
            'user_id': self.user_id,
            'answers': self.answers,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'score': self.score
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'QuizSession':
        """Create a QuizSession object from a dictionary."""
        quiz = Quiz.from_dict(data['quiz'])
        session = cls(
            session_id=data['session_id'],
            quiz=quiz,
            user_id=data['user_id']
        )
        session.answers = data['answers']
        session.start_time = datetime.datetime.fromisoformat(data['start_time'])
        if data['end_time']:
            session.end_time = datetime.datetime.fromisoformat(data['end_time'])
        session.score = data['score']
        return session


class QuizManager:
    """Class to manage quizzes, including storage, retrieval, and session management."""
    
    def __init__(self, storage_dir: str = None):
        """
        Initialize the quiz manager.
        
        Args:
            storage_dir: Directory where quizzes and sessions are stored
        """
        self.storage_dir = storage_dir or os.path.join(os.path.dirname(__file__), 'quizzes')
        self.quiz_dir = os.path.join(self.storage_dir, 'quizzes')
        self.session_dir = os.path.join(self.storage_dir, 'sessions')
        
        os.makedirs(self.quiz_dir, exist_ok=True)
        os.makedirs(self.session_dir, exist_ok=True)
        
        # Cached quizzes
        self.quizzes: Dict[str, Quiz] = {}
        self.sessions: Dict[str, QuizSession] = {}
    
    def create_quiz(
        self, 
        title: str,
        description: str,
        questions: List[Question],
        game_type: str,
        difficulty: Optional[str] = None,
        time_limit: Optional[int] = None
    ) -> str:
        """
        Create a new quiz.
        
        Args:
            title: The quiz title
            description: Description of the quiz
            questions: List of Question objects
            game_type: Type of game ('chess', 'xiangqi', or 'both')
            difficulty: Overall difficulty level
            time_limit: Time limit in seconds (if any)
            
        Returns:
            The ID of the created quiz
        """
        quiz_id = str(uuid.uuid4())
        quiz = Quiz(
            quiz_id=quiz_id,
            title=title,
            description=description,
            questions=questions,
            game_type=game_type,
            difficulty=difficulty,
            time_limit=time_limit
        )
        
        self.quizzes[quiz_id] = quiz
        self._save_quiz(quiz)
        return quiz_id
    
    def get_quiz(self, quiz_id: str) -> Optional[Quiz]:
        """
        Get a quiz by ID.
        
        Args:
            quiz_id: The ID of the quiz to retrieve
            
        Returns:
            The Quiz object if found, None otherwise
        """
        # Check cache first
        if quiz_id in self.quizzes:
            return self.quizzes[quiz_id]
        
        # Try to load from storage
        filepath = os.path.join(self.quiz_dir, f"{quiz_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                quiz_data = json.load(f)
            quiz = Quiz.from_dict(quiz_data)
            self.quizzes[quiz_id] = quiz
            return quiz
        
        return None
    
    def update_quiz(self, quiz: Quiz) -> bool:
        """
        Update an existing quiz.
        
        Args:
            quiz: The updated Quiz object
            
        Returns:
            True if the quiz was updated, False otherwise
        """
        if quiz.quiz_id not in self.quizzes and not os.path.exists(os.path.join(self.quiz_dir, f"{quiz.quiz_id}.json")):
            return False
        
        self.quizzes[quiz.quiz_id] = quiz
        self._save_quiz(quiz)
        return True
    
    def delete_quiz(self, quiz_id: str) -> bool:
        """
        Delete a quiz by ID.
        
        Args:
            quiz_id: The ID of the quiz to delete
            
        Returns:
            True if the quiz was deleted, False otherwise
        """
        if quiz_id in self.quizzes:
            del self.quizzes[quiz_id]
        
        filepath = os.path.join(self.quiz_dir, f"{quiz_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
    
    def list_quizzes(self, game_type: Optional[str] = None, difficulty: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all quizzes, optionally filtered by type and difficulty.
        
        Args:
            game_type: If provided, only quizzes of this type will be returned
            difficulty: If provided, only quizzes of this difficulty will be returned
            
        Returns:
            List of quiz summary dictionaries
        """
        quiz_summaries = []
        for filename in os.listdir(self.quiz_dir):
            if filename.endswith('.json'):
                quiz_id = filename.replace('.json', '')
                quiz = self.get_quiz(quiz_id)
                if not quiz:
                    continue
                
                if (game_type is None or quiz.game_type == game_type or quiz.game_type == 'both') and \
                   (difficulty is None or quiz.difficulty == difficulty):
                    quiz_summaries.append({
                        'quiz_id': quiz.quiz_id,
                        'title': quiz.title,
                        'description': quiz.description,
                        'question_count': quiz.get_question_count(),
                        'game_type': quiz.game_type,
                        'difficulty': quiz.difficulty
                    })
        
        return quiz_summaries
    
    def start_quiz_session(self, quiz_id: str, user_id: str) -> Optional[QuizSession]:
        """
        Start a new quiz session.
        
        Args:
            quiz_id: The ID of the quiz to start
            user_id: Identifier for the user taking the quiz
            
        Returns:
            The QuizSession object if successful, None otherwise
        """
        quiz = self.get_quiz(quiz_id)
        if not quiz:
            return None
        
        session_id = str(uuid.uuid4())
        session = QuizSession(session_id, quiz, user_id)
        
        self.sessions[session_id] = session
        self._save_session(session)
        
        return session
    
    def get_session(self, session_id: str) -> Optional[QuizSession]:
        """
        Get a quiz session by ID.
        
        Args:
            session_id: The ID of the session to retrieve
            
        Returns:
            The QuizSession object if found, None otherwise
        """
        # Check cache first
        if session_id in self.sessions:
            return self.sessions[session_id]
        
        # Try to load from storage
        filepath = os.path.join(self.session_dir, f"{session_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                session_data = json.load(f)
            session = QuizSession.from_dict(session_data)
            self.sessions[session_id] = session
            return session
        
        return None
    
    def answer_question(self, session_id: str, question_id: str, answer: Any) -> Optional[Dict[str, Any]]:
        """
        Record an answer to a question in a session.
        
        Args:
            session_id: The ID of the session
            question_id: The ID of the question being answered
            answer: The user's answer
            
        Returns:
            Dictionary with answer feedback if successful, None otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        for question in session.quiz.questions:
            if question.question_id == question_id:
                is_correct = session.answer_question(question_id, answer)
                self._save_session(session)
                
                return {
                    'is_correct': is_correct,
                    'feedback': question.get_feedback(answer),
                    'session_id': session_id
                }
        
        return None
    
    def complete_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Complete a quiz session and calculate the results.
        
        Args:
            session_id: The ID of the session to complete
            
        Returns:
            Dictionary with session results if successful, None otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        results = session.complete()
        self._save_session(session)
        
        return results
    
    def get_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all quiz sessions for a specific user.
        
        Args:
            user_id: The ID of the user
            
        Returns:
            List of session summary dictionaries
        """
        session_summaries = []
        for filename in os.listdir(self.session_dir):
            if filename.endswith('.json'):
                session_id = filename.replace('.json', '')
                session = self.get_session(session_id)
                if session and session.user_id == user_id:
                    session_summaries.append({
                        'session_id': session.session_id,
                        'quiz_id': session.quiz.quiz_id,
                        'quiz_title': session.quiz.title,
                        'start_time': session.start_time.isoformat(),
                        'end_time': session.end_time.isoformat() if session.end_time else None,
                        'score': session.score,
                        'completed': session.end_time is not None
                    })
        
        return session_summaries
    
    def _save_quiz(self, quiz: Quiz) -> None:
        """
        Save a quiz to storage.
        
        Args:
            quiz: The Quiz object to save
        """
        filepath = os.path.join(self.quiz_dir, f"{quiz.quiz_id}.json")
        with open(filepath, 'w') as f:
            json.dump(quiz.to_dict(), f, indent=2)
    
    def _save_session(self, session: QuizSession) -> None:
        """
        Save a session to storage.
        
        Args:
            session: The QuizSession object to save
        """
        filepath = os.path.join(self.session_dir, f"{session.session_id}.json")
        with open(filepath, 'w') as f:
            json.dump(session.to_dict(), f, indent=2)
    
    def create_sample_quiz(self, game_type: str) -> str:
        """
        Create a sample quiz with predefined questions.
        
        Args:
            game_type: Type of game ('chess' or 'xiangqi')
            
        Returns:
            The ID of the created quiz
        """
        if game_type == 'chess':
            title = "Chess Basics Quiz"
            description = "Test your knowledge of basic chess rules and concepts."
            
            questions = [
                MultipleChoiceQuestion(
                    question_id=str(uuid.uuid4()),
                    text="Which piece can move in an L-shape?",
                    options=["King", "Queen", "Rook", "Knight"],
                    correct_option="Knight",
                    difficulty="beginner",
                    category="rules",
                    game_type="chess",
                    explanation="The Knight is the only chess piece that moves in an L-shape: two squares in one direction and then one square perpendicular to that direction."
                ),
                TrueFalseQuestion(
                    question_id=str(uuid.uuid4()),
                    text="A pawn can move two squares forward on its first move.",
                    correct_answer=True,
                    difficulty="beginner",
                    category="rules",
                    game_type="chess",
                    explanation="Pawns can move two squares forward from their starting position but only one square forward afterward."
                ),
                MultipleChoiceQuestion(
                    question_id=str(uuid.uuid4()),
                    text="What is it called when the king is under attack?",
                    options=["Checkmate", "Check", "Stalemate", "Draw"],
                    correct_option="Check",
                    difficulty="beginner",
                    category="rules",
                    game_type="chess",
                    explanation="When the king is under attack, it is in 'check'. The player must move to eliminate the threat."
                ),
                BoardPositionQuestion(
                    question_id=str(uuid.uuid4()),
                    text="White to move. What is the best move to checkmate Black?",
                    board_position="r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1",
                    correct_moves=["Qxf7#"],
                    difficulty="intermediate",
                    category="tactics",
                    game_type="chess",
                    explanation="Qxf7# is checkmate. The queen captures the f7 pawn with check, and the king has no legal moves."
                ),
                MultipleChoiceQuestion(
                    question_id=str(uuid.uuid4()),
                    text="How many squares are on a standard chess board?",
                    options=["36", "49", "64", "81"],
                    correct_option="64",
                    difficulty="beginner",
                    category="basics",
                    game_type="chess",
                    explanation="A standard chess board has 8×8 = 64 squares."
                )
            ]
        else:  # xiangqi
            title = "Xiangqi Basics Quiz"
            description = "Test your knowledge of basic Xiangqi (Chinese Chess) rules and concepts."
            
            questions = [
                MultipleChoiceQuestion(
                    question_id=str(uuid.uuid4()),
                    text="Which piece in Xiangqi must jump over exactly one piece to capture?",
                    options=["General", "Horse", "Chariot", "Cannon"],
                    correct_option="Cannon",
                    difficulty="beginner",
                    category="rules",
                    game_type="xiangqi",
                    explanation="The Cannon moves like a Chariot (Rook) but must jump over exactly one piece to capture."
                ),
                TrueFalseQuestion(
                    question_id=str(uuid.uuid4()),
                    text="The Elephant in Xiangqi can cross the river.",
                    correct_answer=False,
                    difficulty="beginner",
                    category="rules",
                    game_type="xiangqi",
                    explanation="The Elephant cannot cross the river, which limits its movement to its own side of the board."
                ),
                MultipleChoiceQuestion(
                    question_id=str(uuid.uuid4()),
                    text="How many total intersection points are on a standard Xiangqi board?",
                    options=["64", "81", "90", "100"],
                    correct_option="90",
                    difficulty="beginner",
                    category="basics",
                    game_type="xiangqi",
                    explanation="A Xiangqi board has 9 files and 10 ranks, making 9×10 = 90 intersection points."
                ),
                TrueFalseQuestion(
                    question_id=str(uuid.uuid4()),
                    text="In Xiangqi, the Generals can face each other directly on the same file if there are no pieces between them.",
                    correct_answer=False,
                    difficulty="beginner",
                    category="rules",
                    game_type="xiangqi",
                    explanation="This is the 'flying general' rule. The two Generals cannot face each other directly on the same file with no pieces between them."
                ),
                MultipleChoiceQuestion(
                    question_id=str(uuid.uuid4()),
                    text="What happens to a Soldier in Xiangqi when it crosses the river?",
                    options=["It can move backward", "It can move horizontally", "It gets promoted", "It moves faster"],
                    correct_option="It can move horizontally",
                    difficulty="beginner",
                    category="rules",
                    game_type="xiangqi",
                    explanation="After crossing the river, a Soldier gains the ability to move horizontally in addition to moving forward."
                )
            ]
        
        return self.create_quiz(
            title=title,
            description=description,
            questions=questions,
            game_type=game_type,
            difficulty="beginner",
            time_limit=300  # 5 minutes
        )