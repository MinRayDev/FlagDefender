import pygame
from pygame import Surface


class TreeElement:
    def __init__(self):
        pass

    @classmethod
    def resize(cls, to_resize: Surface, multiplier: float) -> Surface:
        return pygame.transform.scale(to_resize, (to_resize.get_width()*multiplier, to_resize.get_height()*multiplier))
