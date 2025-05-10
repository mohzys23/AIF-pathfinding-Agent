import gymnasium as gym
import numpy as np
import random
from nle import nethack
from nle.nethack import actions as nh_actions
from collections import deque
import time
import helper_functions as helpers
from constant import ITEM_NAMES, ACTION_NAMES, NORTH, SOUTH, EAST, WEST, DOWN
import algorithms as alg





# Configuration
DELAY_BETWEEN_STEPS = 0.1  # Seconds to wait between steps for better visualization


def main(max_steps=None):
    # Create environment with terminal rendering mode
    print("\n🎮 Creating NetHack environment with terminal interface...\n")
    env = gym.make("NetHackScore-v0", render_mode="ansi")
    obs, _ = env.reset()
    seen_map = np.zeros_like(obs["chars"], dtype=bool)
    
    # Keep track of visited positions to avoid getting stuck
    visited_positions = {}

    # Game state tracking
    items_collected = 0
    descended = False
    step = 0
    terminated = False
    truncated = False
    last_pos = None
    stuck_count = 0
    last_action = None
    action_history = []  # Keep track of recent actions to break loops
    random_exploration_steps = 0
    last_level = 1
    died = False
    last_hp = obs["blstats"][10]  # Initial HP
    success = False
    
    try:
        print("\n========== STARTING NEW AGENT RUN ==========\n")
        print(f"Running {'until success or death (no step limit)' if max_steps is None else f'with max {max_steps} steps'}")
        
        # Run until termination, success, or max_steps (if specified)
        while not (terminated or truncated or success or died) and (max_steps is None or step < max_steps):
            # Display the current game state in the terminal
            try:
                ansi_render = env.render()
                print("\n" + ansi_render + "\n")
            except Exception as e:
                print(f"Note: Could not render the game state: {e}")
            
            step += 1
            pos = helpers.get_agent_position(obs)
            x, y = pos
            
            # Update visit count for current position
            visited_positions[pos] = visited_positions.get(pos, 0) + 1
            
            # Update seen map with a 3x3 field of view
            for i in range(max(0, y-3), min(seen_map.shape[0], y+4)):
                for j in range(max(0, x-3), min(seen_map.shape[1], x+4)):
                    seen_map[i][j] = True
                    
            # Get the current level
            current_level = obs['blstats'][12]
            
            # Check game message for important information
            message = helpers.parse_message(obs)
            if message:
                print(f"Game message: {message}")
                
                # Check for death or important events in message
                if "You die" in message or "You were killed" in message:
                    print("⚰️ AGENT DIED!")
                    died = True
                    break
            
            # Check HP to detect damage/death
            current_hp = obs["blstats"][10]
            if current_hp < last_hp:
                print(f"❗ HP decreased from {last_hp} to {current_hp}!")
            last_hp = current_hp
            
            # Check if HP is zero (agent died)
            if current_hp <= 0:
                print("⚰️ AGENT DIED! (HP reached 0)")
                died = True
                break
            
            # Check if level changed
            if current_level != last_level:
                if current_level > last_level:
                    print(f"🔽 DESCENDED from level {last_level} to level {current_level}")
                    descended = True
                    visited_positions = {}  # Reset visit counts for the new level
                    seen_map = np.zeros_like(obs["chars"], dtype=bool)
                else:
                    print(f"🔼 LEVEL DECREASED from {last_level} to {current_level}! This might indicate death or teleport.")
                    
                last_level = current_level
            
            # Print character's status
            hp = obs["blstats"][10]  # Current HP
            max_hp = obs["blstats"][11]  # Max HP
            hunger_status = obs["blstats"][21]  # Hunger state: 1=Satiated, 2=Normal, 3=Hungry, 4=Weak, 5=Fainting
            hunger_text = {1: "Satiated", 2: "Normal", 3: "Hungry", 4: "Weak", 5: "Fainting"}.get(hunger_status, "Unknown")
            
            print(f"\nSTATUS - HP: {hp}/{max_hp} | Hunger: {hunger_text} | Level: {current_level} | Items: {items_collected}")
            
            # Check if we're on an item
            if helpers.is_item(obs["chars"][y][x]):
                item_type = ITEM_NAMES.get(obs["chars"][y][x], "unknown item")
                action = nh_actions.Command.EAT if obs["chars"][y][x] == ord('%') else nh_actions.Command.PICKUP
                print(f"🎒 Found {item_type} at {pos}. Picking up...")
            else:
                # If we're in random exploration mode, continue with it
                if random_exploration_steps > 0:
                    random_exploration_steps -= 1
                    action = random.choice([NORTH, SOUTH, EAST, WEST])
                    print(f"🔄 Random exploration step {5-random_exploration_steps}/5...")
                # If we have enough items and have descended, we're done
                elif items_collected >= 5 and descended:
                    print(f"\n🎉 SUCCESS: Collected {items_collected} items and reached level {current_level}!\n")
                    success = True
                    break
                # If we have enough items, try to find stairs
                elif items_collected >= 3 and not descended:
                    stairs_pos = helpers.find_stairs(obs["chars"])
                    
                    if stairs_pos and pos == stairs_pos:
                        action = DOWN
                        print(f"⬇️ Found stairs! Going down...")
                    elif stairs_pos:
                        # Find path to stairs
                        path = alg.find_path_bfs(pos, stairs_pos, obs["chars"], obs["glyphs"], visited_positions)
                        if path and len(path) > 0:
                            action = path[0]
                            print(f"🧭 Moving toward stairs: {stairs_pos}")
                        else:
                            # No clear path, explore
                            item_pos, item_path = alg.find_nearest_item(pos, obs["chars"], obs["glyphs"], visited_positions)
                            if item_pos and len(item_path) > 0:
                                item_type = ITEM_NAMES.get(obs["chars"][item_pos[1]][item_pos[0]], "unknown item")
                                action = item_path[0]
                                print(f"🏃 Moving toward {item_type} at {item_pos}")
                            else:
                                # Try to find unexplored areas
                                unexplored_pos, unexplored_path = alg.find_unexplored_dfs(pos, seen_map, obs["chars"], obs["glyphs"], visited_positions)
                                if unexplored_pos and len(unexplored_path) > 0:
                                    action = unexplored_path[0]
                                    print(f"🔍 Exploring: {unexplored_pos}")
                                else:
                                    # Try to find least visited position
                                    least_visited_pos, least_visited_path = helpers.get_least_visited_position(pos, obs["chars"], obs["glyphs"], visited_positions)
                                    if least_visited_pos and len(least_visited_path) > 0:
                                        action = least_visited_path[0]
                                        print(f"👣 Moving to least visited: {least_visited_pos}")
                                    else:
                                        # Random movement as a last resort
                                        action = random.choice([NORTH, SOUTH, EAST, WEST])
                                        print(f"🎲 Moving randomly")
                    else:
                        # No stairs found, look for items or explore
                        item_pos, item_path = alg.find_nearest_item(pos, obs["chars"], obs["glyphs"], visited_positions)
                        if item_pos and len(item_path) > 0:
                            item_type = ITEM_NAMES.get(obs["chars"][item_pos[1]][item_pos[0]], "unknown item")
                            action = item_path[0]
                            print(f"🏃 Moving toward {item_type} at {item_pos}")
                        else:
                            # Try to find unexplored areas
                            unexplored_pos, unexplored_path = alg.find_unexplored_dfs(pos, seen_map, obs["chars"], obs["glyphs"], visited_positions)
                            if unexplored_pos and len(unexplored_path) > 0:
                                action = unexplored_path[0]
                                print(f"🔍 Exploring: {unexplored_pos}")
                            else:
                                # Try to find least visited position
                                least_visited_pos, least_visited_path = helpers.get_least_visited_position(pos, obs["chars"], obs["glyphs"], visited_positions)
                                if least_visited_pos and len(least_visited_path) > 0:
                                    action = least_visited_path[0]
                                    print(f"👣 Moving to least visited: {least_visited_pos}")
                                else:
                                    # Random movement as a last resort
                                    action = random.choice([NORTH, SOUTH, EAST, WEST])
                                    print(f"🎲 Moving randomly")
                else:
                    # Look for items to collect
                    item_pos, item_path = alg.find_nearest_item(pos, obs["chars"], obs["glyphs"], visited_positions)
                    if item_pos and len(item_path) > 0:
                        item_type = ITEM_NAMES.get(obs["chars"][item_pos[1]][item_pos[0]], "unknown item")
                        action = item_path[0]
                        print(f"🏃 Moving toward {item_type} at {item_pos}")
                    else:
                        # Try to find unexplored areas
                        unexplored_pos, unexplored_path = alg.find_unexplored_dfs(pos, seen_map, obs["chars"], obs["glyphs"], visited_positions)
                        if unexplored_pos and len(unexplored_path) > 0:
                            action = unexplored_path[0]
                            print(f"🔍 Exploring: {unexplored_pos}")
                        else:
                            # Try to find least visited position
                            least_visited_pos, least_visited_path = helpers.get_least_visited_position(pos, obs["chars"], obs["glyphs"], visited_positions)
                            if least_visited_pos and len(least_visited_path) > 0:
                                action = least_visited_path[0]
                                print(f"👣 Moving to least visited: {least_visited_pos}")
                            else:
                                # Random movement as a last resort
                                action = random.choice([NORTH, SOUTH, EAST, WEST])
                                print(f"🎲 Moving randomly")
            
            # Check if we're stuck in the same position
            if pos == last_pos:
                stuck_count += 1
                if stuck_count > 3:
                    # Start a random exploration phase
                    directions = [NORTH, SOUTH, EAST, WEST]
                    if last_action in directions:
                        try:
                            directions.remove(last_action)
                        except ValueError:
                            # If last_action is not in directions, just continue
                            pass
                    action = random.choice(directions)
                    random_exploration_steps = 5  # Explore randomly for 5 steps
                    stuck_count = 0
                    print(f"⚠️ Stuck! Starting random exploration with: {ACTION_NAMES.get(action)}")
            else:
                stuck_count = 0
            
            # Check for action loops
            action_history.append(action)
            if len(action_history) > 10:
                action_history.pop(0)
                
                # Check if we're in a repetitive pattern (e.g., NSNSNS...)
                if len(action_history) >= 6:
                    if (action_history[-6:] == [NORTH, SOUTH, NORTH, SOUTH, NORTH, SOUTH] or
                        action_history[-6:] == [SOUTH, NORTH, SOUTH, NORTH, SOUTH, NORTH] or
                        action_history[-6:] == [EAST, WEST, EAST, WEST, EAST, WEST] or
                        action_history[-6:] == [WEST, EAST, WEST, EAST, WEST, EAST]):
                        
                        # Break the pattern with a random perpendicular direction
                        if action in [NORTH, SOUTH]:
                            action = random.choice([EAST, WEST])
                        else:
                            action = random.choice([NORTH, SOUTH])
                        
                        # Start random exploration
                        random_exploration_steps = 5
                        print(f"🔄 Breaking oscillation pattern! New direction: {ACTION_NAMES.get(action)}")
                        action_history = [action]  # Reset the history
            
            # Update position and action history
            last_pos = pos
            last_action = action
            
            # Take action
            obs, reward, terminated, truncated, info = env.step(action)
            
            # Print status
            action_name = ACTION_NAMES.get(action, str(action))
            print(f"Step: {step}, Items: {items_collected}, Level: {obs['blstats'][12]}, Action: {action_name}")
            
            # Update items collected
            if reward > 0:
                items_collected += 1
                print(f"📦 Collected an item! Total: {items_collected}")
                
                # Try to determine what was collected from the message
                message = helpers.parse_message(obs)
                print(f"Message: {message}")
                    
            # Slow down the agent execution for better visualization
            time.sleep(DELAY_BETWEEN_STEPS)
                
        # Print final status
        if success:
            print("\n🎉 SUCCESS: Mission accomplished!")
        elif died:
            print("\n⚰️ Agent died")
        elif terminated:
            # Try to determine why the game terminated
            message = helpers.parse_message(obs)
            print(f"\n⚠️ Game terminated: {message if message else 'Unknown reason'}")
            
            # Check level to see if we might have fallen through a trap door
            if obs['blstats'][12] != last_level:
                print(f"📊 Level changed unexpectedly from {last_level} to {obs['blstats'][12]}")
                
            # Check HP to see if agent died
            if obs["blstats"][10] <= 0:
                print("💀 HP is 0 or less, agent likely died")
                
            # Check starvation
            hunger_status = obs["blstats"][21]
            if hunger_status >= 4:  # Weak or Fainting
                print("🍽️ Agent may have starved (hunger status: Weak or Fainting)")
        elif truncated:
            print("\n⏱️ Game truncated (hit external time/step limit)")
        else:
            print(f"\n🛑 Stopped after {step} steps with {items_collected} items collected" + 
                 (", having descended" if descended else ", without descending"))
            
    finally:
        # Show the final game state
        try:
            final_render = env.render()
            print("\nFinal game state:\n")
            print(final_render)
        except Exception as e:
            print(f"Note: Could not render final game state: {e}")
        
        env.close()
        print("\n========== AGENT RUN COMPLETE ==========\n")

if __name__ == "__main__":
    # Run with no step limit (will run until success or death)
    main(max_steps=None)
    
    # Alternatively, you can run with a step limit:
    # main(max_steps=1000) 