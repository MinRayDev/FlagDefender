import pygame
from catppuccin import Flavour

from core.ui.element.impl.rectangle import Rectangle
from core.ui.element.impl.text import Text
from core.ui.game_menu import GameMenu
from entities.livingentities.entity_player import PlayerEntity
from util import client_utils
from util.instance import get_client
from util.instance import get_game


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
        Text("Kills: " + str(get_game().main_player.kills), self.width-self.width//8, self.height//20, Flavour.frappe().text.rgb).draw(surface)
        Text("Round: " + str(get_game().wave), self.width-self.width//8, self.height//10, Flavour.frappe().text.rgb).draw(surface)
        Text("Gold: " + str(get_game().main_player.gold), self.width-self.width//8, self.height//10 + self.height//10 - self.height//20, Flavour.frappe().text.rgb).draw(surface)
        t = 0
        for entity in client_utils.get_out_of_screen():
            if isinstance(entity, PlayerEntity):
                Text(str(entity)[:2], self.width - 40, self.height // 2 + 15 + t * 40, Flavour.frappe().text.rgb).draw(surface)
                t += 1

    @classmethod
    def alpha_draw(cls, surface, color, rect: pygame.Rect):
        temp_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, color, temp_surface.get_rect())
        surface.blit(temp_surface, rect)
