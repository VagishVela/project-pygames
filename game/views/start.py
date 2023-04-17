""" Implements the Landing view """
import sys

import pygame

from game.config import GAME_TITLE
from game.utils import Text
from game.views import View, logger

# get logger
logger = logger.getChild("start")


class Start(View):
    """The Starting view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_draw(self):
        Text(
            GAME_TITLE,
            "pokemon-hollow",
            self.width / 2,
            self.height / 2 - 50,
            100,
            "red",
        ).blit_into(self.screen)
        Text(
            "Click to advance!",
            "pokemon-hollow",
            self.width / 2,
            self.height / 2 + 50,
            50,
            "white",
        ).blit_into(self.screen)

    def on_click(self, event):
        logger.debug(" mouse clicked")
        self.change_views("menu.Menu", caption="Menu")

    def exit(self):
        logger.debug(f" View exits: {self}")
        print("Quiting the game.", flush=True)
        pygame.quit()
        sys.exit()
