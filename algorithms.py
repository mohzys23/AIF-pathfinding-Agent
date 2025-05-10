from collections import deque
from constant import NORTH, EAST, SOUTH, WEST
import helper_functions as helpers



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
                if (nx, ny) not in visited and helpers.is_walkable(chars[ny][nx], glyphs[ny][nx]):
                    # If we have visited positions, avoid revisiting frequently visited positions
                    if visited_positions and visited_positions.get((nx, ny), 0) > 10:
                        continue
                    
                    visited.add((nx, ny))
                    new_path = path + [action]
                    queue.append(((nx, ny), new_path))
    
    return None


def find_nearest_item(pos, chars, glyphs, visited_positions=None):
    """Find the nearest item and return its position and a path to it using BFS."""
    height, width = chars.shape
    x, y = pos
    
    # Check if already on an item
    if helpers.is_item(chars[y][x]):
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
                if (nx, ny) not in visited and helpers.is_walkable(chars[ny][nx], glyphs[ny][nx]):
                    if helpers.is_item(chars[ny][nx]):
                        return (nx, ny), path + [action]
                    
                    # If we have visited positions, avoid revisiting frequently visited positions
                    if visited_positions and visited_positions.get((nx, ny), 0) > 10:
                        continue
                        
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [action]))
    
    return None, []



def find_unexplored_dfs(pos, seen_map, chars, glyphs, visited_positions=None):
    """Find the nearest unexplored area using DFS."""
    height, width = chars.shape
    
    # Use a stack instead of a queue for DFS
    stack = [(pos, [])]
    visited = {pos}
    
    while stack:
        (x, y), path = stack.pop()  # Pop from the end (LIFO) for DFS
        
        # Check surrounding cells for unexplored tiles
        for dx, dy, action in [(0, -1, NORTH), (1, 0, EAST), (0, 1, SOUTH), (-1, 0, WEST)]:
            nx, ny = x + dx, y + dy
            if 0 <= ny < height and 0 <= nx < width:
                if (nx, ny) not in visited:
                    # If we found an unexplored walkable cell
                    if not seen_map[ny][nx] and helpers.is_walkable(chars[ny][nx], glyphs[ny][nx]):
                        return (nx, ny), path + [action]
                    
                    # Continue searching if the cell is walkable
                    if helpers.is_walkable(chars[ny][nx], glyphs[ny][nx]):
                        # If we have visited positions, avoid revisiting frequently visited positions
                        if visited_positions and visited_positions.get((nx, ny), 0) > 15:
                            continue
                            
                        visited.add((nx, ny))
                        stack.append(((nx, ny), path + [action]))
    
    return None, []