""" Implements the Menu view """

from game.helper import Text, Button
from views import View


def fun(t):
    """for debug, rename/reuse this"""

    # """ use a function like this that returns a function pointer, instead of lambdas """
    def _():
        print(t)

    return _


import importlib


class Menu(View):
    """The Menu view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.options = [{"name": "New Game", "module": "map", "screen": "Map"}]
        self.buttons = [
            Button(
                self.width / 2,
                self.height / 2 + i * 60,
                100,
                50,
                text=option["name"],
                module=option["module"],
                screen=option["screen"],
                on_click=self.on_button_click,
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
            self.height / 2 - 50,
            200,
            "red",
        ).blit_into(self.screen)

        for b in self.buttons:
            b.blit_into(self.screen)
