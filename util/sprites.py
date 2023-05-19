import os

import pygame
from pygame import Surface, image


def load(dir_path: str) -> dict[str, Surface]:
    """Loads the sprites from the given directory path.

        :param dir_path: The directory path of the sprites.
        :type dir_path: str.

        :return: The sprites.
        :rtype: dict[str, Surface].

    """
    sprites = {}
    for file in os.listdir(dir_path):
        if os.path.isfile(rf"{dir_path}\{file}") and (file.endswith(".png") or file.endswith(".jpg")):
            sprites[file[:-4]] = image.load(rf"{dir_path}\{file}").convert_alpha()
    return sprites


def resize(to_resize: Surface, ratio: float) -> Surface:
    """Resizes the given surface by the given ratio.

        :param to_resize: The surface to resize.
        :type to_resize: Surface.

        :param ratio: The ratio to resize the surface by.
        :type ratio: float.

    """
    return pygame.transform.scale(to_resize, (to_resize.get_width() * ratio, to_resize.get_height() * ratio))
