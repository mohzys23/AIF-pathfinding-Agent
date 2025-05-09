import gymnasium as gym
import nle
from nle import nethack
from nle.nethack import actions as nh_actions

# Create the environment
env = gym.make("NetHackScore-v0")

# Get the actual actions the environment is using
try:
    print("Environment actions:", env.unwrapped.actions)
except Exception as e:
    print(f"Couldn't get actions directly: {e}")

# Try to get the mapping between action indices and actual commands
print("\nTrying to find the mapping from indices to commands...")
print("NLE Actions:", nh_actions.ACTIONS)
print(f"Number of NLE actions: {len(nh_actions.ACTIONS)}")
print(f"Environment action space: {env.action_space}")

# If the environment has a mapping, try to print it
try:
    for i in range(env.action_space.n):
        print(f"Action index {i} maps to: {env.unwrapped.actions[i]} (value: {env.unwrapped.actions[i].value if hasattr(env.unwrapped.actions[i], 'value') else env.unwrapped.actions[i]})")
except Exception as e:
    print(f"Couldn't get mapping: {e}")

# Print the directional commands we want to use
print("\nMovement commands we want to use:")
move_cmds = {
    'North': {'char': 'k', 'ord': ord('k'), 'enum': nh_actions.CompassDirection.N},
    'South': {'char': 'j', 'ord': ord('j'), 'enum': nh_actions.CompassDirection.S},
    'East': {'char': 'l', 'ord': ord('l'), 'enum': nh_actions.CompassDirection.E},
    'West': {'char': 'h', 'ord': ord('h'), 'enum': nh_actions.CompassDirection.W},
    'Pickup': {'char': ',', 'ord': ord(','), 'enum': nh_actions.Command.PICKUP},
    'Eat': {'char': 'e', 'ord': ord('e'), 'enum': nh_actions.Command.EAT}
}

for direction, cmd in move_cmds.items():
    print(f"{direction}: char='{cmd['char']}', ord={cmd['ord']}, enum={cmd['enum']} (value={cmd['enum'].value})")
    try:
        idx = list(nh_actions.ACTIONS).index(cmd['enum'])
        print(f"  Index in ACTIONS: {idx}")
    except ValueError:
        print(f"  Not found in ACTIONS")

# Close the environment
env.close() 