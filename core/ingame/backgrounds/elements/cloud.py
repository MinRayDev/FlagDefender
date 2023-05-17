import random

from pygame import Surface


class Cloud:
    """Class 'Cloud'.

        :ivar sprite: Cloud's sprite.
        :type sprite: Surface.
        :ivar x: Cloud's x coordinates.
        :type x: int.
        :ivar y: Cloud's y coordinates.
        :type y: int.
        :ivar offset: Cloud's offset.
        :type offset: float.

    """
    sprite: Surface
    x: int
    y: int
    offset: float

    def __init__(self, sprite: Surface, x: int, y: int):
        """Constructor function for HellBackground class.

            :param sprite: Cloud's sprite.
            :type sprite: Surface.
            :param x: Cloud's x coordinates.
            :type x: int.
            :param y: Cloud's y coordinates.
            :type y: int.

        """
        self.sprite = sprite
        self.x = x
        self.y = y
        self.offset = random.randint(7, 50) / 100
