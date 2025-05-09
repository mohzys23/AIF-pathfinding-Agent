
# Action mappings for the reduced action space

NORTH = 1     # CompassDirection.N (k)
SOUTH = 3     # CompassDirection.S (j)
EAST = 2      # CompassDirection.E (l)
WEST = 4      # CompassDirection.W (h)
PICKUP = 0    # Using MORE action as a placeholder (not ideal, but limited options)
EAT = 21      # Command.EAT (e)
WAIT = 19     # MiscDirection.WAIT (.)
DOWN = 18     # MiscDirection.DOWN (>)

# Map from action to name for logging
ACTION_NAMES = {
    NORTH: "NORTH (k)", 
    SOUTH: "SOUTH (j)", 
    EAST: "EAST (l)", 
    WEST: "WEST (h)",
    PICKUP: "PICKUP (,)",
    EAT: "EAT (e)",
    WAIT: "WAIT (.)",
    DOWN: "DOWN (>)"
}

# Item character to name mapping
ITEM_NAMES = {
    ord('$'): "gold piece",
    ord('%'): "food",
    ord('!'): "potion",
    ord('?'): "scroll",
    ord('/'): "wand",
    ord('='): "ring",
    ord('+'): "spellbook",
    ord('\"'): "amulet",
    ord('('): "tool",
    ord('['): "armor",
    ord(')'): "weapon",
    ord(']'): "armor",
    ord('*'): "gem",
    ord(','): "rock/stone",
}