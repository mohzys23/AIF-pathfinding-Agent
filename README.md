# NetHack Pathfinding Agent

This project implements an autonomous agent capable of exploring and making progress in the roguelike game NetHack, using the OpenAI Gymnasium interface and the NetHack Learning Environment (NLE).

## Features

- Intelligent pathfinding using Breadth-First Search (BFS) and Depth-First Search (DFS)
- Item collection strategy with prioritization
- Exploration of unexplored areas in the game map
- Detection and handling of being stuck in the same position
- Oscillation detection and correction
- Automatic descent to lower dungeon levels after collecting sufficient items
- Terminal-based display of the NetHack interface

## Requirements

- Python 3.9+
- pip (Python package installer)

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/nethack-pathfinding-agent.git
cd nethack-pathfinding-agent
```

2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install gymnasium numpy "nle>=0.9.0"
```

Note: NLE (NetHack Learning Environment) may have additional system dependencies. If you encounter installation issues, refer to the [NLE GitHub repository](https://github.com/facebookresearch/nle) for detailed installation instructions.

## Project Structure

- **algorithms.py**: Contains implementations of pathfinding algorithms (BFS, DFS) and related search utilities
- **nethack_agent.py**: Main agent implementation that handles game interactions, decision-making, and action execution.
- **helper_functions.py**: Contains helper functions for pathfinding, item detection, map exploration, and other utilities.
- **constant.py**: Constants and mappings used by the agent (action codes, item identifiers, etc.)
- **run_agent.sh**: Shell script to run the agent with or without a step limit

## Running the Agent

### Using the script

The script provides an easy way to run the agent:

```bash
# Make the script executable first
chmod +x run_agent.sh

# Run without a step limit (until success or death)
./run_agent.sh

# Run with a specific step limit (e.g., 500 steps)
./run_agent.sh 500
```

### Running directly

You can also run the Python script directly:

```bash
python3 nethack_agent.py
```

The agent will display the NetHack interface directly in your terminal using ANSI rendering. You'll see the dungeon, the agent (@), monsters, items, and other game elements, along with detailed logs of the agent's decision-making process.

## Agent Behavior

The agent follows this general strategy:

1. Collect at least 3 items on the current level
2. Find and descend stairs to reach the next level
3. Continue exploring and collecting items
4. Success is achieved when the agent has collected at least 5 items and descended at least one level

## Visual Feedback

The agent provides:

1. The classic ASCII NetHack interface showing the dungeon, character, monsters, and items directly in the terminal
2. Terminal output with detailed logs of agent decision-making
3. Emojis to indicate status:
   - 🎒 Finding items
   - 🏃 Moving toward items
   - 🔍 Exploring new areas
   - 👣 Moving to less-visited areas
   - 🎲 Moving randomly
   - ⬇️ Going down stairs
   - 🔄 Breaking out of movement patterns
   - ⚠️ Stuck detection
   - ❗ HP decrease alerts
   - 😴 Unconsciousness alerts
   - 🕳️ Falling through trap alerts

## Technical Implementation

- **Pathfinding**: Uses BFS to find optimal paths to goals
- **State Management**: Tracks agent position, inventory, and dungeon state
- **Decision Making**: Prioritizes actions based on:
  - Hunger status
  - Item collection goals
  - Level progression
  - Unexplored areas
- **Safety**: Includes walkable tile validation and monster avoidance

## Customization

You can modify the agent's behavior by adjusting parameters in `nethack_agent.py`:

- `time.sleep()`: Adjust the speed of agent actions for better visualization (default is 0.05 seconds between steps)
- Item collection thresholds for level descent (currently set to collect at least 3 items before looking for stairs)
- Pass a `max_steps` parameter to limit the maximum number of steps

## Troubleshooting

If you encounter issues:

1. **Python not found**: Make sure you're using `python3` explicitly on macOS/Linux
2. **Missing dependencies**: Ensure all required packages are installed
3. **ANSI rendering issues**: Some terminals may not display the ASCII art correctly

## Acknowledgments

- [NetHack Learning Environment (NLE)](https://github.com/facebookresearch/nle)
- [OpenAI Gymnasium](https://gymnasium.farama.org/)
