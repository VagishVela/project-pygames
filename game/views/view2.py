# pylint: skip-file
import pygame

from game.custom_event import COUNTER
from game.utils import Text
from game.views import View


class View2(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.count = 5

    def on_draw(self):
        if COUNTER.get():
            self.count -= 1
        text = Text(
            "This is View2", self.font, self.width / 2, self.height / 2, 60, "white"
        )
        text.blit_into(self.screen)

        text = Text(
            f"{self.count}",
            self.font,
            self.width / 2,
            self.height / 2 - 100,
            60,
            "white",
        )
        text.blit_into(self.screen)

    def on_click(self, event):
        self.change_views("view1.View1", "View1")

    def on_keydown(self, event):
        if event.key == pygame.K_f:
            print("F is pressed")
            COUNTER.post()
