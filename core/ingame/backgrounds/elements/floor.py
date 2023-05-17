import random

from pygame import Surface
from util.menu import add_check
from util.draw_util import draw_with_scroll
from util.sprites import load


class Floor:
    """Class 'Floor'.

        :ivar floor_sprites: Dict of sprites associated with their names.
        :type floor_sprites: dict[str, Surface].
        :ivar __floor: List of floors sprites.
        :type __floor: list[str].
        :ivar __ground: List of grounds sprites.
        :type __ground: list[str].
        :ivar surface: Floor's surface.
        :type surface: Surface.
        :ivar x: Floor's x coordinates.
        :type x: int.
        :ivar maps: 2d list where sprites are associated with their x, y coordinates.
        :type maps: list[list[str]].

    """
    floor_sprites: dict[str, Surface]
    __floor: list[str]
    __ground: list[str]
    surface: Surface
    x: int
    maps: list[list[str]]

    def __init__(self, sprites_path: str, width: int, height: int, loading: bool = False):
        """Constructor function for Floor class.

            :param sprites_path: Sprites file path.
            :type sprites_path: str.
            :param width: Floor's with.
            :type width: int.
            :param height: Floor's height.
            :type height: int.
            :param loading: If the level is loaded or not.
            :type loading: bool.

        """
        add_check("Loading sprites.", __name__ + "Floor.init")
        self.floor_sprites = load(sprites_path)
        self.__floor = [x for x in self.floor_sprites.keys() if "floor" in x]
        self.__ground = [x for x in self.floor_sprites.keys() if "floor" not in x]
        self.surface = Surface((width*2, height))
        self.x = -width
        self.maps = []

        add_check("Creating floor surface.", __name__ + "Floor.init")
        if not loading:
            for x in range(width*2//16):
                self.maps.append([])
                for y in range(height//16):
                    if y == 0:
                        index: str = random.choice(self.__floor)
                        self.maps[x].append(index)
                        self.surface.blit(self.floor_sprites[index], (16 * x, 0))
                    else:
                        index: str = random.choice(self.__ground)
                        self.maps[x].append(index)
                        self.surface.blit(self.floor_sprites[index], (16 * x, 16 * y))

    def draw(self, surface: Surface) -> None:
        """Draw this object on the client's screen.

            :param surface: Surface to draw.
            :type surface: Surface.

        """
        draw_with_scroll(surface, self.surface, self.x, surface.get_height()-80)
