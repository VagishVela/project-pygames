"""Generate a level"""
# p is player
# e is Enemy -> En can be a way to have many different enemies
# w is wall -> Wn can be a way to have more obstacles
# x is walkable
import random

import numpy as np
from numpy.typing import NDArray

from game.custom_event import ENEMY_ENCOUNTERED


class Level:
    """Class for generating a level"""

    def __init__(self):
        """Initialize the level"""

        self.loc = [0, 0]
        self.matrix = np.full((9, 9), ord("x"), dtype=np.int8)
        self.rng = random.Random(str(self.loc))

    def set_loc(self, loc) -> None:
        """set the location"""

        self.loc = list(loc)

    def _get_tile(self, at) -> int:
        """Get a tile"""

        if at == (4, 4):
            return ord("p")
        seed = str([self.loc[0] - at[1], self.loc[1] - at[0]])
        self.rng.seed(seed)
        return ord(self.rng.choice("x" * 800 + "w" * 185 + "e" * 15))

    def generate(self) -> NDArray:
        """Generate a level"""

        for idx, _ in np.ndenumerate(self.matrix):
            self.matrix[idx] = self._get_tile(idx)
        self.matrix[(4, 4)] = ord("p")
        return self.matrix

    def move(self, dx, dy) -> bool:
        """Move the whole map in the given direction"""

        if self.matrix[(4 - dy, 4 - dx)] == ord("e"):
            ENEMY_ENCOUNTERED.post()
            return False
        if self.matrix[(4 - dy, 4 - dx)] == ord("x"):
            self.set_loc((self.loc[0] + dx, self.loc[1] + dy))
            return True
        return False
