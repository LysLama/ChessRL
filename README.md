# ChessRL – Chess & Xiangqi Reinforcement Learning Platform

A modular research-oriented framework for experimenting with reinforcement learning (RL) on Chess and Xiangqi (Chinese Chess), plus an interactive GUI viewer.

> Full detailed documentation lives in `chess_rl/README.md`. This root file gives you a fast start.

## Quick Start

Clone and enter the project (already done if you're reading this here):

```bash
git clone https://github.com/LysLama/ChessRL.git
cd ChessRL
```

Create a virtual environment (recommended):

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # Linux/macOS
```

Install dependencies:

```bash
pip install -r chess_rl/requirements.txt
```

Run the GUI Match Viewer (Chess & Xiangqi random self-play):

```bash
cd chess_rl
python ui_match_viewer.py
```

Run a Xiangqi demo (PyFFish engine):

```bash
python demo.py --game xiangqi --engine pyffish --moves 20 --auto
```

Run a Chess demo:

```bash
python demo.py --game chess --moves 30 --render
```

## Features Overview

- Unified Board API for Chess & Xiangqi
- Multiple Xiangqi backends (simple + PyFFish)
- Observation tensor generation for RL
- Random / (planned) learning agents
- Tkinter GUI with:
	- Authentic Xiangqi board (intersections, river 楚河  漢界, palace diagonals, star points)
	- Colorized red vs black Xiangqi stones by default (toggle off for neutral)
	- Last-move highlighting & auto-play controls

## Project Layout (Simplified)

```
chess_rl/
	game/            # Board implementations
	environments/    # RL-style wrappers
	agents/          # (Planned / WIP agents)
	tests/           # Test suite
	ui_match_viewer.py
	demo.py          # Unified CLI demo
```

See the full breakdown in `chess_rl/README.md`.

## Testing

```bash
cd chess_rl
pytest -q
```

## Roadmap (Excerpt)

- Add learning agents (Q-learning, DQN, PPO)
- Add replay buffer + training scripts
- Add move list & human play mode in GUI

## License

MIT License – see `LICENSE`.

## Contributing

Issues and PRs welcome. For larger contributions, open a discussion first.

---
Happy experimenting!