"""
Demo script showcasing the integrated content system with lessons, history, and quizzes.
"""

import os
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the content system
from content import ContentSystem


def demo_content_management(content_system):
    """Demonstrate content management functionality."""
    print("\n===== CONTENT MANAGEMENT DEMO =====\n")
    
    # List all chess lessons
    chess_lessons = content_system.content_manager.list_lessons(game_type='chess')
    print(f"Found {len(chess_lessons)} chess lessons:")
    for lesson in chess_lessons:
        print(f"  - {lesson['title']} (ID: {lesson['id']}, Difficulty: {lesson['difficulty']})")
    
    # Get a specific lesson
    lesson_id = 'chess-basics-001'
    lesson = content_system.content_manager.get_lesson(lesson_id)
    if lesson:
        print(f"\nDetails for lesson '{lesson['title']}':")
        print(f"  Introduction: {lesson['content']['introduction'][:100]}...")
        print(f"  Topics: {', '.join(lesson['topics'])}")
        
        # Get related lessons
        related = content_system.content_manager.get_related_lessons(lesson_id)
        if related:
            print(f"  Related lessons: {', '.join(l['title'] for l in related)}")
    
    # Get a learning path
    learning_path = content_system.get_learning_path('chess', 'beginner')
    print(f"\nLearning path for chess beginners:")
    for i, lesson in enumerate(learning_path):
        print(f"  {i+1}. {lesson['title']} ({lesson['difficulty']})")


def demo_history_management(content_system):
    """Demonstrate game history functionality."""
    if not content_system.history_manager:
        print("\n===== HISTORY MANAGEMENT DEMO =====\n")
        print("History manager not available.")
        return
    
    print("\n===== HISTORY MANAGEMENT DEMO =====\n")
    
    # Create and add a sample chess game
    game_id = f"demo-chess-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    players = {"white": "Player1", "black": "Player2"}
    moves = [
        "e4", "e5", 
        "Nf3", "Nc6", 
        "Bc4", "Nf6", 
        "Ng5", "d5", 
        "exd5", "Na5", 
        "Bb5+", "c6", 
        "dxc6", "bxc6", 
        "Be2", "h6", 
        "Nf3", "e4", 
        "Ne5", "Qd4", 
        "f4", "Bc5", 
        "Rf1", "Qxe5", 
        "fxe5", "Ng4", 
        "d3", "Nxe5", 
        "dxe4", "Bd7"
    ]
    result = "1-0"
    metadata = {
        "event": "Demo Game",
        "site": "Chess RL Demo",
        "opening": "Two Knights Defense"
    }
    
    success = content_system.add_game_to_history(
        game_id=game_id,
        game_type='chess',
        players=players,
        moves=moves,
        result=result,
        metadata=metadata
    )
    
    if success:
        print(f"Added chess game with ID: {game_id}")
        
        # Analyze the game
        analysis = content_system.analyze_game(game_id)
        if analysis:
            print("\nGame analysis:")
            print(f"  Move count: {analysis['move_count']}")
            print(f"  Duration: {analysis['duration']} plies")
            print(f"  Winner: {analysis['winner'] or 'Draw'}")
            
        # List all games
        games = content_system.history_manager.list_games()
        print(f"\nTotal games in history: {len(games)}")
    else:
        print("Failed to add game to history.")


def demo_quiz_management(content_system):
    """Demonstrate quiz functionality."""
    if not content_system.quiz_manager:
        print("\n===== QUIZ MANAGEMENT DEMO =====\n")
        print("Quiz manager not available.")
        return
    
    print("\n===== QUIZ MANAGEMENT DEMO =====\n")
    
    # Create a sample quiz
    chess_quiz_id = content_system.create_sample_quiz('chess')
    xiangqi_quiz_id = content_system.create_sample_quiz('xiangqi')
    
    if chess_quiz_id:
        print(f"Created chess quiz with ID: {chess_quiz_id}")
        
        # Get quiz details
        chess_quiz = content_system.quiz_manager.get_quiz(chess_quiz_id)
        if chess_quiz:
            print(f"  Title: {chess_quiz.title}")
            print(f"  Description: {chess_quiz.description}")
            print(f"  Questions: {chess_quiz.get_question_count()}")
            
            # Start a quiz session
            session = content_system.quiz_manager.start_quiz_session(chess_quiz_id, "demo_user")
            if session:
                print(f"\nStarted quiz session with ID: {session.session_id}")
                
                # Answer a question (first question)
                if chess_quiz.questions:
                    first_question = chess_quiz.questions[0]
                    
                    # Determine the correct answer for demo
                    answer = None
                    if hasattr(first_question, 'correct_option'):
                        if isinstance(first_question.correct_option, int):
                            answer = first_question.correct_option
                        else:
                            answer = first_question.correct_option
                    elif hasattr(first_question, 'correct_answer'):
                        answer = first_question.correct_answer
                    
                    if answer is not None:
                        feedback = content_system.quiz_manager.answer_question(
                            session.session_id, 
                            first_question.question_id, 
                            answer
                        )
                        
                        print(f"\nAnswered question: {first_question.text}")
                        print(f"  Result: {feedback['is_correct']}")
                        print(f"  Feedback: {feedback['feedback']}")
                
                # Complete the session
                results = content_system.quiz_manager.complete_session(session.session_id)
                if results:
                    print(f"\nCompleted quiz session:")
                    print(f"  Score: {results['score']:.1f}%")
                    print(f"  Correct answers: {results['correct_answers']} of {results['total_questions']}")
    
    if xiangqi_quiz_id:
        print(f"\nCreated xiangqi quiz with ID: {xiangqi_quiz_id}")
    
    # Create a quiz from a lesson
    lesson_id = 'chess-strategy-001'
    lesson_quiz_id = content_system.create_quiz_from_lesson(lesson_id)
    
    if lesson_quiz_id:
        print(f"\nCreated quiz from lesson {lesson_id} with ID: {lesson_quiz_id}")
        
        # List all quizzes
        quizzes = content_system.quiz_manager.list_quizzes()
        print(f"\nTotal quizzes available: {len(quizzes)}")


def main():
    """Run the demo of the integrated content system."""
    print("==================================================")
    print("       CHESS & XIANGQI CONTENT SYSTEM DEMO        ")
    print("==================================================")
    
    # Create content system with a temporary directory for data
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'temp_content'))
    os.makedirs(temp_dir, exist_ok=True)
    
    content_system = ContentSystem(temp_dir)
    
    # Run demos
    demo_content_management(content_system)
    demo_history_management(content_system)
    demo_quiz_management(content_system)
    
    print("\n==================================================")
    print("                    DEMO COMPLETE                 ")
    print("==================================================")


if __name__ == "__main__":
    main()