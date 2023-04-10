""" Implements the Landing view """
import sys

import pygame

from game.config import GAME_TITLE
from game.utils import Text
from game.views import View


class Start(View):
    """The Starting view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_draw(self):
        Text(
            GAME_TITLE,
            self.font,
            self.width / 2,
            self.height / 2 - 50,
            200,
            "red",
        ).blit_into(self.screen)
        Text(
            "Click to advance!",
            self.font,
            self.width / 2,
            self.height / 2 + 50,
            50,
            "white",
        ).blit_into(self.screen)

    def on_click(self, event):
        self.change_views("menu.Menu", caption="Menu")

    @staticmethod
    def exit():
        print("Quiting the game.", flush=True)
        pygame.quit()
        sys.exit()
