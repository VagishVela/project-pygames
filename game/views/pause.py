""" Implements the Pause view """

from game.utils import Text
from game.views import View


class Pause(View):
    """The paused menu view"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.options = ["Option 1", "Option 2", "Option 3"]
        # self.buttons = [Button(
        #     self.width / 2,
        #     self.height / 2 + i * 60,
        #     100,
        #     50,
        #     option,
        #     onclick=lambda: print("button pressed!", option)
        # ) for i, option in enumerate(self.options)]
        # print(self.buttons)

    # def on_update(self):
    #     for b in self.buttons:
    #         b.update()

    def on_draw(self):
        # for b in self.buttons:
        #     b.blit_into(self.screen)

        self.screen.fill("black")
        Text(
            "Paused",
            self.font,
            self.width / 2,
            self.height / 2 - 50,
            200,
            "red",
        ).blit_into(self.screen)
        Text(
            "Click to resume!",
            self.font,
            self.width / 2,
            self.height / 2 + 50,
            50,
            "white",
        ).blit_into(self.screen)

    def on_click(self, event):
        self.change_views("map.Map", caption="Map")
