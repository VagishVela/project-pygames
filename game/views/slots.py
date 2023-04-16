""" Implements the Slots view """

from datetime import datetime

import pygame

from game.config import STORE_BG
from game.data import game_data
from game.utils import Text, MenuButton, Button
from game.views import View, logger

# get logger
logger = logger.getChild("slots")


class Slots(View):
    """The Menu view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.escape_to = None
        self.bg_color = STORE_BG
        self.slot = 0
        self._generate_buttons()

    def _generate_buttons(self):
        self.slots = [
            str(
                datetime.fromtimestamp(slot["time"]).strftime(
                    "Load the game saved on %d-%b-%Y at %r"
                )
            )
            for slot in game_data.data.slots
        ]
        while len(self.slots) != 5:
            self.slots.append("EMPTY SLOT")
        self.buttons = [
            MenuButton(
                self,
                xy=(self.width / 2, self.height / 2 - 120 + i * 60),
                dimensions=(400, 50),
                text=text,
                on_click=self._set_slot(i),
                view_path=f'map.Map#{{"load":{i}}}',
            )
            if text != "EMPTY SLOT"
            else Button(
                xy=(self.width / 2, self.height / 2 - 120 + i * 60),
                dimensions=(200, 50),
                text=text,
            )
            for i, text in enumerate(self.slots)
        ]
        # logger.debug(f" buttons: {self.buttons}")

    def _set_slot(self, num):
        def _():
            self.slot = num

        return _

    def on_update(self):
        self._generate_buttons()
        for b in self.buttons:
            # ensure display is initiated
            if self._running:
                b.update()

    def on_draw(self):
        Text(
            "Select from the saved games",
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
