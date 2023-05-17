import pygame
from pygame import Surface


class TreeElement:
    """Class 'TreeElement'."""

    def __init__(self):
        """Constructor function for TreeElement class."""
        pass

    @classmethod
    def resize(cls, to_resize: Surface, multiplier: float) -> Surface:
        """Resize a pygame surface.

            :param to_resize: Surface to resize.
            :type to_resize: Surface.
            :param multiplier: Multiplier to use to resize the surface.
            :type multiplier: float.

            :return: Resized surface.
            :rtype: Surface.

        """
        return pygame.transform.scale(to_resize, (to_resize.get_width()*multiplier, to_resize.get_height()*multiplier))
