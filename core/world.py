import enum
from typing import Tuple


class Facing(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class World:
    def __init__(self, name, floor: int, size: Tuple[int, int]):
        self.name = name
        self.entities = []
        self.living_entities = []
        self.floor = floor
        self.size = size
