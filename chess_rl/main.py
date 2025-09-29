"""
Main entry point for the chess_rl project.

This module provides basic functionality for testing the environment
and will be expanded in future implementations.
"""

import argparse
import random
import sys
from environments.chess_env import ChessEnv


def play_random_game(env, num_games=1, render=True, seed=None):
    """Play random games in the chess environment."""
    for game in range(num_games):
        print(f"\n===== Game {game + 1} =====")
        observation, info = env.reset(seed=seed)
        
        if render:
            env.render()
        
        done = False
        truncated = False
        step = 0
        
        while not (done or truncated):
            # Choose a random legal action
            legal_actions = info["legal_moves"]
            action = random.choice(legal_actions)
            
            # Take the action
            observation, reward, done, truncated, info = env.step(action)
            step += 1
            
            if render:
                print(f"\nStep {step}: {'White' if step % 2 == 1 else 'Black'} move")
                print(f"Action: {env.action_to_move(action)}")
                env.render()
            
            if done:
                result = info["result"]
                print("\nGame over!")
                print(f"Result: {result}")
                print(f"Total steps: {step}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Chess RL Environment")
    parser.add_argument(
        "--games", type=int, default=1, help="Number of games to play"
    )
    parser.add_argument(
        "--render", action="store_true", help="Render each step"
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Random seed"
    )
    
    args = parser.parse_args()
    
    # Create the environment
    env = ChessEnv()
    
    # Play random games
    play_random_game(
        env, 
        num_games=args.games, 
        render=args.render,
        seed=args.seed
    )


if __name__ == "__main__":
    main()