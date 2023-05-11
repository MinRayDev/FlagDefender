import pygame
from pygame import Surface

from core.ui.element.impl.rectangle import Rectangle
from core.ui.element.impl.text import Text
from core.ui.game_menu import GameMenu
from util.colors import Colors


class HUD(GameMenu):
    def __init__(self):
        from util.instance import get_client
        super().__init__("HUD")

        self.x = 0
        self.y = 0
        self.width = get_client().screen.get_width()
        self.height = get_client().screen.get_height()
        self.health_rect_base = Rectangle("CENTER", self.height - self.height//30 - self.height//50, self.width//8, self.height//30, Colors.surface2, Colors.surface2)
        # self.health_rect = pygame.Rect("CENTER", self.height - self.height//30 - self.height//50, self.width//8, self.height//30)
        self.elems = []

    def draw(self, surface: Surface) -> None:
        from util.instance import get_game
        self.health_rect_base.draw(surface)
        health_percentage = get_game().current_level.main_player.entity.health/get_game().current_level.main_player.entity.max_health
        pygame.draw.rect(surface, Colors.red, pygame.Rect(self.health_rect_base.x, self.height - self.height//30 - self.height//50, int((self.width//8)*health_percentage), self.height//30))
        Text("Kills: " + str(get_game().current_level.main_player.kills), self.width-self.width//8, self.height//20, Colors.text).draw(surface)
        Text("Round: " + str(get_game().current_level.round_manager.get_round().number), self.width-self.width//8, self.height//10, Colors.text).draw(surface)

    @classmethod
    def alpha_draw(cls, surface, color, rect: pygame.Rect):
        temp_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, color, temp_surface.get_rect())
        surface.blit(temp_surface, rect)
