from __future__ import annotations

import random

from pygame import Surface

from util.draw_util import draw_with_scroll
from util.sprites import load


class Floor:
    def __init__(self, sprites_path: str, width: int, height: int, loading: bool = False):
        from util.menu import add_check
        add_check("Loading sprites.", __name__ + "Floor.init")
        self.floor_sprites = load(sprites_path)
        self.floor = [x for x in self.floor_sprites.keys() if "floor" in x]
        self.ground = [x for x in self.floor_sprites.keys() if "floor" not in x]
        self.surface = Surface((width*2, height))
        self.x = -width
        self.maps: list[list[str]] = []
        add_check("Creating floor surface.", __name__ + "Floor.init")
        if not loading:
            for x in range(width*2//16):
                self.maps.append([])
                for y in range(height//16):
                    if y == 0:
                        index: str = random.choice(self.floor)
                        self.maps[x].append(index)
                        self.surface.blit(self.floor_sprites[index], (16 * x, 0))
                    else:
                        index: str = random.choice(self.ground)
                        self.maps[x].append(index)
                        self.surface.blit(self.floor_sprites[index], (16 * x, 16 * y))

    def draw(self, surface: Surface) -> None:
        draw_with_scroll(surface, self.surface, self.x, surface.get_height()-80)
