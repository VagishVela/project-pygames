""" Implements the Landing view """
import sys

import pygame

from game.config import GAME_TITLE
from game.helper import Text
from views import View


class Start(View):
    """The Starting view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_draw(self):
        self.screen.fill("black")
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

    def on_click(self):
        # import here to avoid circular imports
        # pylint: disable=C0415
        from game.views.map import Map
        # from game.views.battle import Battle

        self.change_views(Map, self.width, self.height, "Map")

    @staticmethod
    def exit():
        print("Quiting the game.", flush=True)
        pygame.quit()
        sys.exit()
