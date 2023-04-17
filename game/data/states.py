"""This module implements States used in various views"""
from dataclasses import dataclass

from game.data import logger
from game.entities.player import PlayerAttributes

logger = logger.getChild("states")


@dataclass
class LevelState:
    """Represents the level state"""

    # to store current player absolute position
    _loc: list
    # to store removed items
    _removed: set[tuple]

    def get(self):
        """get the current state"""
        logger.debug(f"get {self.loc}, {self.removed}")
        return self.loc, self.removed

    def set(self, loc: list, removed: set[tuple]):
        """get the current state"""
        logger.debug(f"set {loc}, {removed}")
        self._loc = loc
        self._removed = removed

    @property
    def loc(self):
        """absolute player position"""
        return self._loc

    @property
    def removed(self):
        """get the positions for removed objects"""
        return self._removed

    def reset(self):
        """reset to default values"""
        self._loc = [0, 0]
        self._removed = set()


@dataclass
class GameState:
    """Represents the game state"""

    level_state: LevelState
    attributes: PlayerAttributes
    # todo: add invenetory and other states
