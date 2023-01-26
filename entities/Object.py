from typing import Optional

from core.world import World


class Object:
    def __init__(self, x: int, y: int, world: Optional[World], width: int, height: int):
        self.x = x
        self.y = y
        self.world = world
        self.width = width
        self.height = height
