import numpy as np
from collections import deque
from constants import NORTH, EAST, SOUTH, WEST, visited_path, visit_counts, ACTION_NAMES
from utils import is_walkable
import heapq
import nle.nethack.actions as ACTIONS


def bfs(start, goal, chars, glyphs):
    """4-way BFS from start→goal avoiding visited_path & heavily visited tiles."""
    h, w = chars.shape
    queue = deque([(start, [])])
    seen = {start}
    moves = [(0,-1,NORTH),(1,0,EAST),(0,1,SOUTH),(-1,0,WEST)]
    while queue:
        (x,y), path = queue.popleft()
        if (x,y) == goal:
            return path
        for dx, dy, act in moves:
            nx, ny = x+dx, y+dy
            if 0 <= nx < w and 0 <= ny < h:
                pos = (nx,ny)
                if pos in seen or pos in visited_path:
                    continue
                if not is_walkable(chars[ny,nx], glyphs[ny,nx]):
                    continue
                if visit_counts.get(pos,0) > 10:
                    continue
                seen.add(pos)
                queue.append((pos, path+[act]))
    return []




def a_star(start, goal, chars, glyphs, is_walkable_fn, visit_counts, max_revisit):
    """A* search with Manhattan heuristic on your NetHack grid."""
    def manhattan(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    w, h = chars.shape[1], chars.shape[0]
    open_set = [(manhattan(start, goal), 0, start, [])]
    closed   = set()

    while open_set:
        est, cost, (x, y), path = heapq.heappop(open_set)
        if (x, y) == goal:
            return path

        if (x, y) in closed:
            continue
        closed.add((x, y))

        for dx, dy, act in [(0,-1,'N'), (1,0,'E'), (0,1,'S'), (-1,0,'W')]:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < w and 0 <= ny < h):
                continue
            if visit_counts.get((nx, ny), 0) > max_revisit:
                continue
            if not is_walkable_fn(nx, ny, chars, glyphs):
                continue

            new_cost = cost + 1
            heapq.heappush(open_set, (
                new_cost + manhattan((nx, ny), goal),
                new_cost,
                (nx, ny),
                path + [ACTION_NAMES[act]]
            ))
    return []
