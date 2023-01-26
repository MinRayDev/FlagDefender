import os
import pygame


def load(dir_path: str):
    sprites = {}
    for file in os.listdir(dir_path):
        sprites[file[:-4]] = pygame.image.load(rf"{dir_path}\{file}").convert_alpha()
    return sprites
