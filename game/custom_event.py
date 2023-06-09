"""Initiate the custom events used in the game"""

from game.utils.eventhandler import CustomEvent

# to be used in level_gen, views.map and battle
# if player encounters an enemy
ENEMY_ENCOUNTERED = CustomEvent({"pos": ...})
# to pass views within views
PASS_VIEW = CustomEvent({"view": ...})
# wait for enemy's turn
WAIT_FOR_ENEMY = CustomEvent()

# make mouse controls easier
LEFT_CLICK = CustomEvent({"pos": ..., "button": "left"})
RIGHT_CLICK = CustomEvent({"pos": ..., "button": "right"})
SCROLL_UP = CustomEvent({"pos": ..., "mode": "up"})
SCROLL_DOWN = CustomEvent({"pos": ..., "mode": "down"})

# to be used in the store
ITEM_FOCUSED = CustomEvent({"item": ...})

# disappearing texts
TEXT_DISAPEAR = CustomEvent({"id": ...})
