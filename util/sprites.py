import os

import pygame
from pygame import Surface, image


def load(dir_path: str) -> dict[str, Surface]:
    sprites = {}
    for file in os.listdir(dir_path):
        if os.path.isfile(rf"{dir_path}\{file}"):
            sprites[file[:-4]] = image.load(rf"{dir_path}\{file}").convert_alpha()
    return sprites


def resize(to_resize: Surface, ratio: float) -> Surface:
    return pygame.transform.scale(to_resize, (to_resize.get_width() * ratio, to_resize.get_height() * ratio))
