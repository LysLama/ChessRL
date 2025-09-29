# Chess and Xiangqi Reinforcement Learning Project

A comprehensive framework for reinforcement learning (RL) research with board games, focusing on Chess and Xiangqi (Chinese Chess). This project emphasizes modularity, testability, and reproducibility.

## 🚀 Introduction

This project implements environments and reinforcement learning algorithms for board games, with these key objectives:

- Building a modular and extensible platform
- Implementing and comparing various RL algorithms
- Creating high-performance agents with reproducible results
- Providing evaluation and analysis tools

## 🧩 Project Structure

```
chess_rl/
├── agents/              # Agent implementations (random, greedy, RL, etc.)
├── environments/        # Game environments compatible with RL algorithms
├── game/                # Board game implementations
│   ├── board_base.py    # Abstract base class for all board implementations
│   ├── simple_xiangqi_board.py  # Simple Xiangqi implementation
│   └── xiangqi_pyffish_board.py # Xiangqi using pyffish library
├── models/              # Neural network architectures for RL
├── tests/              # Test cases
│   └── test_pyffish_combined.py # Combined tests for pyffish API
├── training/            # Training scripts and utilities
├── utils/               # Helper functions and tools
├── xiangqi_demos.py     # Comprehensive demos for Xiangqi implementations
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## 🔧 Installation and Setup

### Requirements

- Python 3.8+
- PyTorch 2.0+
- Gymnasium
- python-chess (for Chess)
- pyffish (for Xiangqi)

### Setting Up the Environment

```bash
# Clone repository
git clone <repository-url>
cd chess_rl

# (Optional) Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA available: {torch.cuda.is_available()}')"
python -c "import pyffish; print(f'Pyffish version: {pyffish.version()}')"
```

## 🎮 Trying Out the Project

### Exploring Xiangqi Implementations

```bash
# Run the comprehensive demo comparing different Xiangqi implementations
python xiangqi_demos.py
```

### Testing Pyffish API

```bash
# Run combined pyffish tests for Xiangqi
python tests/test_pyffish_combined.py
```

### Running Board API Tests

```bash
# Test the Chess Board API
python test_board_api.py
```

### Running Unit Tests

```bash
# Run all tests
python -m pytest tests/

# Or run specific tests with details
python -m pytest tests/test_board.py -v
```

### Running Game Demos

You can run unified demos via `demo.py`:

```bash
# Xiangqi via PyFFish (pretty visualization)
python demo.py --game xiangqi --engine pyffish --moves 10 --auto

# Xiangqi via Env wrapper (Gym-like)
python demo.py --game xiangqi --engine env --moves 10 --auto

# Chess via Env
python demo.py --game chess --moves 20 --render
```

### GUI Match Viewer (Chess & Xiangqi)

An interactive Tkinter GUI that auto-plays random games and visualizes boards.

Launch:

```bash
python ui_match_viewer.py
```

Features:
- Game selector (Chess / Xiangqi)
- Random self-play with Start / Pause / Reset
- Speed slider (ms between moves)
- Require Checkmate toggle (restarts non-mate endings until a mate occurs)
- Authentic Xiangqi rendering: intersections, river (楚河  漢界), palace diagonals, star points, circular stones, last-move highlight ring
 - Default red vs black Xiangqi stones (neutral discs + colored text); toggle "Colorize" off to use neutral monochrome text

Notes:
- Random vs random Xiangqi or Chess can take a long time to reach checkmate; disable "Require Checkmate" if you just want a single finished game (may end in draw or stalemate).
- Window auto-resizes Xiangqi board with margins so pieces sit exactly on line intersections.

Planned Enhancements:
- Move list panel & manual step mode
- Click-to-move for human vs agent
- Screenshot embedding (add once captured)


## � Project Components

### Game Implementations

- **Chess**: Classic chess implementation using python-chess
- **Xiangqi**: Chinese Chess with multiple implementations:
  - Direct pyffish API usage
  - Wrapper implementation (XiangqiPyffishBoard)
  - Simplified implementation (SimpleXiangqiBoard)

### Board Base Class

All board implementations inherit from `BoardBase`, which provides a common interface:

```python
# Key methods in the BoardBase abstract class
def reset(self) -> None:
    """Reset the board to initial position."""
    
def get_legal_moves(self, player: Optional[bool] = None) -> List[Move]:
    """Get all legal moves for the current position."""
    
def apply_move(self, move: Move) -> Tuple[float, bool]:
    """Apply a move to the board. Returns (reward, done)."""
```

### Example Usage

#### Chess Board

```python
from game.chess_board import ChessBoard

# Initialize board
board = ChessBoard()

# Get legal moves
legal_moves = board.get_legal_moves()

# Make a move
move = legal_moves[0]  # Select first legal move
reward, done = board.apply_move(move)

# Convert board to observation tensor
observation = board.to_observation()  # Shape: (12, 8, 8)
```

#### Xiangqi with Pyffish

```python
import pyffish as sf

# Basic pyffish usage
variant = "xiangqi"
init_fen = sf.start_fen(variant)
legal_moves = sf.legal_moves(variant, init_fen, [])

# Make a move
if legal_moves:
    move = legal_moves[0]
    new_fen = sf.get_fen(variant, init_fen, [move])
```

#### Simple Xiangqi Board

```python
from game.simple_xiangqi_board import SimpleXiangqiBoard

# Initialize board
board = SimpleXiangqiBoard()

# Get legal moves
legal_moves = board.get_legal_moves()

# Make a move
if legal_moves:
    move = legal_moves[0]
    reward, done = board.make_move(move)
```

## 🧪 Testing

Run unit tests:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_pyffish_combined.py
```

## 📘 Development Roadmap

### Phase 1 (Completed)
- ✅ Standardize Board API
  - Implement methods: reset(), get_legal_moves(), apply_move(), is_game_over()
  - Create board tensor representation
  - Handle game termination conditions

### Xiangqi Extension (Completed)
- ✅ Create abstract BoardBase class
- ✅ Implement XiangqiPyffishBoard inheriting from BoardBase
- ✅ Create SimpleXiangqiBoard for simplified usage
- ✅ Create XiangqiMove for move representation
- ✅ Design observation tensor for Xiangqi (14, 10, 9)
- ✅ Implement testing infrastructure

### Phase 2 (In Progress)
- ✅ Improve XiangqiPyffishBoard with better visualization (unicode/coords via `to_pretty_string` and `__str__`)
- 🔄 Consolidate testing files (stabilized `test_pyffish.py` on Windows)
- ✅ Create unified demo scripts (`demo.py` CLI for chess/xiangqi)
- 🔄 Enhance documentation (this README updates in progress)

### Phase 3 (Planned)
- 🔜 Complete agents/base_agent.py API
- 🔜 Implement Random agent and tabular Q-learning
- 🔜 Create replay buffer utility
- 🔜 Design simple network architecture
- 🔜 Develop trainer pipeline

### Phase 4 (Future)
- � DQN implementation
- � PPO architecture
- � Model persistence utilities
- � Evaluation pipeline

## 📝 References

- [Gymnasium Documentation](https://gymnasium.farama.org/)
- [Python Chess Documentation](https://python-chess.readthedocs.io/en/latest/)
- [PyFFish Project](https://github.com/gbtami/pyffish)
- [PyTorch RL Tutorial](https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - See LICENSE file for details.