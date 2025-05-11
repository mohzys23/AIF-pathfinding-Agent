import time
from nethack_agent import main

def evaluate_agent(num_episodes=5, steps_per_episode=1000):
    """
    Run multiple episodes of the agent and collect statistics
    
    Args:
        num_episodes (int): Number of episodes to run
        steps_per_episode (int): Maximum steps per episode
    """
    print(f"\n=== Starting Agent Evaluation ===")
    print(f"Episodes: {num_episodes}")
    print(f"Steps per episode: {steps_per_episode}")
    
    total_items = 0
    total_steps = 0
    
    for episode in range(num_episodes):
        print(f"\n=== Episode {episode + 1}/{num_episodes} ===")
        start_time = time.time()
        
        # Run one episode
        main(max_steps=steps_per_episode)
        
        episode_time = time.time() - start_time
        print(f"\nEpisode {episode + 1} completed in {episode_time:.2f} seconds")
        
        # Add a small delay between episodes
        time.sleep(1)
    
    print("\n=== Evaluation Complete ===")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Evaluate NetHack Agent')
    parser.add_argument('--episodes', type=int, default=5,
                      help='number of episodes to run (default: 5)')
    parser.add_argument('--steps', type=int, default=1000,
                      help='maximum steps per episode (default: 1000)')
    
    args = parser.parse_args()
    evaluate_agent(args.episodes, args.steps) 