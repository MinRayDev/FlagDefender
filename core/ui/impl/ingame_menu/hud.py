import time

import pygame
from catppuccin import Flavour

from core.chat.chat import MessageType
from core.ui.element.impl.rectangle import Rectangle
from core.ui.game_menu import GameMenu
from util.fonts import Fonts
from util.instance import get_game
from util.instance import get_client


class HUD(GameMenu):
    def __init__(self):
        super().__init__("HUD")
        self.x = 0
        self.y = 0
        self.width = get_client().screen.get_width()
        self.height = get_client().screen.get_height()
        self.health_rect_base = Rectangle("CENTER", self.height - self.height//30 - self.height//50, self.width//8, self.height//30, Flavour.frappe().surface2.rgb, Flavour.frappe().surface2.rgb)
        # self.health_rect = pygame.Rect("CENTER", self.height - self.height//30 - self.height//50, self.width//8, self.height//30)
        self.elems = []

    def draw(self, surface):
        # pygame.draw.rect(surface, Flavour.frappe().surface2.rgb, self.health_rect)
        self.health_rect_base.draw(surface)
        health_percentage = get_game().main_player.entity.health/get_game().main_player.entity.max_health
        pygame.draw.rect(surface, Flavour.frappe().red.rgb, pygame.Rect(self.health_rect_base.x, self.height - self.height//30 - self.height//50, int((self.width//8)*health_percentage), self.height//30))

    @classmethod
    def alpha_draw(cls, surface, color, rect: pygame.Rect):
        temp_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, color, temp_surface.get_rect())
        surface.blit(temp_surface, rect)
