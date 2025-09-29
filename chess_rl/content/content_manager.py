"""
Content Manager for accessing and organizing educational content.
"""

import json
import os
import importlib
from typing import Dict, List, Any, Optional, Union


class ContentManager:
    """
    Manages educational content for chess and xiangqi.
    Provides methods to access lessons, topics, and resources.
    """
    
    def __init__(self, content_dir: Optional[str] = None):
        """
        Initialize the content manager.
        
        Args:
            content_dir: Optional directory containing content files.
                         If None, uses the default content.
        """
        self.content_dir = content_dir
        self.chess_lessons = {}
        self.xiangqi_lessons = {}
        self.custom_lessons = {}
        
        # Load default content
        from content.chess_lessons import CHESS_LESSONS
        from content.xiangqi_lessons import XIANGQI_LESSONS
        
        self.chess_lessons = CHESS_LESSONS
        self.xiangqi_lessons = XIANGQI_LESSONS
        
        # If external content directory provided, load that too
        if content_dir:
            if os.path.exists(content_dir):
                self._load_external_content(content_dir)
            
            # Load custom lessons
            custom_dir = os.path.join(content_dir, 'custom')
            if os.path.exists(custom_dir):
                self._load_custom_lessons(custom_dir)
    
    def _load_external_content(self, content_dir: str) -> None:
        """Load content from external directory."""
        chess_path = os.path.join(content_dir, 'chess_lessons.json')
        xiangqi_path = os.path.join(content_dir, 'xiangqi_lessons.json')
        
        if os.path.exists(chess_path):
            try:
                with open(chess_path, 'r', encoding='utf-8') as f:
                    external_chess = json.load(f)
                    # Merge with default content
                    self._merge_content(self.chess_lessons, external_chess)
            except Exception as e:
                print(f"Error loading external chess content: {e}")
        
        if os.path.exists(xiangqi_path):
            try:
                with open(xiangqi_path, 'r', encoding='utf-8') as f:
                    external_xiangqi = json.load(f)
                    # Merge with default content
                    self._merge_content(self.xiangqi_lessons, external_xiangqi)
            except Exception as e:
                print(f"Error loading external xiangqi content: {e}")
    
    def _load_custom_lessons(self, custom_dir: str) -> None:
        """Load custom lessons from the content directory."""
        if not os.path.exists(custom_dir):
            os.makedirs(custom_dir, exist_ok=True)
            return
        
        for filename in os.listdir(custom_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(custom_dir, filename), 'r', encoding='utf-8') as f:
                        lesson = json.load(f)
                        if 'id' in lesson:
                            self.custom_lessons[lesson['id']] = lesson
                except Exception as e:
                    print(f"Error loading lesson {filename}: {e}")
    
    def _merge_content(self, base_content: Dict, new_content: Dict) -> None:
        """
        Merge new content into base content.
        Preserves existing content, adds new content, updates as needed.
        """
        for key, value in new_content.items():
            if key in base_content:
                if isinstance(value, dict) and isinstance(base_content[key], dict):
                    self._merge_content(base_content[key], value)
                else:
                    base_content[key] = value
            else:
                base_content[key] = value
    
    def get_lesson(self, lesson_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a lesson by ID.
        
        Args:
            lesson_id: The ID of the lesson to retrieve
            
        Returns:
            The lesson data if found, None otherwise
        """
        # Check custom lessons first
        if lesson_id in self.custom_lessons:
            return self.custom_lessons[lesson_id]
        
        # Check built-in lessons
        if lesson_id in self.chess_lessons:
            return self.chess_lessons[lesson_id]
        
        if lesson_id in self.xiangqi_lessons:
            return self.xiangqi_lessons[lesson_id]
        
        return None
    
    def get_chess_lesson(self, lesson_id: str) -> Dict:
        """
        Get a specific chess lesson by ID.
        
        Args:
            lesson_id: ID of the lesson to retrieve
            
        Returns:
            Dictionary containing lesson content
        """
        return self.chess_lessons.get(lesson_id, {"error": f"Lesson {lesson_id} not found"})
    
    def get_xiangqi_lesson(self, lesson_id: str) -> Dict:
        """
        Get a specific xiangqi lesson by ID.
        
        Args:
            lesson_id: ID of the lesson to retrieve
            
        Returns:
            Dictionary containing lesson content
        """
        return self.xiangqi_lessons.get(lesson_id, {"error": f"Lesson {lesson_id} not found"})
    
    def get_all_chess_lessons(self) -> List[Dict]:
        """
        Get all chess lessons.
        
        Returns:
            List of all chess lesson dictionaries
        """
        return list(self.chess_lessons.values())
    
    def get_all_xiangqi_lessons(self) -> List[Dict]:
        """
        Get all xiangqi lessons.
        
        Returns:
            List of all xiangqi lesson dictionaries
        """
        return list(self.xiangqi_lessons.values())
    
    def list_lessons(
        self,
        game_type: Optional[str] = None,
        difficulty: Optional[str] = None,
        topics: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        List lessons with optional filtering.
        
        Args:
            game_type: Filter by game type ('chess' or 'xiangqi')
            difficulty: Filter by difficulty level
            topics: Filter by topics
            
        Returns:
            List of lesson summaries
        """
        all_lessons = []
        
        # Collect lessons based on game type
        if game_type is None or game_type.lower() == 'chess':
            all_lessons.extend(self.chess_lessons.values())
        
        if game_type is None or game_type.lower() == 'xiangqi':
            all_lessons.extend(self.xiangqi_lessons.values())
        
        # Always include custom lessons
        all_lessons.extend(self.custom_lessons.values())
        
        # Apply filters
        filtered_lessons = []
        for lesson in all_lessons:
            if difficulty and lesson.get('difficulty') != difficulty:
                continue
            
            if topics:
                lesson_topics = lesson.get('topics', [])
                if not any(topic in lesson_topics for topic in topics):
                    continue
            
            # Create a summary with essential information
            summary = {
                'id': lesson['id'],
                'title': lesson['title'],
                'difficulty': lesson.get('difficulty', 'unknown'),
                'topics': lesson.get('topics', []),
                'game_type': self._determine_game_type(lesson['id'])
            }
            
            filtered_lessons.append(summary)
        
        return filtered_lessons
    
    def _determine_game_type(self, lesson_id: str) -> str:
        """
        Determine the game type based on the lesson ID.
        
        Args:
            lesson_id: The lesson ID
            
        Returns:
            'chess', 'xiangqi', or 'unknown'
        """
        if lesson_id in self.chess_lessons:
            return 'chess'
        elif lesson_id in self.xiangqi_lessons:
            return 'xiangqi'
        elif lesson_id in self.custom_lessons:
            return self.custom_lessons[lesson_id].get('game_type', 'unknown')
        else:
            return 'unknown'
    
    def save_content(self, output_dir: str) -> None:
        """
        Save content to files in the specified directory.
        
        Args:
            output_dir: Directory to save content files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        chess_path = os.path.join(output_dir, 'chess_lessons.json')
        with open(chess_path, 'w', encoding='utf-8') as f:
            json.dump(self.chess_lessons, f, indent=2, ensure_ascii=False)
        
        xiangqi_path = os.path.join(output_dir, 'xiangqi_lessons.json')
        with open(xiangqi_path, 'w', encoding='utf-8') as f:
            json.dump(self.xiangqi_lessons, f, indent=2, ensure_ascii=False)
        
        # Save custom lessons
        custom_dir = os.path.join(output_dir, 'custom')
        os.makedirs(custom_dir, exist_ok=True)
        
        for lesson_id, lesson in self.custom_lessons.items():
            lesson_path = os.path.join(custom_dir, f"{lesson_id}.json")
            with open(lesson_path, 'w', encoding='utf-8') as f:
                json.dump(lesson, f, indent=2, ensure_ascii=False)
        
        print(f"Content saved to {output_dir}")
    
    def get_lesson_by_topic(self, game_type: str, topic: str) -> List[Dict]:
        """
        Get lessons filtered by topic.
        
        Args:
            game_type: 'chess' or 'xiangqi'
            topic: Topic to filter by
            
        Returns:
            List of lesson dictionaries matching the topic
        """
        if game_type.lower() == 'chess':
            lessons = self.chess_lessons
        elif game_type.lower() == 'xiangqi':
            lessons = self.xiangqi_lessons
        else:
            return []
        
        return [
            lesson for lesson in lessons.values() 
            if topic.lower() in [t.lower() for t in lesson.get('topics', [])]
        ]
        
    def add_custom_lesson(self, lesson: Dict[str, Any]) -> str:
        """
        Add a custom lesson.
        
        Args:
            lesson: The lesson data
            
        Returns:
            The ID of the added lesson
            
        Raises:
            ValueError: If the lesson data is invalid
        """
        if 'id' not in lesson:
            raise ValueError("Lesson must have an ID")
        
        if 'title' not in lesson:
            raise ValueError("Lesson must have a title")
        
        if 'content' not in lesson or not isinstance(lesson['content'], dict):
            raise ValueError("Lesson must have content as a dictionary")
        
        lesson_id = lesson['id']
        self.custom_lessons[lesson_id] = lesson
        
        # Save the lesson to file if we have a content directory
        if self.content_dir:
            custom_dir = os.path.join(self.content_dir, 'custom')
            os.makedirs(custom_dir, exist_ok=True)
            
            with open(os.path.join(custom_dir, f"{lesson_id}.json"), 'w', encoding='utf-8') as f:
                json.dump(lesson, f, indent=2, ensure_ascii=False)
        
        return lesson_id
    
    def update_custom_lesson(self, lesson_id: str, lesson: Dict[str, Any]) -> bool:
        """
        Update a custom lesson.
        
        Args:
            lesson_id: The ID of the lesson to update
            lesson: The updated lesson data
            
        Returns:
            True if the lesson was updated, False otherwise
        """
        if lesson_id not in self.custom_lessons:
            return False
        
        # Ensure the ID in the lesson matches the given ID
        lesson['id'] = lesson_id
        
        self.custom_lessons[lesson_id] = lesson
        
        # Save the updated lesson if we have a content directory
        if self.content_dir:
            custom_dir = os.path.join(self.content_dir, 'custom')
            os.makedirs(custom_dir, exist_ok=True)
            
            with open(os.path.join(custom_dir, f"{lesson_id}.json"), 'w', encoding='utf-8') as f:
                json.dump(lesson, f, indent=2, ensure_ascii=False)
        
        return True
    
    def delete_custom_lesson(self, lesson_id: str) -> bool:
        """
        Delete a custom lesson.
        
        Args:
            lesson_id: The ID of the lesson to delete
            
        Returns:
            True if the lesson was deleted, False otherwise
        """
        if lesson_id not in self.custom_lessons:
            return False
        
        del self.custom_lessons[lesson_id]
        
        # Remove the lesson file if we have a content directory
        if self.content_dir:
            custom_dir = os.path.join(self.content_dir, 'custom')
            lesson_path = os.path.join(custom_dir, f"{lesson_id}.json")
            
            if os.path.exists(lesson_path):
                os.remove(lesson_path)
        
        return True
    
    def get_related_lessons(self, lesson_id: str) -> List[Dict[str, Any]]:
        """
        Get related lessons for a specific lesson.
        
        Args:
            lesson_id: The ID of the lesson
            
        Returns:
            List of related lesson summaries
        """
        lesson = self.get_lesson(lesson_id)
        if not lesson:
            return []
        
        related_ids = lesson.get('related_lessons', [])
        related_lessons = []
        
        for related_id in related_ids:
            related = self.get_lesson(related_id)
            if related:
                summary = {
                    'id': related['id'],
                    'title': related['title'],
                    'difficulty': related.get('difficulty', 'unknown'),
                    'topics': related.get('topics', []),
                    'game_type': self._determine_game_type(related['id'])
                }
                related_lessons.append(summary)
        
        return related_lessons
    
    def get_lesson_exercises(self, lesson_id: str) -> List[Dict[str, Any]]:
        """
        Get exercises for a specific lesson.
        
        Args:
            lesson_id: The ID of the lesson
            
        Returns:
            List of exercises
        """
        lesson = self.get_lesson(lesson_id)
        if not lesson:
            return []
        
        return lesson.get('exercises', [])


class ContentSystem:
    """
    Integrated content system that combines content, history, and quiz functionality.
    """
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Initialize the content system.
        
        Args:
            base_dir: Base directory for content storage
        """
        self.base_dir = base_dir or os.path.dirname(__file__)
        
        # Initialize components
        self.content_manager = ContentManager(os.path.join(self.base_dir))
        
        # Import and initialize other components dynamically to avoid circular imports
        try:
            from content.history import HistoryManager
            self.history_manager = HistoryManager(
                os.path.join(self.base_dir, 'history_data')
            )
        except ImportError:
            self.history_manager = None
        
        try:
            from content.quiz import QuizManager
            self.quiz_manager = QuizManager(
                os.path.join(self.base_dir, 'quiz_data')
            )
        except ImportError:
            self.quiz_manager = None
    
    def get_learning_path(
        self,
        game_type: str,
        difficulty: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate a recommended learning path for a specific game type and difficulty.
        
        Args:
            game_type: Type of game ('chess' or 'xiangqi')
            difficulty: Starting difficulty level
            
        Returns:
            List of lesson summaries in recommended order
        """
        # Get all lessons for the specified game type
        all_lessons = self.content_manager.list_lessons(game_type=game_type)
        
        # Define difficulty progression
        difficulty_order = ['beginner', 'intermediate', 'advanced', 'expert']
        
        # If no difficulty specified, start with beginner
        if not difficulty:
            difficulty = 'beginner'
        
        # Create a learning path
        learning_path = []
        
        try:
            current_difficulty_index = difficulty_order.index(difficulty)
        except ValueError:
            current_difficulty_index = 0
        
        # First, add lessons of the starting difficulty
        for lesson in all_lessons:
            if lesson.get('difficulty') == difficulty:
                learning_path.append(lesson)
        
        # Then, add lessons of higher difficulties
        for i in range(current_difficulty_index + 1, len(difficulty_order)):
            next_difficulty = difficulty_order[i]
            for lesson in all_lessons:
                if lesson.get('difficulty') == next_difficulty:
                    learning_path.append(lesson)
        
        return learning_path
    
    def create_quiz_from_lesson(self, lesson_id: str) -> Optional[str]:
        """
        Create a quiz based on a specific lesson.
        
        Args:
            lesson_id: The ID of the lesson
            
        Returns:
            The ID of the created quiz if successful, None otherwise
        """
        if not self.quiz_manager:
            return None
        
        lesson = self.content_manager.get_lesson(lesson_id)
        if not lesson:
            return None
        
        # Get exercises from the lesson
        exercises = lesson.get('exercises', [])
        if not exercises:
            return None
        
        # Import quiz module to access question classes
        try:
            from content.quiz import MultipleChoiceQuestion, TrueFalseQuestion
        except ImportError:
            return None
        
        # Create questions from exercises
        questions = []
        for i, exercise in enumerate(exercises):
            if exercise['type'] == 'multiple_choice':
                question = MultipleChoiceQuestion(
                    question_id=f"{lesson_id}-q{i+1}",
                    text=exercise['question'],
                    options=exercise['options'],
                    correct_option=exercise['correct_answer'],
                    difficulty=lesson.get('difficulty', 'beginner'),
                    category='lesson',
                    game_type=self.content_manager._determine_game_type(lesson_id),
                    explanation=exercise.get('explanation', '')
                )
                questions.append(question)
            
            elif exercise['type'] == 'true_false':
                question = TrueFalseQuestion(
                    question_id=f"{lesson_id}-q{i+1}",
                    text=exercise['question'],
                    correct_answer=exercise['correct_answer'],
                    difficulty=lesson.get('difficulty', 'beginner'),
                    category='lesson',
                    game_type=self.content_manager._determine_game_type(lesson_id),
                    explanation=exercise.get('explanation', '')
                )
                questions.append(question)
        
        if not questions:
            return None
        
        # Create a quiz
        quiz_id = self.quiz_manager.create_quiz(
            title=f"Quiz: {lesson['title']}",
            description=f"Quiz based on the lesson: {lesson['title']}",
            questions=questions,
            game_type=self.content_manager._determine_game_type(lesson_id),
            difficulty=lesson.get('difficulty', 'beginner')
        )
        
        return quiz_id
    
    def add_game_to_history(
        self,
        game_id: str,
        game_type: str,
        players: Dict[str, str],
        moves: List[str],
        result: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add a completed game to the history manager.
        
        Args:
            game_id: Unique identifier for the game
            game_type: Type of game ('chess' or 'xiangqi')
            players: Dictionary with player info (e.g., {'white': 'player1', 'black': 'player2'})
            moves: List of moves in standard notation
            result: Game result (e.g., '1-0', '0-1', '1/2-1/2')
            metadata: Additional game information
            
        Returns:
            True if the game was added successfully, False otherwise
        """
        if not self.history_manager:
            return False
        
        try:
            from content.history import GameHistory
            game = GameHistory(
                game_id=game_id,
                game_type=game_type,
                players=players,
                moves=moves,
                result=result,
                metadata=metadata
            )
            self.history_manager.add_game(game)
            return True
        except (ImportError, Exception):
            return False
    
    def create_sample_quiz(self, game_type: str) -> Optional[str]:
        """
        Create a sample quiz for the specified game type.
        
        Args:
            game_type: Type of game ('chess' or 'xiangqi')
            
        Returns:
            The ID of the created quiz if successful, None otherwise
        """
        if not self.quiz_manager:
            return None
        
        try:
            return self.quiz_manager.create_sample_quiz(game_type)
        except Exception:
            return None
    
    def analyze_game(self, game_id: str) -> Optional[Dict[str, Any]]:
        """
        Analyze a game from history.
        
        Args:
            game_id: The ID of the game to analyze
            
        Returns:
            Dictionary with analysis results if successful, None otherwise
        """
        if not self.history_manager:
            return None
        
        try:
            return self.history_manager.analyze_game_statistics(game_id)
        except Exception:
            return None