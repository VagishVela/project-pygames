""" Implements the Pause view """
from functools import partial

import pygame

from game.data import game_data
from game.utils import Text, MenuButton
from game.views import View, logger

# get logger
logger = logger.getChild("pause")


class Pause(View):
    """The paused menu view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.escape_to = None
        self.options = None
        self.buttons = None

    @staticmethod
    def _save():
        if not game_data.get_temp("ghost"):
            return partial(game_data.save_game_state, game_data.temp)
        logger.debug("ghost tried to save")
        game_data.save_temp(True, "GHOST_SAVE")
        return None

    def pre_run(self, _spl_args):
        escape_to_name: str = game_data.get_temp("paused_from")
        self.escape_to = f"{escape_to_name.lower()}.{escape_to_name}"
        self.options = [
            {"text": "Main Menu", "view_path": "menu.Menu"},
            {
                "text": "Save progress",
                "view_path": f"{self.escape_to}",
                "on_click": self._save(),
            },
            {
                "text": "Load a previous game",
                "view_path": "slots.Slots",
            },
            {"text": "Store", "view_path": "store.Store"},
        ]
        self.buttons = [
            MenuButton(
                self,
                xy=(self.width / 2, self.height / 2 - 120 + i * 60),
                dimensions=(250, 50),
                view_path=option["view_path"],
                text=option["text"],
                on_click=option.get("on_click"),
            )
            for i, option in enumerate(self.options)
        ]
        logger.debug(f" buttons: {self.buttons}")

    def on_update(self):
        for b in self.buttons:
            # ensure display is initiated
            if self._running:
                b.update()

    def on_draw(self):
        Text(
            "Paused",
            "pokemon-hollow",
            self.width / 2,
            self.height / 2 - 200,
            40,
            "red",
        ).blit_into(self.screen)

        for b in self.buttons:
            b.blit_into(self.screen, size=20)

    def on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.change_views(self.escape_to)
