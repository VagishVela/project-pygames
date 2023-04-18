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
    """The Slots view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.escape_to = None
        self.bg_color = STORE_BG
        self._generate_buttons()

    def _generate_buttons(self):
        self.slots = [
            str(
                datetime.fromtimestamp(slot.time).strftime(
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
                view_path=f'map.Map#{{"load":{i}}}',
            )
            if text != "EMPTY SLOT"
            else Button(
                xy=(self.width / 2, self.height / 2 - 120 + i * 60),
                dimensions=(150, 50),
                text=text,
            )
            for i, text in enumerate(self.slots)
        ] + [
            Button(
                xy=(self.width / 2 + 200, self.height - 100),
                dimensions=(150, 50),
                text="Clear saved games",
                on_click=game_data.clean,
            )
        ]

    def on_update(self):
        self._generate_buttons()
        for b in self.buttons:
            # ensure display is initiated
            if self._running:
                b.update()

    def on_draw(self):
        Text(
            "Select from the saved games",
            "pokemon-hollow",
            self.width / 2,
            self.height / 2 - 200,
            40,
            "red",
        ).blit_into(self.screen)

        for b in self.buttons:
            b.blit_into(self.screen, size=13)

    def pre_run(self, _spl_args):
        escape_to_name: str = game_data.get_temp("return_to")
        self.escape_to = f"{escape_to_name.lower()}.{escape_to_name}"

    def on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.change_views(self.escape_to)
