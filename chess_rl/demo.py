#!/usr/bin/env python3
"""
Unified demo runner for Chess and Xiangqi.

Usage (examples):
  python demo.py --game xiangqi --engine pyffish --moves 10 --auto
  python demo.py --game chess --moves 20 --render
"""

import argparse
import random

from environments.chess_env import ChessEnv
from environments.xiangqi_env import XiangqiEnv
from game.xiangqi_pyffish_board import XiangqiPyffishBoard


def run_chess_env(games: int, moves: int, seed: int | None, render: bool):
    env = ChessEnv()
    for g in range(games):
        obs, info = env.reset(seed=seed)
        if render:
            env.render()
        done = truncated = False
        step = 0
        while not (done or truncated) and step < moves:
            legal = info["legal_moves"]
            if not legal:
                break
            action = random.choice(legal)
            obs, reward, done, truncated, info = env.step(action)
            step += 1
            if render:
                print(f"Step {step}: {env.action_to_move(action)} | reward={reward}")
                env.render()
        print(f"Game {g+1} finished after {step} steps.")


def run_xiangqi_env(games: int, moves: int, seed: int | None, auto: bool):
    env = XiangqiEnv()
    for g in range(games):
        obs, info = env.reset(seed=seed)
        print("Initial board:")
        print(info.get("board_str", "<no board>") )
        done = truncated = False
        step = 0
        while not (done or truncated) and step < moves:
            legal_idx = info.get("legal_moves", [])
            if not legal_idx:
                print("No legal moves. Stopping.")
                break
            action = random.choice(range(len(legal_idx)))
            move = env.action_to_move(action)
            print(f"Step {step+1}: {move}")
            obs, reward, done, truncated, info = env.step(action)
            step += 1
            print(info.get("board_str", ""))
            if not auto:
                _ = input("Press Enter to continue...")
        print(f"Game {g+1} finished after {step} steps.")


def run_xiangqi_pyffish(moves: int, auto: bool):
    board = XiangqiPyffishBoard()
    print(board)
    for i in range(moves):
        legal = board.get_legal_moves()
        if not legal:
            print("No legal moves. Stopping.")
            break
        mv = random.choice(legal)
        print(f"Move {i+1}: {mv}")
        reward, done = board.apply_move(mv)
        print(board)
        if done:
            print("Game over.")
            break
        if not auto:
            _ = input("Press Enter to continue...")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--game", choices=["chess", "xiangqi"], default="xiangqi")
    p.add_argument("--engine", choices=["env", "pyffish"], default="pyffish")
    p.add_argument("--games", type=int, default=1)
    p.add_argument("--moves", type=int, default=10)
    p.add_argument("--seed", type=int, default=None)
    p.add_argument("--render", action="store_true")
    p.add_argument("--auto", action="store_true", help="Do not pause between moves")
    args = p.parse_args()

    if args.game == "chess":
        run_chess_env(args.games, args.moves, args.seed, args.render)
    else:
        if args.engine == "env":
            run_xiangqi_env(args.games, args.moves, args.seed, args.auto)
        else:
            run_xiangqi_pyffish(args.moves, args.auto)


if __name__ == "__main__":
    main()
