
# AIF-pathfinding-Agent

A pathfinding agent for NetHack using Python and the NetHack Learning Environment (NLE).

## Overview

This project implements an intelligent agent that navigates the NetHack dungeon environment with the following capabilities:

- Pathfinding using Breadth-First Search (BFS)
- Hunger management and food-seeking behavior
- Stair detection and level progression
- Item collection tracking
- Exploration of unseen areas

## Goals

The agent aims to:

1. Collect at least 5 items
2. Reach dungeon level 2 or deeper

## Dependencies

- gymnasium
- nle (NetHack Learning Environment)
- numpy

## Key Features

- **Pathfinding**: Uses BFS algorithm to find optimal paths to goals
- **Exploration**: Systematically explores unseen areas of the dungeon
- **Survival**: Manages hunger by finding and consuming food
- **Navigation**: Can locate and use stairs to descend levels
- **Item Collection**: Tracks collected items and aims for collection goals

## Agent Behaviors

- Searches for and moves toward dungeon stairs
- Explores unexplored areas when no stairs are visible
- Monitors hunger status and seeks food when hungry
- Picks up items encountered during exploration
- Uses fallback movement patterns when stuck

## Usage

Run the Jupyter notebook `agent-nethack.ipynb` to see the agent in action. The environment renders in "human" mode for visual observation of the agent's behavior.
