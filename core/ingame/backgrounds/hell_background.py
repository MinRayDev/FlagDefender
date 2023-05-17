import traceback

from pygame import Surface

from core.world import World
from util.menu import add_check
from core.ingame.background import Background
from util.instance import get_game, get_client


class HellBackground(Background):
    """Class 'HellBackground'.

        HellBackground class is the class for backgrounds of hell's dimensions.

        :ivar __parts: List of parts making up the background.
        :type __parts: list[Surface].
        :ivar __ratios: List of ratios modifying the scroll.
        :type __ratios: list[float].

    """
    __parts: list[Surface]
    __ratios: list[float]

    def __init__(self, world: World):
        """Constructor function for HellBackground class.

            :param world: World of the background.
            :type world: World.

        """
        add_check("Loading background.", __name__ + "HellBackground.init")
        super().__init__(r"./resources/sprites/world/background/hell", r"./resources/sprites/world/background/hell/floor", world, (130, 240, 255))
        add_check("Resizing background's sprites.", __name__ + "HellBackground.init")
        surface = get_client().get_screen()
        self.__parts = [
            self.resize(self.sprites["0"], surface.get_width()),
            self.resize(self.sprites["1"], int(surface.get_width() * 1.5)),
            self.resize(self.sprites["3"], int(surface.get_width() * 1.8))
        ]
        self.__ratios = [
            (surface.get_width() / ((self.world.size[0] * 2 + self.__parts[1].get_width() * 2) * 2 + self.world.size[0] / 1.5)) * 0.2,
            (surface.get_width() / ((self.world.size[0] * 2 + self.__parts[2].get_width() * 2) * 2 + self.world.size[0] / 4))
        ]

    def draw(self, surface: Surface) -> None:
        """Draw this object on the client's screen.

            :param surface: Surface to draw.
            :type surface: Surface.

        """
        surface.blit(self.__parts[0], (0, 0))
        surface.blit(self.__parts[1], (- ((self.__parts[1].get_width() - surface.get_width()) // 2) + get_game().current_level.scroll * self.__ratios[0] - get_game().current_level.main_player.entity.width // 2, 0))
        surface.blit(self.__parts[2], (- ((self.__parts[2].get_width() - surface.get_width()) // 2) + get_game().current_level.scroll * self.__ratios[1] - get_game().current_level.main_player.entity.width // 2, 0))
        self.floor.draw(surface)
