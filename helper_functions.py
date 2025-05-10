import numpy as np
from collections import deque
from constant import ITEM_NAMES, NORTH, SOUTH, EAST, WEST
import algorithms as alg

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
            path = alg.find_path_bfs(pos, target_pos, chars, glyphs, visited_positions)
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