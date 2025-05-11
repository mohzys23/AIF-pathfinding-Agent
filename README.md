# NetHack Pathfinding Agent

A simple pathfinding agent that explores and collects items in the NetHack game environment.

## Features

- BFS pathfinding for navigation
- Basic item collection and inventory management
- Hunger monitoring and food management
- Automatic stair detection after collecting items

## Requirements & Installation

```bash
pip install gymnasium numpy nle
```

## Usage

Run without step limit:
```bash
python nethack_agent.py
```

Run with step limit:
```bash
python nethack_agent.py 1000
```

## How It Works

The agent:
- Explores the dungeon using BFS
- Collects items it finds along the way
- Manages hunger by prioritizing food when needed
- Seeks stairs after collecting 5 items
- Tracks visited locations to avoid loops

The agent provides real-time status updates showing position, HP, hunger level, and items collected.
