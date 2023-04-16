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
        self.options = [
            {"text": "Main Menu", "view_path": "menu.Menu"},
            {
                "text": "Save progress",
                "view_path": "map.Map",
                "on_click": partial(game_data.save, *game_data.temp),
            },
            {
                "text": "Load a previous game",
                "view_path": 'slots.Slots#{"escape": "pause.Pause"}',
            },
            {"text": "Store", "view_path": 'store.Store#{"escape": "pause.Pause"}'},
        ]
        self.buttons = [
            MenuButton(
                self,
                xy=(self.width / 2, self.height / 2 - 120 + i * 60),
                dimensions=(200, 50),
                view_path=option["view_path"],
                text=option["text"],
                on_click=option.get("on_click"),
            )
            for i, option in enumerate(self.options)
        ]
        logger.debug(f" buttons: {self.buttons}")
        self.escape_to = None

    def on_update(self):
        for b in self.buttons:
            # ensure display is initiated
            if self._running:
                b.update()

    def on_draw(self):
        Text(
            "Menu",
            self.font,
            self.width / 2,
            self.height / 2 - 200,
            40,
            "red",
        ).blit_into(self.screen)

        for b in self.buttons:
            b.blit_into(self.screen)

    def pre_run(self, _spl_args):
        self.escape_to = _spl_args["escape"]

    def on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.change_views(self.escape_to)
