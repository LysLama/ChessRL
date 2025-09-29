# Chess & Xiangqi Educational Content Module

This module provides educational content, game history tracking, and quiz functionality for chess and xiangqi (Chinese chess).

## Overview

The content module consists of three main components:

1. **Content Management**: Provides lessons and educational materials for chess and xiangqi.
2. **History Management**: Tracks and analyzes game histories for review and learning.
3. **Quiz System**: Creates and manages quizzes based on lesson content.

## Directory Structure

```
content/
├── __init__.py              # Module initialization
├── content_manager.py       # Main content management system
├── chess_lessons.py         # Chess educational content
├── xiangqi_lessons.py       # Xiangqi educational content
├── history.py               # Game history tracking and analysis
├── quiz.py                  # Quiz creation and management
├── custom/                  # Custom/user-created lessons
├── history_data/            # Stored game histories
└── quiz_data/               # Quiz definitions and session data
    ├── quizzes/             # Quiz definitions
    └── sessions/            # Quiz session records
```

## Usage

### Basic Usage

```python
from content import ContentSystem

# Initialize the content system
content_system = ContentSystem()

# Access components
content_manager = content_system.content_manager
history_manager = content_system.history_manager
quiz_manager = content_system.quiz_manager
```

### Working with Content

```python
# List all chess lessons
chess_lessons = content_system.content_manager.list_lessons(game_type='chess')

# Get a specific lesson
lesson = content_system.content_manager.get_lesson('chess-basics-001')

# Get a learning path for beginners
learning_path = content_system.get_learning_path('chess', 'beginner')
```

### Working with Game History

```python
# Add a game to history
content_system.add_game_to_history(
    game_id='game-001',
    game_type='chess',
    players={'white': 'Player1', 'black': 'Player2'},
    moves=['e4', 'e5', 'Nf3', 'Nc6', ...],
    result='1-0'
)

# Analyze a game
analysis = content_system.analyze_game('game-001')
```

### Working with Quizzes

```python
# Create a sample quiz
quiz_id = content_system.create_sample_quiz('chess')

# Create a quiz from a lesson
lesson_quiz_id = content_system.create_quiz_from_lesson('chess-strategy-001')

# Start a quiz session
session = content_system.quiz_manager.start_quiz_session(quiz_id, 'user_id')

# Answer a question
feedback = content_system.quiz_manager.answer_question(
    session.session_id,
    question_id,
    answer
)

# Complete the session
results = content_system.quiz_manager.complete_session(session.session_id)
```

## Demo

Run the demo script to see the content system in action:

```bash
python content_system_demo.py
```

## Custom Content

You can add custom lessons, which will be stored in the `custom/` directory:

```python
custom_lesson = {
    "id": "custom-chess-001",
    "title": "My Custom Chess Lesson",
    "difficulty": "intermediate",
    "topics": ["tactics", "endgame"],
    "content": {
        "introduction": "This is my custom lesson.",
        "sections": [...]
    },
    "exercises": [...]
}

content_system.content_manager.add_custom_lesson(custom_lesson)
```

## Dependencies

- Python 3.8+
- No external dependencies required