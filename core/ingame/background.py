import pygame
from pygame import Surface

from core.ingame.backgrounds.elements.floor import Floor
from core.world import World
from util.menu import add_check
from util.sprites import load


class Background:
    """Class 'Background'.

        Background class is the class for parent backgrounds.

        :ivar sprites: Dict of sprites associated with their names.
        :type sprites: dict[str, Surface].
        :ivar floor: Background's floor.
        :type floor: Floor.
        :param world: World of the background.
        :type world: World.
        :ivar sky_color: Sky color (rgb).
        :type sky_color: tuple[int, int, int].

    """
    sprites: dict[str, Surface]
    floor: Floor
    world: World
    sky_color: tuple[int, int, int]

    def __init__(self, sprites_path: str, floor_path: str, world: World, sky_color: tuple[int, int, int], loading: bool = False):
        """Constructor function for OverworldBackground class.

            :param sprites_path: Sprites file path.
            :type sprites_path: str.
            :param floor_path: Floors sprites file path.
            :type floor_path: str.
            :param world: World of the background.
            :type world: World.
            :ivar sky_color: Night sky color (rgb).
            :type sky_color: tuple[int, int, int].
            :param loading: If the level is loaded or not.
            :type loading: bool.

        """
        add_check("Loading sprites.", __name__ + "Background.init")
        self.sprites = load(sprites_path)
        self.floor: Floor
        if not loading:
            add_check("Creating floor.", __name__ + "Background.init")
            self.floor = Floor(floor_path, world.size[0]*2, world.floor)
        add_check("Floor creating ended.", __name__ + "Background.init")
        self.world = world
        self.sky_color: tuple[int, int, int] = sky_color

    def draw(self, surface: Surface) -> None:
        """Draw this object on the client's screen.

            :param surface: Surface to draw.
            :type surface: Surface.

        """
        pass

    @classmethod
    def resize(cls, to_resize: Surface, new_width: int) -> Surface:
        """Resize 'to_resize' with the new width.

            :param to_resize: Surface to resize.
            :type to_resize: Surface.
            :param new_width: Surface's new width.
            :type new_width: int.

        """
        ratio = new_width / to_resize.get_width()
        return pygame.transform.scale(to_resize, (new_width, to_resize.get_height() * ratio))
