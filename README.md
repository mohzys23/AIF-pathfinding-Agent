# NetHack Pathfinding Agent

An intelligent agent that navigates the NetHack dungeon environment using Python and the NetHack Learning Environment (NLE).


### Resources

**Gen NLE doc**

**GITHUB**: [https://gist.github.com/HanClinto/310bc189dcb34b9628d5151b168a34b0](https://gist.github.com/HanClinto/310bc189dcb34b9628d5151b168a34b0)

## Overview

This project implements an autonomous agent that explores and navigates through NetHack dungeons using pathfinding algorithms and strategic decision-making.

## Features

- Intelligent pathfinding using Breadth-First Search (BFS)
- Dynamic exploration of unseen areas
- Automated hunger management and food seeking
- Stair detection and level progression
- Item collection tracking
- Fallback movement strategies

## Technical Implementation

- **Pathfinding**: Uses BFS to find optimal paths to goals
- **State Management**: Tracks agent position, inventory, and dungeon state
- **Decision Making**: Prioritizes actions based on:
  - Hunger status
  - Item collection goals
  - Level progression
  - Unexplored areas
- **Safety**: Includes walkable tile validation and monster avoidance

## Requirements

- Python 3.x
- gymnasium
- NetHack Learning Environment (nle)
- numpy

## Goals

The agent aims to:

1. Collect at least 5 items
2. Reach dungeon level 2 or deeper

## Key Components

- `get_agent_position()`: Extracts agent coordinates
- `is_walkable()`: Validates safe movement tiles
- `find_stairs()`: Locates dungeon stairs
- `find_food_letter()`: Identifies food in inventory
- `bfs()`: Implements pathfinding algorithm
- `find_unseen()`: Discovers unexplored areas

## Usage

```python
# Run the agent
env = gym.make("NetHackScore-v0", render_mode="human")
# Execute the notebook [agent-nethack.ipynb](http://_vscodecontentref_/1)
```
