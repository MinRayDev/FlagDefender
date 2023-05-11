import time

import pygame
from pygame import Surface

from core.chat.chat import MessageType
from core.ui.game_menu import GameMenu
from util.fonts import Fonts



class ChatMessageMenu(GameMenu):
    def __init__(self, game):
        super().__init__("Chat Menu")
        from util.instance import get_client
        self.game_instance = game
        self.client_instance = get_client()
        self.x = 10
        self.height = len(game.chat)*(30+10)
        self.width = self.client_instance.get_screen().get_width()/2.5
        self.y = self.client_instance.get_screen().get_height()-self.client_instance.get_screen().get_height()//20 - 50 - self.height
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface: Surface) -> None:
        to_draw = []
        for message in self.game_instance.chat.messages:
            if message.created_time + 5 > time.time():
                to_draw.insert(0, message)
        if len(to_draw) > 0:
            self.height = len(to_draw)*40
            self.y = self.client_instance.get_screen().get_height()-self.client_instance.get_screen().get_height()//20 - 50 - self.height
            self.alpha_draw(surface, (32, 32, 32, 163), pygame.Rect(self.x, self.y, self.width, self.height))
            for i, message in enumerate(to_draw):
                author_draw = pygame.font.Font(Fonts.product_sans, 30).render(message.author, True, (255, 255, 255))
                message_draw = pygame.font.Font(Fonts.product_sans, 30).render(": " + message.content, True, (255, 255, 255))
                if message.type == MessageType.GAME:
                    author_draw = pygame.font.Font(Fonts.product_sans, 30).render(message.author, True, (0, 255, 0))
                if message.type == MessageType.CLIENT:
                    author_draw = pygame.font.Font(Fonts.product_sans, 30).render(message.author, True, (255, 0, 0))
                surface.blit(author_draw, pygame.Rect(10, self.y + i * 40 + 2, self.width - 10, 30))
                surface.blit(message_draw, pygame.Rect(10 + author_draw.get_rect().width + 2, self.y + i * 40 + 3, self.width - 10, 30))

    @classmethod
    def alpha_draw(cls, surface, color, rect: pygame.Rect):
        temp_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, color, temp_surface.get_rect())
        surface.blit(temp_surface, rect)
