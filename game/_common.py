""" Commonly used types in pygame """

from os import PathLike
from typing import IO, Sequence, Tuple, Union

from pygame.color import Color
from pygame.math import Vector2

# For functions that take a file name
AnyPath = Union[str, bytes, PathLike[str], PathLike[bytes]]

# Most pygame functions that take a file argument should be able to handle a FileArg type
FileArg = Union[AnyPath, IO[bytes], IO[str]]

Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]

# This typehint is used when a function would return an RGBA tuple
RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]
