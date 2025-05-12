# ─── Evaluation (no descent) ───────────────────────────────────────────────────
import gymnasium as gym
import numpy as np
import statistics

# Import your refactored main
from nethack_agent import main  

N = 1 # Number of evaluation runs
items_list = []
starve_count = 0
steps_per_item = []
success_count = 0

for _ in range(N):
    items, starvation, steps = main(max_steps=1000)
    items_list.append(items)
    if starvation:
        starve_count += 1
    if items > 0:
        steps_per_item.append(steps / items)
    if items >= 5:
        success_count += 1

print(f"Items collected:      {statistics.mean(items_list):.2f} ± {statistics.pstdev(items_list):.2f}")
print(f"Starvation rate:      {starve_count}/{N} ({starve_count/N*100:.0f}%)")
print(f"Avg steps per item:   {statistics.mean(steps_per_item):.1f} ± {statistics.pstdev(steps_per_item):.1f}")
print(f"Full‐success rate:    {success_count}/{N} ({success_count/N*100:.0f}%)")
