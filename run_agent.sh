#!/bin/bash

# Run the NetHack Pathfinding Agent
# Usage: ./run_agent.sh [max_steps]
# If max_steps is provided, the agent will run for at most that many steps
# If max_steps is not provided, the agent will run until success or death

echo "Starting NetHack Pathfinding Agent..."
echo "The NetHack interface will be displayed in the terminal."
echo ""

# Check if a max_steps argument was provided
if [ -n "$1" ]; then
    # Edit the nethack_agent.py file to use the provided max_steps
    sed -i.bak "s/main(max_steps=None)/main(max_steps=$1)/" nethack_agent.py
    echo "Running with max steps: $1"
    python3 nethack_agent.py
    # Restore the original file
    mv nethack_agent.py.bak nethack_agent.py
else
    # Run without a step limit
    echo "Running without step limit (until success or death)"
    python3 nethack_agent.py
fi 