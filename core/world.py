import enum


class Facing(enum.Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class World:
    def __init__(self, name):
        self.name = name
        self.entities = []
        self.living_entities = []
