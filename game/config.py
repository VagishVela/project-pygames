""" Configuration for the game """
import logging

# Game
GAME_TITLE = "Game"
SCREEN_HEIGHT = 640
SCREEN_WIDTH = 640
FPS = 60
TILE_SIZE = 72  # ceil(screen_size/9)

# Logger
LOGGER_LEVEL = logging.DEBUG  # development
# LOGGER_LEVEL = logging.WARNING    # production

# Store meta
STORE_PADDING = int(TILE_SIZE * 1.33)
STORE_BG = (50, 50, 50)
STORE_SCROLL_SPEED = 20
STORE_ON_FOCUS = (25, 25, 25)
