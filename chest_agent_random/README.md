# Chess Reinforcement Learning Project

Dự án nghiên cứu và phát triển hệ thống học tăng cường (RL) cho cờ vua, tập trung vào tính module hóa, khả năng kiểm thử và tái tạo kết quả.

## 🚀 Roadmap tổng quan

Dự án được phân chia thành hai giai đoạn lớn:
1. **3 tuần triển khai codebase** - Xây dựng nền tảng ổn định
2. **5 tuần huấn luyện và thử nghiệm** - Thực hiện các thí nghiệm và đánh giá

## 🎯 3-Week Implementation Roadmap (Code & Infrastructure)

Mục tiêu: Xây dựng codebase module, được kiểm thử và tái tạo được kết quả với training loop hoàn chỉnh cho các thử nghiệm nhanh.

### Tuần 1 — Ổn định môi trường và core game 
**Focus**: Làm vững chắc các module game/ và environments/ để code RL có thể dựa vào giao diện có tính xác định.

**Tasks**:
1. **Tiêu chuẩn hóa Board API** (game/chess_board.py, chinese_chess_board.py)
   - Methods: reset(), get_legal_moves(player) -> List[Move], apply_move(move) -> reward, done, is_game_over(), to_observation()
   - Biểu diễn state: tensor số (e.g., shape (N_planes, H, W)) và một biểu diễn nhỏ gọn để hashing
2. **Đối tượng Move** (game/utils.py hoặc game/move.py)
   - Immutable dataclass chứa (from_sq, to_sq, promotion, metadata)
3. **Unit tests cho tính đúng đắn luật chơi** (nước đi cơ bản, bắt quân, phát hiện chiếu/chiếu hết)
4. **Triển khai base_env.py** với reset(), step(action), render(mode='human'|'rgb_array')
5. **Triển khai chess_env.py** (wrap board; chuyển đổi move index ↔ đối tượng Move)

**Deliverables**:
- Unit tests cho logic board (ít nhất 25 assertions covering các trường hợp biên)
- ChessEnv tương thích Gym với hành vi seed() có tính xác định

**Validation**:
- python -m pytest tests/test_board.py passes
- env.step(action) tạo ra cùng state khi cùng seed và chuỗi hành động

### Tuần 2 — Baseline agents + Utilities
**Focus**: Làm cho agents có tính plug-n-play và thêm các agents cơ bản cùng công cụ (replay buffer, logging).

**Tasks**:
1. **Hoàn thiện API agents/base_agent.py**
   - Methods: select_action(obs), train_step(batch) (optional), save(path), load(path)
2. **Triển khai Random agent và Q-learning (tabular)** có thể chạy end-to-end
3. **Replay buffer & training/replay_buffer** nếu sử dụng DQN sau này
4. **models/networks.py**: khung ConvNet/MLP nhỏ với forward(obs)
5. **Khung Trainer** (training/trainer.py) có thể:
   - Chấp nhận env, agent, config
   - Chạy episodes, ghi log rewards, checkpoint models mỗi N episodes
6. **Logging**: tích hợp utils/logger.py (console + CSV + TensorBoard tùy chọn)
7. **Script thử nghiệm cơ bản** (training/experiments.py) để chạy:
   - python -m training.experiments --agent random --env chess

**Deliverables**:
- Random và tabular Q agents chạy ~100 episodes
- Logs và checkpoints được lưu

**Validation**:
- Trainer chạy 100 episodes không crash; logs hiển thị reward mỗi episode

### Tuần 3 — Deep agents, tests, và CI
**Focus**: Triển khai DQN, tests, config, và tính tái tạo kết quả.

**Tasks**:
1. **DQN agent** (agents/dqn_agent.py)
   - Prioritized replay tùy chọn nhưng bắt đầu với uniform
   - Target network, epsilon-greedy schedule, gradient clipping
2. **Khung PPO** (agents/ppo_agent.py) — chỉ cần giao diện cho giai đoạn huấn luyện sau
3. **Model save/load** (models/model_utils.py) và cấu trúc models/saved_models
4. **Pipeline đánh giá** (training/evaluator.py) để tính win-rate, avg-reward, độ dài episode trung bình
5. **Unit tests** cho:
   - Tính đúng đắn của Replay buffer (các shapes khi sampling),
   - Shapes của DQN forward pass,
   - Trainer checkpointing
6. **CI hook** (GitHub Actions hoặc script local) để chạy tests khi push

**Deliverables**:
- DQN training chạy cho smoke-test ngắn (ví dụ 500 steps)
- CI chạy pytest và kiểm tra lint

**Validation**:
- pytest pass cho các tests mới
- DQN agent có thể học cấu trúc reward đơn giản (sanity check)

## � 5-Week Training Roadmap (Experiments, Tuning, Evaluation)

Mục tiêu: Tạo ra và so sánh các agents (Random, Q-Learning, DQN, PPO) và chọn model cuối cùng với báo cáo đánh giá.

### Tuần 0 (chuẩn bị) — Compute & baseline metrics (trùng với kết thúc tuần 3)
- Chuẩn bị compute: GPU local hoặc cloud (chỉ rõ loại GPU), ghi lại RAM, GPU memory
- Thiết lập metrics cơ sở: tỷ lệ thắng của random agent, hiệu suất Q-learning
- Xác định các trận đánh giá: 1000 episodes self-play và vs Random agent

### Tuần 4 (Training Week 1) — DQN baseline run
**Tasks**:
1. **Hyperparam sweep (coarse)**: learning rate [1e-4, 1e-3], batch size [32, 128], gamma [0.99]
2. **Chạy 3 DQN runs** (seeds khác nhau) cho ~100k environment steps (hoặc giới hạn thời gian)
3. **Theo dõi** reward mỗi episode, moving average, loss curves, và evaluation snapshots mỗi 5k steps

**Deliverables**:
- 3 DQN runs với logs, saved checkpoints tại các điểm
- Plots các learning curves

**Metrics**:
- Cải thiện moving average reward so với random; sample win rate vs random mỗi checkpoint

### Tuần 5 (Training Week 2) — DQN tuning & robustness
**Tasks**:
1. **Fine-tune hyperparameters tốt nhất** từ tuần 4
2. **Chạy dài hơn** (e.g., 300k steps) cho config tốt nhất
3. **Ablation**: target update frequency, replay buffer size, network depth

**Deliverables**:
- Một checkpoint "best DQN" + báo cáo ablation

**Metrics**:
- Win rate vs random và vs Q-learning baseline; stability across seeds

### Tuần 6 (Training Week 3) — PPO experiments
**Tasks**:
1. **Triển khai PPO** đầy đủ nếu khung chưa xong: actor-critic network, GAE, clip ratio
2. **Chạy PPO** với hyperparams ban đầu: learning rate 3e-4, batch size 2048 (hoặc điều chỉnh), epochs mỗi update 10
3. **So sánh PPO vs DQN** trên cùng ngân sách compute

**Deliverables**:
- PPO run logs và checkpoint tốt nhất

**Metrics**:
- Sample efficiency (hiệu suất mỗi training step), final win rates, stability

### Tuần 7 (Training Week 4) — Model comparison & ensemble/self-play
**Tasks**:
1. **Giải đấu head-to-head**: DQN vs PPO vs Q-learning vs Random (round-robin)
2. **Self-play training runs** nếu áp dụng được (train via self-play để cải thiện)
3. **Thu thập metrics**: xếp hạng kiểu Elo, tỷ lệ thắng head-to-head, độ dài episode trung bình, các dạng thất bại rõ ràng

**Deliverables**:
- Kết quả giải đấu, scripts để tái tạo các trận đấu

**Metrics**:
- Xếp hạng Elo, kiểm tra ý nghĩa thống kê (ví dụ bootstrap win-rate CI)

### Tuần 8 (Training Week 5) — Final evaluation, report & checkpoints
**Tasks**:
1. **Hoàn thiện model tốt nhất** và freeze hyperparams
2. **Đánh giá đầy đủ**: 10k games vs baselines, record logs và lưu final model
3. **Tạo báo cáo cuối cùng**:
   - Training curves, hyperparams, bảng đánh giá, các trường hợp thất bại, các bước tiếp theo được đề xuất
4. **Tổng kết**: thêm README để tái tạo thử nghiệm, model cards cho saved models

**Deliverables**:
- Final model files trong models/saved_models/, báo cáo đánh giá (Markdown + plots), reproduction script

**Metrics / Acceptance criteria**:
- Đạt threshold tỷ lệ thắng mong muốn vs random/baselines (được xác định dựa trên hiệu suất chấp nhận được)
- Kết quả tái tạo được (cùng seed -> đường cong tương tự) trong giới hạn độ biến thiên

## 🔍 Phân tích rủi ro & Giảm thiểu

| Rủi ro | Giảm thiểu |
|--------|------------|
| **Biểu diễn state lossy / không tương thích giữa các module** | Xác định format observation chuẩn trong game/board.py và thực thi trong tests |
| **Action space phát nổ (số lượng actions rời rạc lớn)** | Mã hóa moves gọn gàng (from,to,promote) và sử dụng action masking trong env để tránh illegal action gradient updates |
| **Training không ổn định / hiệu quả mẫu thấp** | Bắt đầu với các nhiệm vụ đơn giản / biến thể board nhỏ hơn (quy tắc đơn giản) để xác thực học; sử dụng curriculum/self-play |
| **Pygame/UI làm rối training và ngăn headless runs** | Làm cho rendering tùy chọn và không bao giờ gọi bên trong env.step() mặc định |
| **Thiếu compute (GPUs)** | Ưu tiên các agents nhẹ (tabular/Q) và test DQN trên networks nhỏ trước khi mở rộng |

## 🛠️ Đề xuất thực tế và config

- **Observation tensor**: shape=(N_planes=12, H=8, W=8) (one-hot per piece type per color), dtype float32
- **Action encoding**: map legal moves to indices mỗi step; trả về action_mask trong step() nếu có thể
- **Logging**: sử dụng tensorboardX hoặc torch.utils.tensorboard, cộng với backup CSV trong logs/
- **Checkpoint cadence**: mỗi 5k environment steps hoặc mỗi 100 episodes (tùy cái nào nhỏ hơn)

## 🗂️ Cấu trúc Project Mới

```
chess_rl/
├── game/                      # Game logic core
│   ├── chess_board.py         # Chess rules & board representation  
│   ├── chinese_chess_board.py # Optional variant
│   └── move.py                # Move object implementation
├── environments/              # RL environment wrappers
│   ├── base_env.py            # Base environment class
│   └── chess_env.py           # Chess-specific environment
├── agents/                    # Agent implementations
│   ├── base_agent.py          # Abstract base class
│   ├── random_agent.py        # Random baseline
│   ├── tabular_q_agent.py     # Tabular Q-learning
│   ├── dqn_agent.py           # Deep Q-Network
│   └── ppo_agent.py           # PPO implementation
├── models/                    # Neural network models
│   ├── networks.py            # Network architectures
│   ├── model_utils.py         # Save/load functionality
│   └── saved_models/          # Checkpoints directory
├── training/                  # Training infrastructure
│   ├── trainer.py             # Main training loop
│   ├── replay_buffer.py       # Experience replay
│   ├── experiments.py         # Experiment runner
│   └── evaluator.py           # Evaluation pipeline
├── utils/                     # Utility functions
│   ├── logger.py              # Logging utilities
│   └── visualization.py       # Plotting & visualization
├── tests/                     # Unit & integration tests
│   ├── test_board.py          # Board logic tests
│   ├── test_env.py            # Environment tests
│   └── test_agents.py         # Agent implementation tests
├── configs/                   # Configuration files
│   ├── default.yaml           # Default parameters
│   └── experiments/           # Experiment-specific configs
├── logs/                      # Training logs
├── scripts/                   # Utility scripts
│   └── generate_data.py       # Generate training data
├── notebooks/                 # Analysis notebooks
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

## ⚙️ Môi trường phát triển 

### Yêu cầu phần mềm
- Python 3.8+ 
- PyTorch 2.0+ (với CUDA support cho GPU training)
- Gym / Gymnasium
- pytest
- TensorBoard

### Cài đặt môi trường
```bash
# Tạo và kích hoạt conda environment
conda create -n chess-rl python=3.10
conda activate chess-rl

# Cài đặt dependencies
pip install -r requirements.txt

# Kiểm tra cài đặt 
python -c "import torch; print(f'PyTorch {torch.__version__}, CUDA available: {torch.cuda.is_available()}')"
python -m pytest tests/
```

### Phát triển và testing
```bash
# Chạy unit tests
python -m pytest tests/

# Chạy linting
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Chạy format code
black .
```

## 📚 Tham khảo và resources

### Tiếp cận codebase
1. Đọc qua môi trường trong environments/chess_env.py
2. Hiểu cách biểu diễn state và action trong game/chess_board.py
3. Xem các agents cơ bản trong agents/random_agent.py
4. Tìm hiểu training loop trong training/trainer.py

### Tài liệu học tăng cường
- "Reinforcement Learning: An Introduction" bởi Sutton & Barto
- PPO Paper: "Proximal Policy Optimization Algorithms" bởi Schulman et al.
- DQN Paper: "Human-level control through deep reinforcement learning" bởi Mnih et al.
- AlphaZero Paper: "Mastering Chess and Shogi by Self-Play with a General Reinforcement Learning Algorithm" bởi Silver et al.

---

## 📞 Liên hệ và Đóng góp

- **Issues**: Báo bugs và feature requests
- **Pull Requests**: Đóng góp code và improvements
- **Documentation**: Cải thiện docs và examples
- **Testing**: Thêm test cases và validation scenarios

## 📄 License

MIT License - Tự do sử dụng cho nghiên cứu và phát triển.

---

**Happy Chess AI Development! 🏁**