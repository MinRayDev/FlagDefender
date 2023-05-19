import pygame
from pygame import Surface
from util.instance import get_client, get_game
from ui.element.impl.rectangle import Rectangle
from ui.element.impl.text import Text
from ui.game_menu import GameMenu
from util.colors import Colors


class HUD(GameMenu):
    """Class 'HUD' is the HUD of the game.

        Extends the class 'GameMenu'.
        :ivar health_rect_base: The base rectangle of the health bar.
        :type health_rect_base: Rectangle.

    """
    health_rect_base: Rectangle

    def __init__(self):
        """Constructor of the class 'HUD'."""
        super().__init__("HUD")
        self.x = 0
        self.y = 0
        self.width = get_client().get_screen().get_width()
        self.height = get_client().get_screen().get_height()
        self.health_rect_base = Rectangle("CENTER", self.height - self.height//30 - self.height//50, self.width//8, self.height//30, Colors.surface2, Colors.surface2)
        self.elems = []

    def draw(self, surface: Surface) -> None:
        """Draws the HUD on the screen.

            :param surface: The surface on which the HUD is drawn.
            :type surface: Surface.
        """
        self.health_rect_base.draw(surface)
        health_percentage: float = get_game().current_level.main_player.entity.health/get_game().current_level.main_player.entity.max_health
        pygame.draw.rect(surface, Colors.red, pygame.Rect(self.health_rect_base.x, self.height - self.height//30 - self.height//50, int((self.width//8)*health_percentage), self.height//30))
        Text("Kills: " + str(get_game().current_level.main_player.kills), self.width-self.width//8, self.height//20, Colors.red).draw(surface)
        Text("Round: " + str(get_game().current_level.round_manager.round_.number), self.width - self.width // 8, self.height // 10, Colors.red).draw(surface)
        Text("Incline: " + str(get_game().current_level.main_player.entity.incline), self.width - self.width // 8, self.height // 8, Colors.red).draw(surface)
