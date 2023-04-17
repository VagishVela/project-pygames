""" Implements the Map view, TopDown2D """
import itertools

import numpy as np
import pygame

from game.config import SCREEN_WIDTH, SCREEN_HEIGHT
from game.custom_event import ENEMY_ENCOUNTERED, PASS_VIEW
from game.data import game_data
from game.data.states import GameState
from game.entities.enemy import Enemy
from game.entities.player import Player
from game.entities.walls import Wall
from game.level_gen import Level, LevelState
from game.utils.bar import HealthBar
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
    regenerate = False

    @classmethod
    def initiate(cls):
        """initiate the sprites"""
        for i, j in itertools.product(range(9), range(9)):
            cls.enemies[(i, j)] = Enemy()
            cls.walls[(i, j)] = Wall()
        cls._initiated = True
        cls.regenerate = True

    @classmethod
    def load(cls, level_state: LevelState = None):
        """load and generate the screen"""
        if cls.regenerate:
            cls.clear()
        if level_state:
            cls.clear()
            cls.level.state.reset()
            cls.level.state.set(level_state.loc, level_state.removed)
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
            logger.debug(str(cls.level.state))
            cls.regenerate = True
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

        # to be used for battle view
        self.enemy_pos = None

    def on_draw(self):
        scale = (64, 96) if self.player.scale != (64, 96) else None
        self.screen_map.draw(self.screen)
        self.player.draw(self.screen, scale=scale)

        # draw the health bar
        HealthBar(self.player.max_health).draw(
            self.screen, self.player.abilities["health"], (20, 20), 150, 20
        )

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
                # needed for saving game from a different view
                self.save_data(temp=True)
                game_data.save_temp("Map", "paused_from")
                logger.debug(" game paused")
                self.change_views("pause.Pause", caption="Paused")
                return
        if e := ENEMY_ENCOUNTERED.get():
            self._on_enemy_encounter(e)

    def _on_enemy_encounter(self, event):
        """called when enemy is encountered"""
        # get enemy position
        self.enemy_pos = event.pos
        logger.debug(" enemy encountered!")
        PASS_VIEW.post({"view": self})
        # needed for saving game from a different view
        self.save_data(temp=True)
        self.change_views(
            "battle.Battle",
            caption="Battle",
            check_cache=False,
        )

    def save_data(self, temp=False):
        """Save the data"""

        state = GameState(self.screen_map.level.state)

        logger.debug(" saving data...")
        if not temp:
            game_data.save_game_state(state)
        else:
            game_data.save_temp(state)
        logger.debug(" saved data!")

    def load_data(self, state_index):
        """Load a saved state from the data"""

        logger.debug(" loading data")
        game_data.load(state_index)

        # clear screen and set level state
        self.screen_map.load(LevelState(game_data.get("loc"), game_data.get("removed")))
        # redraw
        self.on_draw()

    def pre_run(self, _spl_args):
        if _spl_args:
            if "reset" in _spl_args:
                self.screen_map.load(LevelState([0, 0], set()))
            elif "load" in _spl_args:
                self.load_data(_spl_args["load"])
