"""
Demo module for testing the chess and xiangqi implementations
"""

import argparse
import random
from game.game_factory import GameFactory


def play_random_game(env_type, num_games=1, render=True, seed=None):
    """Play random games in the specified environment."""
    # Create environment based on specified type
    env = GameFactory.create_environment(env_type)
    
    for game in range(num_games):
        print(f"\n===== {env_type.capitalize()} Game {game + 1} =====")
        observation, info = env.reset(seed=seed)
        
        if render:
            env.render()
        
        done = False
        truncated = False
        step = 0
        
        while not (done or truncated):
            # Choose a random legal action
            legal_actions = info["legal_moves"]
            if not legal_actions:
                print("No legal moves available. Game ends.")
                break
                
            action = random.choice(legal_actions)
            
            # Take the action
            observation, reward, done, truncated, info = env.step(action)
            step += 1
            
            if render:
                print(f"\nStep {step}: Move by {info['turn']}")
                try:
                    print(f"Action: {env.action_to_move(action)}")
                except:
                    print(f"Action index: {action}")
                env.render()
            
            if done:
                result = info.get("result", {})
                print("\nGame over!")
                print(f"Result: {result}")
                print(f"Total steps: {step}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Board Game Environments")
    parser.add_argument(
        "--game", type=str, choices=["chess", "xiangqi"], default="chess",
        help="Type of game to play"
    )
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
    
    # Play random games
    play_random_game(
        env_type=args.game,
        num_games=args.games, 
        render=args.render,
        seed=args.seed
    )


if __name__ == "__main__":
    main()