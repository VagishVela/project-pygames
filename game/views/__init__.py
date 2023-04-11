""" This package contains the views """
from importlib import import_module

import pygame
from pygame import Vector2

from game.logger import logger
from game.common_types import ColorValue, Coordinate
from game.config import FPS
from game.utils import Cache, EventHandler

# used to cache views
views_cache = Cache()

# get logger
logger = logger.getChild("views")


class View:
    """An object representing the current 'view' on display"""

    def __init__(
        self,
        size: Coordinate = None,
        caption: str = None,
        icon: pygame.Surface = None,
        bg_color: ColorValue = None,
    ):
        """
        Initialize the View

        :param size: View dimensions, (width, height)
        :param caption: View caption
        :param icon: View icon
        :param bg_color: View background color
        """
        logger.debug(f" initialise new view: {self}")
        self.width, self.height = size
        self.size = Vector2(size)

        # set caption and icon
        self.caption = caption
        if self.caption:
            logger.debug(f" set caption: {self.caption}")
            pygame.display.set_caption(caption)
        if icon:
            logger.debug(f" set icon: {icon}")
            pygame.display.set_icon(icon)

        # set bg color
        self.bg_color = bg_color or "black"

        # initiate the screen and font
        self.screen = pygame.display.set_mode(self.size)
        self.font = pygame.font.get_default_font()

        # keep track of states, time and events
        self._running = False
        self._clock = pygame.time.Clock()
        self.events = EventHandler()

        @self.events.register(pygame.QUIT)
        def on_close(event):
            logger.debug(f" {event}")
            self._running = False

        # on_click
        self.events.register(pygame.MOUSEBUTTONDOWN)(self.on_click)
        # on_keydown
        self.events.register(pygame.KEYDOWN)(self.on_keydown)

    def on_draw(self):
        """Draw things onto the View surface"""

    def exit(self):
        """Quit the view"""
        logger.debug(f" View {self} exits")
        pygame.display.quit()

    @classmethod
    def from_view(cls, prev_view: "View", caption=None, size=None, bg_color=None):
        """Get a class instance with attributes of the another view"""
        return cls(
            size or prev_view.size,
            caption or prev_view.caption,
            None,  # icon
            bg_color or prev_view.bg_color,
        )

    def _refresh(self, frame_rate=FPS):
        # check if display is still initiated
        if self._running:
            self._clock.tick(frame_rate)
            pygame.display.flip()

    def _handle_events(self):
        self.events.run()

    def on_update(self):
        """To override"""

    def run(self):
        """Runs the main loop for this view"""

        self._running = True
        logger.debug(f" Loading done! {self}")
        while self._running:
            self._handle_events()
            if self._running:
                self.screen.fill(self.bg_color)
                self.on_draw()
                self.on_update()
                self._refresh()
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
        size: Coordinate = None,
        bg_color=None,
        check_cache: bool = True,
    ):
        """
        Change views and display the next View

        :param next_view_path: path to the View class within game.views
        :param caption: Window title, stays the same by default
        :param size: Window size, stays the same by default
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
