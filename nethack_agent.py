import gymnasium as gym
import numpy as np
import random
from nle import nethack
from nle.nethack import actions as nh_actions
from collections import deque
import time

# Action mappings for the reduced action space
NORTH = 1     # CompassDirection.N (k)
SOUTH = 3     # CompassDirection.S (j)
EAST = 2      # CompassDirection.E (l)
WEST = 4      # CompassDirection.W (h)
PICKUP = 0    # Using MORE action as a placeholder (not ideal, but limited options)
EAT = 21      # Command.EAT (e)
WAIT = 19     # MiscDirection.WAIT (.)
DOWN = 18     # MiscDirection.DOWN (>)

# Map from action to name for logging
ACTION_NAMES = {
    NORTH: "NORTH (k)", 
    SOUTH: "SOUTH (j)", 
    EAST: "EAST (l)", 
    WEST: "WEST (h)",
    PICKUP: "PICKUP (,)",
    EAT: "EAT (e)",
    WAIT: "WAIT (.)",
    DOWN: "DOWN (>)"
}

# Item character to name mapping
ITEM_NAMES = {
    ord('$'): "gold piece",
    ord('%'): "food",
    ord('!'): "potion",
    ord('?'): "scroll",
    ord('/'): "wand",
    ord('='): "ring",
    ord('+'): "spellbook",
    ord('\"'): "amulet",
    ord('('): "tool",
    ord('['): "armor",
    ord(')'): "weapon",
    ord(']'): "armor",
    ord('*'): "gem",
    ord(','): "rock/stone",
}

def get_agent_position(obs):
    return tuple(obs["blstats"][:2])

def is_walkable(char_code, glyph):
    # Floor, corridor, open door, stairs
    walkable = [ord('.'), ord('#'), ord('+'), ord('>'), ord('<')]
    return char_code in walkable or is_item(char_code)

def is_item(char_code):
    # Expanded list of item characters
    return char_code in ITEM_NAMES

def find_path_bfs(start, target, chars, glyphs, visited_positions=None):
    """Find a path from start to target using BFS."""
    queue = deque([(start, [])])
    visited = {start}
    height, width = chars.shape
    
    while queue:
        (x, y), path = queue.popleft()
        
        if (x, y) == target:
            return path
        
        # Try all four directions
        for dx, dy, action in [(0, -1, NORTH), (1, 0, EAST), (0, 1, SOUTH), (-1, 0, WEST)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < height and 0 <= nx < width:
                if (nx, ny) not in visited and is_walkable(chars[ny][nx], glyphs[ny][nx]):
                    # If we have visited positions, avoid revisiting frequently visited positions
                    if visited_positions and visited_positions.get((nx, ny), 0) > 10:
                        continue
                    
                    visited.add((nx, ny))
                    new_path = path + [action]
                    queue.append(((nx, ny), new_path))
    
    return None

def find_nearest_item(pos, chars, glyphs, visited_positions=None):
    """Find the nearest item and return its position and a path to it."""
    height, width = chars.shape
    x, y = pos
    
    # Check if already on an item
    if is_item(chars[y][x]):
        return pos, []
    
    # Search using BFS
    queue = deque([(pos, [])])
    visited = {pos}
    
    while queue:
        (cx, cy), path = queue.popleft()
        
        # Try all four directions
        for dx, dy, action in [(0, -1, NORTH), (1, 0, EAST), (0, 1, SOUTH), (-1, 0, WEST)]:
            nx, ny = cx + dx, cy + dy
            if 0 <= ny < height and 0 <= nx < width:
                if (nx, ny) not in visited and is_walkable(chars[ny][nx], glyphs[ny][nx]):
                    if is_item(chars[ny][nx]):
                        return (nx, ny), path + [action]
                    
                    # If we have visited positions, avoid revisiting frequently visited positions
                    if visited_positions and visited_positions.get((nx, ny), 0) > 10:
                        continue
                        
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [action]))
    
    return None, []

def find_unexplored_bfs(pos, seen_map, chars, glyphs, visited_positions=None):
    """Find the nearest unexplored area using BFS."""
    height, width = chars.shape
    
    queue = deque([(pos, [])])
    visited = {pos}
    
    while queue:
        (x, y), path = queue.popleft()
        
        # Check surrounding cells for unexplored tiles
        for dx, dy, action in [(0, -1, NORTH), (1, 0, EAST), (0, 1, SOUTH), (-1, 0, WEST)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < height and 0 <= nx < width:
                if (nx, ny) not in visited:
                    # If we found an unexplored walkable cell
                    if not seen_map[ny][nx] and is_walkable(chars[ny][nx], glyphs[ny][nx]):
                        return (nx, ny), path + [action]
                    
                    # Continue searching if the cell is walkable
                    if is_walkable(chars[ny][nx], glyphs[ny][nx]):
                        # If we have visited positions, avoid revisiting frequently visited positions
                        if visited_positions and visited_positions.get((nx, ny), 0) > 15:
                            continue
                            
                        visited.add((nx, ny))
                        queue.append(((nx, ny), path + [action]))
    
    return None, []

def get_least_visited_position(pos, chars, glyphs, visited_positions):
    """Find the least visited walkable position."""
    if not visited_positions:
        return None, []
    
    # Get all walkable positions and their visit counts
    height, width = chars.shape
    walkable_positions = []
    
    for y in range(height):
        for x in range(width):
            if is_walkable(chars[y][x], glyphs[y][x]):
                visits = visited_positions.get((x, y), 0)
                walkable_positions.append(((x, y), visits))
    
    if not walkable_positions:
        return None, []
    
    # Sort by visit count (ascending)
    walkable_positions.sort(key=lambda p: p[1])
    
    # Take the least visited position that's not the current one
    for target_pos, visits in walkable_positions:
        if target_pos != pos and visits < 5:
            # Find path to this position
            path = find_path_bfs(pos, target_pos, chars, glyphs, visited_positions)
            if path:
                return target_pos, path
    
    return None, []

def find_stairs(chars):
    """Find down stairs in the level."""
    stairs_positions = np.argwhere(chars == ord('>'))
    if len(stairs_positions) > 0:
        # Return as (x, y)
        y, x = stairs_positions[0]
        return (x, y)
    return None

def parse_message(obs):
    """Extract readable message from observation."""
    message_chars = obs["message"]
    message = "".join([chr(c) for c in message_chars if c != 0])
    return message

def main():
    env = gym.make("NetHackScore-v0", render_mode="human")
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
    max_steps = 1000
    last_action = None
    action_history = []  # Keep track of recent actions to break loops
    random_exploration_steps = 0
    last_level = 1
    died = False
    
    try:
        print("\n========== STARTING NEW AGENT RUN ==========\n")
        
        while not (terminated or truncated) and step < max_steps:
            step += 1
            pos = get_agent_position(obs)
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
            message = parse_message(obs)
            if message:
                print(f"Game message: {message}")
                
                # Check for death or important events in message
                if "You die" in message or "You were killed" in message:
                    print("⚰️ AGENT DIED!")
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
            if is_item(obs["chars"][y][x]):
                item_type = ITEM_NAMES.get(obs["chars"][y][x], "unknown item")
                action = EAT if obs["chars"][y][x] == ord('%') else PICKUP
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
                    break
                # If we have enough items, try to find stairs
                elif items_collected >= 3 and not descended:
                    stairs_pos = find_stairs(obs["chars"])
                    
                    if stairs_pos and pos == stairs_pos:
                        action = DOWN
                        print(f"⬇️ Found stairs! Going down...")
                    elif stairs_pos:
                        # Find path to stairs
                        path = find_path_bfs(pos, stairs_pos, obs["chars"], obs["glyphs"], visited_positions)
                        if path and len(path) > 0:
                            action = path[0]
                            print(f"🧭 Moving toward stairs: {stairs_pos}")
                        else:
                            # No clear path, explore
                            item_pos, item_path = find_nearest_item(pos, obs["chars"], obs["glyphs"], visited_positions)
                            if item_pos and len(item_path) > 0:
                                item_type = ITEM_NAMES.get(obs["chars"][item_pos[1]][item_pos[0]], "unknown item")
                                action = item_path[0]
                                print(f"🏃 Moving toward {item_type} at {item_pos}")
                            else:
                                # Try to find unexplored areas
                                unexplored_pos, unexplored_path = find_unexplored_bfs(pos, seen_map, obs["chars"], obs["glyphs"], visited_positions)
                                if unexplored_pos and len(unexplored_path) > 0:
                                    action = unexplored_path[0]
                                    print(f"🔍 Exploring: {unexplored_pos}")
                                else:
                                    # Try to find least visited position
                                    least_visited_pos, least_visited_path = get_least_visited_position(pos, obs["chars"], obs["glyphs"], visited_positions)
                                    if least_visited_pos and len(least_visited_path) > 0:
                                        action = least_visited_path[0]
                                        print(f"👣 Moving to least visited: {least_visited_pos}")
                                    else:
                                        # Random movement as a last resort
                                        action = random.choice([NORTH, SOUTH, EAST, WEST])
                                        print(f"🎲 Moving randomly")
                    else:
                        # No stairs found, look for items or explore
                        item_pos, item_path = find_nearest_item(pos, obs["chars"], obs["glyphs"], visited_positions)
                        if item_pos and len(item_path) > 0:
                            item_type = ITEM_NAMES.get(obs["chars"][item_pos[1]][item_pos[0]], "unknown item")
                            action = item_path[0]
                            print(f"🏃 Moving toward {item_type} at {item_pos}")
                        else:
                            # Try to find unexplored areas
                            unexplored_pos, unexplored_path = find_unexplored_bfs(pos, seen_map, obs["chars"], obs["glyphs"], visited_positions)
                            if unexplored_pos and len(unexplored_path) > 0:
                                action = unexplored_path[0]
                                print(f"🔍 Exploring: {unexplored_pos}")
                            else:
                                # Try to find least visited position
                                least_visited_pos, least_visited_path = get_least_visited_position(pos, obs["chars"], obs["glyphs"], visited_positions)
                                if least_visited_pos and len(least_visited_path) > 0:
                                    action = least_visited_path[0]
                                    print(f"👣 Moving to least visited: {least_visited_pos}")
                                else:
                                    # Random movement as a last resort
                                    action = random.choice([NORTH, SOUTH, EAST, WEST])
                                    print(f"🎲 Moving randomly")
                else:
                    # Look for items to collect
                    item_pos, item_path = find_nearest_item(pos, obs["chars"], obs["glyphs"], visited_positions)
                    if item_pos and len(item_path) > 0:
                        item_type = ITEM_NAMES.get(obs["chars"][item_pos[1]][item_pos[0]], "unknown item")
                        action = item_path[0]
                        print(f"🏃 Moving toward {item_type} at {item_pos}")
                    else:
                        # Try to find unexplored areas
                        unexplored_pos, unexplored_path = find_unexplored_bfs(pos, seen_map, obs["chars"], obs["glyphs"], visited_positions)
                        if unexplored_pos and len(unexplored_path) > 0:
                            action = unexplored_path[0]
                            print(f"🔍 Exploring: {unexplored_pos}")
                        else:
                            # Try to find least visited position
                            least_visited_pos, least_visited_path = get_least_visited_position(pos, obs["chars"], obs["glyphs"], visited_positions)
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
                        directions.remove(last_action)
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
                message = parse_message(obs)
                print(f"Message: {message}")
                    
            # Slow down the agent execution for better visualization
            time.sleep(0.05)  # 50ms delay
                
        # Print final status
        if terminated:
            print("\n⚠️ Game terminated (agent likely died)")
        elif truncated:
            print("\n⏱️ Game truncated (hit step/time limit)")
        elif died:
            print("\n⚰️ Agent died")
        elif items_collected >= 5 and descended:
            print("\n🎉 SUCCESS: Mission accomplished!")
        else:
            print(f"\n🛑 Stopped after {step} steps with {items_collected} items collected" + 
                 (", having descended" if descended else ", without descending"))
            
    finally:
        env.close()
        print("\n========== AGENT RUN COMPLETE ==========\n")

if __name__ == "__main__":
    main() 