""" This package contains the views """
import json
from importlib import import_module
from typing import Optional

import pygame
from pygame import Vector2, Surface

from game.common_types import ColorValue, Coordinate, NumType
from game.config import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from game.custom_event import LEFT_CLICK, RIGHT_CLICK, SCROLL_UP, SCROLL_DOWN
from game.logger import logger
from game.utils import Cache, EventHandler
from game.utils.text import Font

# used to cache views
views_cache = Cache()

# get logger
logger = logger.getChild("views")


class View:
    """An object representing the current 'view' on display"""

    def __init__(
        self,
        size: Optional[Coordinate] = None,
        caption: Optional[str] = None,
        icon: Optional[Surface] = None,
        bg_color: Optional[ColorValue] = None,
    ):
        """
        Initialize the View

        :param size: View dimensions, (width, height)
        :param caption: View caption
        :param icon: View icon
        :param bg_color: View background color
        """
        logger.debug(f" initialise new view: {self}")
        if not size:
            size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.width: NumType
        self.height: NumType
        self.width, self.height = size
        self.size = Vector2(size)

        # set caption and icon
        self.caption = caption or self.__class__.__name__
        if self.caption:
            logger.debug(f" set caption: {self.caption}")
            pygame.display.set_caption(self.caption)
        if icon:
            logger.debug(f" set icon: {icon}")
            pygame.display.set_icon(icon)

        # set bg color
        self.bg_color = bg_color or "black"

        # initiate the screen and font
        self.screen = pygame.display.set_mode(self.size)
        # self.font = pygame.font.get_default_font()

        self.font = Font("assets/Pokemon Hollow.ttf", 23)

        # keep track of states, time and events
        self._running = False
        self._clock = pygame.time.Clock()
        self.events = EventHandler()

        @self.events.register(pygame.QUIT)
        def on_close(event):
            logger.debug(f" {event}")
            self._running = False

        # on_mouse_down
        self.events.register(pygame.MOUSEBUTTONDOWN)(self._on_mouse_down)
        # on_click
        self.events.register(LEFT_CLICK.type)(self.on_click)
        self.events.register(RIGHT_CLICK.type)(self.on_click)
        # on_scroll
        self.events.register(SCROLL_UP.type)(self.on_scroll)
        self.events.register(SCROLL_DOWN.type)(self.on_scroll)
        # on_keydown
        self.events.register(pygame.KEYDOWN)(self.on_keydown)

    def on_draw(self):
        """Draw things onto the View surface"""

    def exit(self):
        """Quit the view"""
        logger.debug(f" View {self} exits")
        self._running = False
        pygame.display.quit()

    @classmethod
    def from_view(cls, prev_view: "View", caption=None, size=None, bg_color=None):
        """Get a class instance with attributes of the another view"""
        return cls(
            size or prev_view.size,
            caption or cls.__name__,
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

    def pre_run(self, _spl_args):
        """Called just before running the view"""

    def run(self, _spl_args=None):
        """
        Runs the main loop for this view
        :param _spl_args: special serializable kwargs
        """

        if _spl_args:
            self.pre_run(_spl_args)

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

    @staticmethod
    def _on_mouse_down(event):
        match event.button:
            case 1:
                LEFT_CLICK.post({"pos": event.pos})
            case 3:
                RIGHT_CLICK.post({"pos": event.pos})
            case 4:
                SCROLL_UP.post({"pos": event.pos})
            case 5:
                SCROLL_DOWN.post({"pos": event.pos})

    def on_click(self, event):
        """Called when the mouse is clicked"""

    def on_scroll(self, event):
        """Called when the mouse is scrolled"""

    def on_keydown(self, event):
        """Called when a key is pressed"""

    # pylint: disable=too-many-arguments
    def change_views(
        self,
        next_view_path: str,
        caption: Optional[str] = None,
        size: Optional[Coordinate] = None,
        bg_color: Optional[ColorValue] = None,
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
        if "#" in next_view_path:
            next_view_path, _spl_args = next_view_path.split("#")
            _spl_args = json.loads(_spl_args)
        else:
            _spl_args = None
        next_view_module, _class_name = next_view_path.split(".")
        next_view_module = import_module(f"game.views.{next_view_module}")

        if not caption:
            #     default to class name
            caption = _class_name

        # implement a try-catch block here if other modules are used for views than `game.views`

        next_view: "View" = (
            views_cache.get(
                (next_view_path, caption, size, bg_color),
                getattr(next_view_module, _class_name).from_view(
                    self, caption, size, bg_color
                ),
            )
            if check_cache
            else getattr(next_view_module, _class_name).from_view(
                self, caption, size, bg_color
            )
        )
        self._running = False
        logger.debug(f" switching views from {self} to {next_view}")
        next_view.run(_spl_args or None)
