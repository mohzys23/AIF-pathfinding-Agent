import numpy as np
from collections import deque
from constant import ITEM_NAMES, NORTH, SOUTH, EAST, WEST

def get_agent_position(obs):
    """Extract the agent's position from the observation."""
    return tuple(obs["blstats"][:2])

def is_walkable(char_code, glyph):
    """Check if a tile is walkable."""
    # Floor, corridor, open door, stairs
    walkable = [ord('.'), ord('#'), ord('+'), ord('>'), ord('<')]
    return char_code in walkable or is_item(char_code)

def is_item(char_code):
    """Check if a character code represents an item."""
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