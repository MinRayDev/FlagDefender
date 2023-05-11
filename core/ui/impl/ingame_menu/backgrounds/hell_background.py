from pygame import Surface

from core.ui.impl.ingame_menu.background import Background
from core.world import World
from util.instance import get_game, get_client


class HellBackground(Background):
    def __init__(self, world: World):
        from util.menu import add_check
        add_check("Loading background.", __name__ + "HellBackground.init")
        super().__init__(r"./resources/sprites/world/background/hell",
                         r"./resources/sprites/world/background/hell/floor",
                         world, (130, 240, 255))
        surface = get_client().screen
        self.last_time = 0
        self.last_sprite = 20
        add_check("Resizing background's sprites.", __name__ + "OverworldBackground.init")
        self.parts = [self.resize(self.sprites["0"], surface.get_width()),
                      self.resize(self.sprites["1"], surface.get_width() * 1.5),
                      self.resize(self.sprites["3"], surface.get_width() * 1.8)]
        self.ratios = [(surface.get_width() / ((self.world.size[0] * 2 + self.parts[1].get_width() * 2) * 2 + self.world.size[0] / 1.5)) * 0.2,
                       (surface.get_width() / ((self.world.size[0] * 2 + self.parts[2].get_width() * 2) * 2 + self.world.size[0] / 4))]

    def draw(self, surface: Surface) -> None:
        surface.blit(self.parts[0], (0, 0))
        surface.blit(self.parts[1], (- ((self.parts[1].get_width() - surface.get_width()) // 2) + get_game().current_level.scroll * self.ratios[0] - get_game().current_level.main_player.entity.width // 2, 0))
        surface.blit(self.parts[2], (- ((self.parts[2].get_width() - surface.get_width()) // 2) + get_game().current_level.scroll * self.ratios[1] - get_game().current_level.main_player.entity.width // 2, 0))
        self.floor.draw(surface)
