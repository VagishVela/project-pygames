"""Initiate the custom events used in the game"""

from game.utils.eventhandler import CustomEvent

# to be used in level_gen and views.map
# check if player was moved, if not, don't regenerate the map
MOVED = CustomEvent()
# if player encounters an enemy
ENEMY_ENCOUNTERED = CustomEvent()

# make mouse controls easier
LEFT_CLICK = CustomEvent({"pos": ..., "button": "left"})
RIGHT_CLICK = CustomEvent({"pos": ..., "button": "right"})
SCROLL_UP = CustomEvent({"pos": ..., "mode": "up"})
SCROLL_DOWN = CustomEvent({"pos": ..., "mode": "down"})

# to be used in the store
ITEM_FOCUSED = CustomEvent({"item": ...})
