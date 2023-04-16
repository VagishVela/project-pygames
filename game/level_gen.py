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
        # set to store removed items
        self.removed = set()

    def set_loc(self, loc) -> None:
        """set the location"""

        self.loc = list(loc)

    def _get_tile(self, at: tuple) -> int:
        """Get a tile"""

        if at == (4, 4):
            return ord("p")

        if self._get_abs_pos(at) in self.removed:
            return ord("x")

        seed = str(list(self._get_abs_pos(at)))
        self.rng.seed(seed)
        return ord(self.rng.choice("x" * 800 + "w" * 185 + "e" * 15))

    def _get_abs_pos(self, rel_pos) -> tuple:
        """get absolute position on the map"""
        # rel_pos is transposed as matrix is stored column major
        return self.loc[0] - rel_pos[1], self.loc[1] - rel_pos[0]

    def generate(self) -> NDArray:
        """Generate a level"""

        for idx, _ in np.ndenumerate(self.matrix):
            self.matrix[idx] = self._get_tile(idx)
        self.matrix[(4, 4)] = ord("p")
        return self.matrix

    def move(self, dx, dy) -> bool:
        """Move the whole map in the given direction"""

        if self.matrix[(4 - dy, 4 - dx)] == ord("e"):
            ENEMY_ENCOUNTERED.post({"pos": (4 - dy, 4 - dx)})
            return False
        if self.matrix[(4 - dy, 4 - dx)] == ord("x"):
            self.set_loc((self.loc[0] + dx, self.loc[1] + dy))
            return True
        return False

    def remove_object(self, abs_pos: tuple) -> None:
        """
        remove an object from the map
        :param abs_pos: absolute position of that object from the map_origin, Level().loc-rel_pos

        :return:
        """
        self.removed.add(abs_pos)

    def remove_enemy(self, rel_pos: tuple):
        """remove enemy from the map"""
        # check enemy
        assert self.matrix[(*rel_pos,)] == ord(
            "e"
        ), f"No enemy was found at position {rel_pos}"
        self.remove_object(self._get_abs_pos(rel_pos))
