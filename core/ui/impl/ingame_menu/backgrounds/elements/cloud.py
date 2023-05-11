import random

from pygame import Surface


class Cloud:
    sprite: Surface
    x: int
    y: int
    offset: float

    def __init__(self, sprite: Surface, x: int, y: int):
        self.sprite = sprite
        self.x = x
        self.y = y
        self.offset = random.randint(7, 50) / 100
