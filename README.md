# NetHack Pathfinding Agent

A simple agent that explores NetHack dungeons, collects items, and uses pathfinding to navigate.

## Setup

1. Create and activate virtual environment:

```bash
# Create venv
python -m venv venv

# Activate venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install gymnasium numpy nle
```

## Usage

Run single episode:

```bash
python nethack_agent.py
```

Run with step limit:

```bash
python nethack_agent.py 1000
```

Run evaluation (multiple episodes):

```bash
# Run default (5 episodes, 1000 steps each)
python evaluate_agent.py

# Run custom configuration
python evaluate_agent.py --episodes 10 --steps 2000
```

## Agent Behavior

The agent:

- Collects items (food, gold, weapons, armor, etc.)
- Seeks stairs after collecting items
- Tracks visited locations to prevent getting stuck
- Maintains a log of collected items

The agent displays:

- Current position and step count
- HP and hunger status
- Items collected
- Action being taken
- Detailed collection log at end of run
