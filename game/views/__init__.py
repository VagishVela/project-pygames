""" This package contains the views """
from importlib import import_module

import pygame
from pygame import Vector2

from game.common_types import ColorValue, NumType
from game.config import FPS
from game.utils import Cache, EventHandler

views_cache = Cache()


class View:
    """An object representing the current 'view' on display"""

    def __init__(
        self,
        width,
        height,
        caption: str = None,
        icon: pygame.Surface = None,
        bg_color: ColorValue = None,
    ):
        """Initialize the View"""
        self.width: NumType = width
        self.height: NumType = height
        self.size = Vector2(self.width, self.height)

        if caption:
            self.caption = caption
            pygame.display.set_caption(caption)
        else:
            self.caption = None
        if icon:
            pygame.display.set_icon(icon)
        self.bg_color = bg_color or "black"

        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.get_default_font()

        self._running = False
        self._clock = pygame.time.Clock()
        self.events = EventHandler()

        @self.events.register(pygame.QUIT)
        def on_close(event):
            print(event)
            self._running = False

        # on_click
        self.events.register(pygame.MOUSEBUTTONDOWN)(self.on_click)
        # on_keydown
        self.events.register(pygame.KEYDOWN)(self.on_keydown)

    def on_draw(self):
        """Draw things onto the View surface"""

    @staticmethod
    def exit():
        """Quit the view"""
        pygame.display.quit()

    @classmethod
    def from_view(
        cls, prev_view: "View", caption=None, width=None, height=None, bg_color=None
    ):
        """Get a class instance with attributes of the another view"""
        return cls(
            width or prev_view.width,
            height or prev_view.height,
            caption or prev_view.caption,
            None,  # icon
            bg_color or prev_view.bg_color,
        )

    def _refresh(self, frame_rate=FPS):
        self._clock.tick(frame_rate)
        pygame.display.flip()

    def _handle_events(self):
        self.events.run()

    def on_update(self):
        """To override"""

    def run(self):
        """Runs the main loop for this view"""

        self._running = True
        print("Loading done!", self, flush=True)
        while self._running:
            self._handle_events()
            if self._running:
                self.screen.fill(self.bg_color)
                self.on_draw()
                self.on_update()
                try:
                    self._refresh()
                except pygame.error as e:
                    # TODO: figure this out
                    print("clean exit failed:", e)
        self.exit()

    def on_click(self, event):
        """Called when the mouse is clicked"""

    def on_keydown(self, event):
        """Called when a key is pressed"""

    # pylint: disable=too-many-arguments
    def change_views(
        self,
        next_view_path,
        caption: str = None,
        width: float | int = None,
        height: float | int = None,
        bg_color=None,
        check_cache: bool = True,
    ):
        """
        Change views and display the next View

        :param next_view_path: path to the View class within game.views
        :param caption: Window title, stays the same by default
        :param height: Window height, stays the same by default
        :param width: Window width, stays the same by default
        :param bg_color: Window background color
        :param check_cache: Whether to check for cached objects
        :return:
        """

        # try most common usage
        next_view_module, _class = next_view_path.split(".")
        next_view_module = import_module(f"game.views.{next_view_module}")

        # implement a try-catch block here if other modules are used for views than `game.views`

        next_view = (
            views_cache.get(
                (next_view_path, caption, width, height, bg_color),
                getattr(next_view_module, _class).from_view(
                    self, caption, width, height, bg_color
                ),
            )
            if check_cache
            else getattr(next_view_module, _class).from_view(
                self, caption, width, height, bg_color
            )
        )
        self._running = False
        print("switching views from", self, "to", next_view, flush=True)
        next_view.run()
