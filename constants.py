import nle.nethack.actions as actions


# ─── Action constants ──────────────────────────────────────────────────────────
NORTH, EAST, SOUTH, WEST = (
    actions.CompassDirection.N, # type: ignore
    actions.CompassDirection.E, # type: ignore
    actions.CompassDirection.S, # type: ignore
    actions.CompassDirection.W, # type: ignore
)
DOWN, WAIT = actions.MiscDirection.DOWN, actions.MiscDirection.WAIT
PICKUP, EAT = actions.MiscAction.MORE, actions.Command.EAT

ACTION_NAMES = {
    NORTH: "NORTH (k)", EAST: "EAST (l)",
    SOUTH: "SOUTH (j)", WEST: "WEST (h)",
    DOWN:   "DOWN (>)",  WAIT: "WAIT (.)",
    PICKUP: "PICKUP (,)", EAT:   "EAT (e)",
}

# ─── Item lookup ───────────────────────────────────────────────────────────────
ITEM_NAMES = {
    ord('$'): "gold piece", ord('%'): "food",    ord('!'): "potion",
    ord('?'): "scroll",     ord('/'): "wand",    ord('='): "ring",
    ord('+'): "spellbook",  ord('\"'):"amulet", ord('('): "tool",
    ord('['):"armor",       ord(')'): "weapon",  ord(']'): "armor",
    ord('*'):"gem",         ord(','): "rock/stone",
}


# ─── Globals for tracking ─────────────────────────────────────────────────────
visited_path   = set()   # positions we've stepped on
visit_counts   = {}      # (x,y) -> # of visits
items_collected = 0
collected_items_log = []  # List to store details of collected items
picked_up_locations = set()  # Set to track locations where items were picked up
# Before your loop, tighten revisit threshold:
MAX_REVISIT = 5