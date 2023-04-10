""" Implements the Menu view """

import importlib

from game.helper import Text, Button
from views import View


class Menu(View):
    """The Menu view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = [{"name": "New Game", "module": "map", "screen": "Map"}]
        self.buttons = [
            Button(
                self.width / 2,
                self.height / 2 - 120 + i * 60,
                100,
                50,
                text=option["name"],
                module=option["module"],
                screen=option["screen"],
                onclick=self.on_button_click,
            )
            for i, option in enumerate(self.options)
        ]
        print(self.buttons)

    def on_button_click(self, button):
        new_view = importlib.import_module(f"game.views.{button.module}")
        self.change_views(
            getattr(new_view, button.screen),
            self.width,
            self.height,
            button.screen,
        )

    def on_update(self):
        for b in self.buttons:
            b.update()

    def on_draw(self):
        self.screen.fill("black")
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
