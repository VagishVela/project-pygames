""" Implements the Slots view """

from datetime import datetime
from importlib import import_module
from typing import Optional

import pygame

from game.common_types import Coordinate, ColorValue
from game.config import STORE_BG
from game.data import game_data
from game.utils import Text, MenuButton, Button
from game.views import View, logger, views_cache

# get logger
logger = logger.getChild("slots")


class Slots(View):
    """The Menu view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.escape_to = None
        self.bg_color = STORE_BG
        self.slot = 0

        # read the savefile
        game_data.read()

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
                view_path="map.Map",
            )
            if text != "EMPTY SLOT"
            else Button(
                xy=(self.width / 2, self.height / 2 - 120 + i * 60),
                dimensions=(200, 50),
                text=text,
            )
            for i, text in enumerate(self.slots)
        ]
        logger.debug(f" buttons: {self.buttons}")

    def _set_slot(self, num):
        def _():
            self.slot = num

        return _

    def on_update(self):
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

    # pylint: disable=too-many-arguments
    def change_views(
        self,
        next_view_path,
        caption: Optional[str] = None,
        size: Optional[Coordinate] = None,
        bg_color: Optional[ColorValue] = None,
        check_cache: bool = True,
    ):
        # try most common usage
        next_view_module, _class = next_view_path.split(".")
        next_view_module = import_module(f"game.views.{next_view_module}")

        # implement a try-catch block here if other modules are used for views than `game.views`

        if next_view_path == "map.Map":
            # preset values for map
            bg_color = "black"
            size = (*self.size,)

            next_view = (
                views_cache.get(
                    (next_view_path, caption, size, bg_color),
                    getattr(next_view_module, _class)(
                        size, caption, None, bg_color, load_from=self.slot
                    ),
                )
                if check_cache
                else getattr(next_view_module, _class)(
                    size, caption, None, bg_color, load_from=self.slot
                )
            )
        else:
            next_view = (
                views_cache.get(
                    (next_view_path, caption, size, bg_color),
                    getattr(next_view_module, _class).from_view(
                        self, caption, size, bg_color
                    ),
                )
                if check_cache
                else getattr(next_view_module, _class).from_view(
                    self, caption, size, bg_color
                )
            )

        self._running = False
        logger.debug(f" switching views from {self} to {next_view}")
        next_view.run()

    def pre_run(self, _spl_args):
        self.escape_to = _spl_args["escape"]

    def on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            self.change_views(self.escape_to)
