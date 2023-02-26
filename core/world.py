import enum
from typing import Tuple


class Facing(enum.IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class World:
    def __init__(self, name, floor: int, size: Tuple[int, int]):
        self.name = name
        self.entities = []
        self.floor = floor
        self.size = size
