import time
from typing import TYPE_CHECKING

import pygame
from pygame import Surface

from core.chat.chat import MessageType
from ui.game_menu import GameMenu
from util.fonts import Fonts
from util.instance import get_client, get_game

if TYPE_CHECKING:
    from core.game import Game


class ChatMessageMenu(GameMenu):
    """Class 'ChatMessageMenu' is the chat message menu of the game.

        Extends the class 'GameMenu'.
        :ivar x: The x position of the chat message menu.
        :type x: int.
        :ivar y: The y position of the chat message menu.
        :type y: int.
        :ivar width: The width of the chat message menu.
        :type width: int.
        :ivar height: The height of the chat message menu.
        :type height: int.
        :ivar rectangle: The rectangle of the chat message menu.
        :type rectangle: pygame.Rect.

    """
    x: int
    y: int
    width: int
    height: int
    rectangle: pygame.Rect

    def __init__(self, game: 'Game'):
        """Constructor of the class 'ChatMessageMenu'.

            :param game: The game of the chat message menu.
            :type game: Game.

        """
        super().__init__("Chat Menu")
        self.x = 10
        self.height = len(game.chat)*(30+10)
        self.width = int(get_client().get_screen().get_width()/2.5)
        self.y = get_client().get_screen().get_height()-get_client().get_screen().get_height()//20 - 50 - self.height
        self.rectangle = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface: Surface) -> None:
        to_draw = []
        for message in get_game().chat.messages:
            if message.created_time + 5 > time.time():
                to_draw.insert(0, message)
        if len(to_draw) > 0:
            self.height = len(to_draw)*40
            self.y = get_client().get_screen().get_height()-get_client().get_screen().get_height()//20 - 50 - self.height
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
    def alpha_draw(cls, surface: Surface, color_rgba: tuple[int, int, int, int], rect: pygame.Rect) -> None:
        """Method to draw a rectangle with an alpha value.

            :param surface: The surface on which the rectangle is drawn.
            :type surface: Surface.
            :param color_rgba: The color of the rectangle.
            :type color_rgba: tuple[int, int, int, int].
            :param rect: The rectangle to draw.
            :type rect: pygame.Rect.

        """
        temp_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, color_rgba, temp_surface.get_rect())
        surface.blit(temp_surface, rect)
