import numpy as np
from constants import ITEM_NAMES



# ─── Helpers ──────────────────────────────────────────────────────────────────
def get_pos(obs):
    """Return (x,y) from obs['tty_cursor']==(row,col)."""
    r, c = obs["tty_cursor"]
    return int(c), int(r)

def is_item(ch):
    return ch in ITEM_NAMES

def is_walkable(ch, glyph):
    return ch in (ord('.'), ord('#'), ord('+'), ord('>'), ord('<')) or is_item(ch)

def find_ground_food(obs):
    """Return first (x,y) of '%' on the ground, or None."""
    ys, xs = np.where(obs["chars"] == ord('%'))
    if xs.size:
        return int(xs[0]), int(ys[0])
    return None

def find_stairs(obs):
    ys, xs = np.where(obs["chars"] == ord('>'))
    if xs.size:
        return int(xs[0]), int(ys[0])
    return None

