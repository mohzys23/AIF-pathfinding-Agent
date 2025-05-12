import sys
import time
import random
import gymnasium as gym
from nle.nethack.actions import ACTIONS

# 
from algorithms import bfs
from utils import get_pos, is_item, find_ground_food, find_stairs
from constants import items_collected, visited_path, visit_counts, picked_up_locations, collected_items_log, ITEM_NAMES, ACTION_NAMES, NORTH, EAST, SOUTH, WEST, DOWN, WAIT, PICKUP, EAT

# ─── Main loop ────────────────────────────────────────────────────────────────
def main(max_steps=None):
    global items_collected, collected_items_log, picked_up_locations

    env = gym.make("NetHackScore-v0", render_mode="human")
    obs, _ = env.reset()
    step = 0

    # Two-step flags for PICKUP/EAT
    picking_up = False
    eating     = False
    eat_letter = None

    print("\n=== NetHack AI Agent Starting ===")

    while max_steps is None or step < max_steps:
        env.render()
        step += 1

        # record visit
        x,y = get_pos(obs)
        visited_path.add((x,y))
        visit_counts[(x,y)] = visit_counts.get((x,y),0)+1

        # status line
        hp, max_hp = obs["blstats"][10], obs["blstats"][11]
        hunger = obs["blstats"][18]
        print(f"\nStep {step:4d} | Pos=({x:2d},{y:2d}) | HP={hp}/{max_hp} | Hunger={hunger} | Items={items_collected}")

        # two-step pickup or eat
        if picking_up:
            action_enum = WAIT
            picking_up = False
            # Add location to picked up set after successful pickup
            picked_up_locations.add((x,y))

        elif eating:
            action_enum = ord(eat_letter)
            eating = False
            eat_letter = None

        else:
            ch = obs["chars"][y,x]

            # — on an item?
            if is_item(ch) and (x,y) not in picked_up_locations:  # Only pick up if not picked up before
                item_name = ITEM_NAMES[ch]
                if ch == ord('%') and hunger>=4:
                    # ground food when starving
                    print("→ Eating ground food")
                    collected_items_log.append({
                        'step': step,
                        'item': item_name,
                        'action': 'eaten',
                        'position': (x,y)
                    })
                    action_enum = PICKUP
                    picking_up = True
                    items_collected += 1
                elif ch == ord('%'):
                    # pick up food to inventory
                    print("→ PICKUP ground food")
                    collected_items_log.append({
                        'step': step,
                        'item': item_name,
                        'action': 'picked up',
                        'position': (x,y)
                    })
                    action_enum = PICKUP
                    picking_up = True
                    items_collected += 1
                else:
                    print("→ PICKUP", ITEM_NAMES[ch])
                    collected_items_log.append({
                        'step': step,
                        'item': item_name,
                        'action': 'picked up',
                        'position': (x,y)
                    })
                    action_enum = PICKUP
                    picking_up = True
                    items_collected += 1
            else:
                # if starving, go for ground food
                if hunger>=4:
                    gf = find_ground_food(obs)
                    if gf and gf not in picked_up_locations:  # Only go for food that hasn't been picked up
                        path = bfs((x,y), gf, obs["chars"], obs["glyphs"])
                        if path:
                            action_enum = path[0]
                            print("→ heading to food at", gf)
                        else:
                            action_enum = WAIT
                    else:
                        action_enum = WAIT

                # if enough items, head to stairs
                elif items_collected >= 5:
                    st = find_stairs(obs)
                    if st:
                        if (x,y)==st:
                            print("→ Descending")
                            action_enum = DOWN
                        else:
                            path = bfs((x,y), st, obs["chars"], obs["glyphs"])
                            if path:
                                action_enum = path[0]
                                print("→ heading to stairs at", st)
                            else:
                                action_enum = random.choice([NORTH,EAST,SOUTH,WEST])
                    else:
                        action_enum = random.choice([NORTH,EAST,SOUTH,WEST])

                # otherwise random exploration
                else:
                    action_enum = random.choice([NORTH,EAST,SOUTH,WEST])

        # map enum→index
        try:
            idx = ACTIONS.index(action_enum)
        except ValueError:
            print("⚠️ Unknown action, defaulting to WAIT")
            idx = ACTIONS.index(WAIT)

        print("Action:", ACTION_NAMES.get(action_enum, action_enum))
        obs, rew, term, trun, _ = env.step(idx)

        if rew>0:
            print(f"→ +{rew} reward (item?)")
        if term or trun:
            print("\n*** Game Over ***")
            print("\n=== Final Game State ===")
            print(f"Total steps: {step}")
            print(f"Total items collected: {items_collected}")
            print("\nDetailed Item Collection Log:")
            for item in collected_items_log:
                print(f"Step {item['step']}: {item['item']} - {item['action']} at position {item['position']}")
            break

        time.sleep(0.05)

    env.close()
    print("\n=== Run Complete ===")
    # Always print final state even if we didn't hit game over
    print("\n=== Final Game State ===")
    print(f"Total steps: {step}")
    print(f"Total items collected: {items_collected}")
    print("\nDetailed Item Collection Log:")
    for item in collected_items_log:
        print(f"Step {item['step']}: {item['item']} - {item['action']} at position {item['position']}")

if __name__=="__main__":
    ms = None
    if len(sys.argv)>1:
        try:
            ms = int(sys.argv[1])
        except:
            pass
    main(ms)
