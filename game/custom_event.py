"""Initiate the custom events used in the game"""

from game.utils.eventhandler import CustomEvent

# to be used in level_gen and views.map
# check if player was moved, if not, don't regenerate the map
MOVED = CustomEvent()
# if player encounters an enemy
ENEMY_ENCOUNTERED = CustomEvent()

# new event
COUNTER = CustomEvent()
