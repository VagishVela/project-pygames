""" Implements the Map view, TopDown2D """
import itertools

import numpy as np
import pygame

from game.config import SCREEN_WIDTH, SCREEN_HEIGHT
from game.custom_event import ENEMY_ENCOUNTERED
from game.data import game_data
from game.entities.enemy import Enemy
from game.entities.player import Player
from game.entities.walls import Wall
from game.level_gen import Level
from game.views import View, logger

# get logger
logger.getChild("map")


class Screen:
    """Represents the screen for the map view"""

    screen = {}
    enemies = {}
    walls = {}
    level = Level()
    _initiated = False
    _regenerate = False

    @classmethod
    def initiate(cls):
        """initiate the sprites"""
        for i, j in itertools.product(range(9), range(9)):
            cls.enemies[(i, j)] = Enemy()
            cls.walls[(i, j)] = Wall()
        cls._initiated = True
        cls._regenerate = True

    @classmethod
    def load(cls, loc=None):
        """load and generate the screen"""
        if cls._regenerate:
            cls.clear()
        if loc:
            cls.clear()
            cls.level.set_loc(loc)
        if not cls._initiated:
            cls.initiate()
        map_ = cls.level.generate()
        for idx, x in np.ndenumerate(map_):
            match chr(x):
                case "w":
                    cls.screen[idx] = cls.walls[idx]
                case "e":
                    cls.screen[idx] = cls.enemies[idx]

    @classmethod
    def move(cls, dx, dy):
        """move the map in 2D"""
        # move the level

        if cls.level.move(dx, dy):
            cls._regenerate = True
            # update the screen
            cls.load()

    @classmethod
    def clear(cls):
        """clear the screen"""
        cls.screen.clear()

    @classmethod
    def draw(cls, screen):
        """draw the screen"""
        for idx, sprite in cls.screen.items():
            sprite.draw(screen, idx[1] * SCREEN_WIDTH / 9, idx[0] * SCREEN_HEIGHT / 9)


class Map(View):
    """Map view"""

    player = Player()
    screen_map = Screen

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.speed = 5

    def on_draw(self):
        self.screen_map.draw(self.screen)
        self.player.draw(self.screen)

    def on_keydown(self, event):
        match event.key:
            case pygame.K_UP | pygame.K_w:
                self.screen_map.move(0, 1)
            case pygame.K_DOWN | pygame.K_s:
                self.screen_map.move(0, -1)
            case pygame.K_LEFT | pygame.K_a:
                self.screen_map.move(1, 0)
            case pygame.K_RIGHT | pygame.K_d:
                self.screen_map.move(-1, 0)
            case pygame.K_ESCAPE:
                self.save_data(temp=True)
                logger.debug(" game paused")
                self.change_views("pause.Pause", caption="Paused")
                return
        if ENEMY_ENCOUNTERED.get():
            logger.debug(" enemy encountered!")
            self.change_views("battle.Battle", caption="Battle", check_cache=False)

    def save_data(self, temp=False):
        """Save the data"""

        logger.debug(" saving data...")
        if not temp:
            game_data.save(self.screen_map.level.loc, [])
        else:
            game_data.save_temp(self.screen_map.level.loc, [])
        logger.debug(" saved data!")

    def load_data(self, state):
        """Load a saved state from the data"""

        logger.debug(" loading data")
        game_data.load(state)

        # clear screen and set level state
        self.screen_map.load(game_data.get("loc"))
        # redraw
        self.on_draw()

    def pre_run(self, _spl_args):
        if _spl_args.get("reset"):
            self.screen_map.load((0, 0))
        elif _spl_args.get("load"):
            self.load_data(_spl_args["load"])
