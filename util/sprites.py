import os
from pygame import Surface, SurfaceType, image


def load(dir_path: str) -> dict[str, Surface | SurfaceType]:
    sprites = {}
    for file in os.listdir(dir_path):
        sprites[file[:-4]] = image.load(rf"{dir_path}\{file}").convert_alpha()
    return sprites
