# NetHack Pathfinding Agent

This project implements an autonomous agent capable of exploring and making progress in the roguelike game NetHack, using the OpenAI Gymnasium interface and the NetHack Learning Environment (NLE).

## Features

- Intelligent pathfinding using Breadth-First Search (BFS)
- Item collection strategy with prioritization
- Exploration of unexplored areas in the game map
- Detection and handling of being stuck in the same position
- Oscillation detection and correction
- Automatic descent to lower dungeon levels after collecting sufficient items

## Requirements

- Python 3.9+
- pip (Python package installer)
- A graphical environment to display the NetHack interface

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

- **nethack_agent.py**: Main agent implementation that handles game interactions, decision-making, and action execution.
- **helper_functions.py**: Contains helper functions for pathfinding, item detection, map exploration, and other utilities.
- **constant.py**: Constants and mappings used by the agent (action codes, item identifiers, etc.)

## Running the Agent

To run the agent with the visual NetHack interface:

```bash
python nethack_agent.py
```

Alternatively, use the provided script:

```bash
chmod +x run_agent.sh
./run_agent.sh
```

This will open a window displaying the NetHack game interface along with log information in the terminal.

## Troubleshooting the NetHack Interface

If you don't see the NetHack interface:

1. **Check your display environment**: Ensure you're running in an environment that supports graphical windows (X11 on Linux, native GUI on Windows/macOS).
2. **Check for SDL dependencies**: The NetHack Learning Environment uses SDL for rendering. Make sure your system has the necessary SDL libraries.
3. **Remote environments**: If you're running on a remote server or SSH session, ensure you have X11 forwarding enabled.
4. **Check console output**: The script provides information in the terminal about the interface status.
5. **Alternative render modes**: If you still can't see the interface, you can modify the `render_mode` parameter in nethack_agent.py to use "ansi" instead of "human" for terminal-based visualization.

## Agent Behavior

The agent follows this general strategy:

1. Collect at least 3 items on the current level
2. Find and descend stairs to reach the next level if 5 items has been retrieved/collected
3. Continue exploring and collecting items
4. Success is achieved when the agent has collected at least 5 items and descended at least one level

## Visual Feedback

The agent provides:

1. The classic ASCII NetHack interface showing the dungeon, character, monsters, and items
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

- `max_steps`: Maximum steps the agent will take before stopping
- `time.sleep()`: Adjust the speed of agent actions for better visualization
- Item collection thresholds for level descent

## Acknowledgments

- [NetHack Learning Environment (NLE)](https://github.com/facebookresearch/nle)
- [OpenAI Gymnasium](https://gymnasium.farama.org/)
