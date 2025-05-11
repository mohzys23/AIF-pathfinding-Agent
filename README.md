# NetHack Pathfinding Agent

A focused implementation of an autonomous agent for collecting items in NetHack using the OpenAI Gymnasium interface and the NetHack Learning Environment (NLE).

## Features

- Efficient pathfinding using BFS and DFS algorithms
- Smart item collection strategy
- Intelligent hunger management with all NetHack hunger states
- Systematic exploration of unexplored areas
- Pattern detection to avoid movement loops
- Clear status display with hunger state tracking

## Requirements

- Python 3.9+
- pip (Python package installer)
- OpenAI Gymnasium
- NetHack Learning Environment (NLE)

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install required packages:
```bash
pip install gymnasium numpy "nle>=0.9.0"
```

## Project Structure

- **nethack_agent.py**: Main agent implementation with game interaction and decision-making
- **algorithms.py**: Core pathfinding algorithms (BFS, DFS)
- **helper_functions.py**: Utility functions for navigation and item detection
- **constant.py**: Game constants, hunger states, and mappings

## Running the Agent

Run the agent with:
```bash
python nethack_agent.py           # Run indefinitely until goal reached
python nethack_agent.py 600       # Run for maximum 600 steps
```

The agent will:
1. Navigate through the dungeon
2. Collect items (gold, food, armor, weapons)
3. Manage hunger state intelligently:
   - Eat when hungry or worse
   - Avoid eating when satiated
   - Prevent oversatiation to avoid choking
4. Stop after collecting 5 items or reaching max steps (if specified)

## Hunger States

The agent tracks and responds to all NetHack hunger states:
- Oversatiated: Too full, risk of choking
- Satiated: Well fed
- Not Hungry: Normal state
- Hungry: Getting hungry
- Weak: Weak from hunger
- Fainting: About to faint

## Configuration

You can modify these parameters in the code:
- `DELAY_BETWEEN_STEPS`: Time between actions for visualization (constant.py)
- Visit thresholds for position revisiting (helper_functions.py)

## Troubleshooting

Common issues:
1. **Missing dependencies**: Ensure all packages are installed
2. **Rendering issues**: Some terminals may not display ASCII art correctly
3. **NLE installation**: See [NLE GitHub](https://github.com/facebookresearch/nle) for platform-specific instructions
