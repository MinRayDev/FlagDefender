import pygame
from pygame import Surface

from ui.element.impl.button_text import ButtonText
from ui.element.impl.text import Text
from ui.impl.main_menu import MainMenu
from ui.menu import Menu
from util.instance import get_client
from util.instance import get_game


class GameOverMenu(Menu):
    """Menu that appears when the flag is destroyed.

        Extends the class 'Menu'.
        :ivar game_over: Text that says "Game Over".
        :type game_over: Text.
        :ivar back_button: Button that says "ok".
        :type back_button: ButtonText.
        :ivar rounds: Text that says the number of rounds.
        :type rounds: Text.
        :ivar kills: Text that says the number of kills.
        :type kills: Text.

    """
    game_over: Text
    back_button: ButtonText
    rounds: Text
    kills: Text

    def __init__(self, kills: int, rounds: int):
        """Constructor of the class 'GameOverMenu'.

            :param kills: Number of kills.
            :type kills: int.
            :param rounds: Number of rounds.
            :type rounds: int.

        """
        super().__init__("Game Over", None)
        get_game().reset_level()
        self.game_over = Text("Game Over", 0, 0, (225, 10, 10), 60)
        self.game_over.x = get_client().get_screen().get_width()/2 - self.game_over.rectangle.width/2
        self.game_over.rectangle.x = get_client().get_screen().get_width()/2 - self.game_over.rectangle.width/2
        self.game_over.rectangle.y = get_client().get_screen().get_height()/2 - self.game_over.rectangle.height*3.5
        self.back_button = ButtonText("CENTER",
                                      int(get_client().get_screen().get_height()/2+(get_client().get_screen().get_height() // 17)*3),
                                      get_client().get_screen().get_width() // 10,
                                      get_client().get_screen().get_height() // 17,
                                      "ok", (0, 0, 0), (225, 10, 10),
                                      hover_color=(10, 10, 10)
                                      )
        self.back_button.click = lambda: get_game().set_menu(MainMenu())
        self.rounds = Text("Round: " + str(rounds), 0, 0, (225, 10, 10), 30)
        self.rounds.x = get_client().get_screen().get_width() / 2 - self.rounds.rectangle.width / 2
        self.rounds.rectangle.x = get_client().get_screen().get_width() / 2 - self.rounds.rectangle.width / 2
        self.rounds.rectangle.y = get_client().get_screen().get_height() / 2 - self.rounds.rectangle.height * 3
        self.rounds.rectangle.y = get_client().get_screen().get_height() / 2 - self.rounds.rectangle.height * 3

        self.kills = Text("Kills: " + str(kills), 0, 0, (225, 10, 10), 30)
        self.kills.x = get_client().get_screen().get_width() / 2 - self.kills.rectangle.width / 2
        self.kills.rectangle.x = get_client().get_screen().get_width() / 2 - self.kills.rectangle.width / 2
        self.kills.rectangle.y = get_client().get_screen().get_height() / 2 - self.kills.rectangle.height * 1.5
        self.kills.rectangle.y = get_client().get_screen().get_height() / 2 - self.kills.rectangle.height * 1.5
        self.elems += [self.game_over, self.back_button, self.rounds, self.kills]

    def activity(self) -> None:
        """Method that updates the menu."""
        inputs = self.get_queue()
        for elem in self.elems:
            elem.activity(inputs)

    def draw(self, surface: Surface) -> None:
        """Method that draws the menu.

            :param surface: Surface where the menu is drawn.
            :type surface: Surface.

        """
        pygame.draw.rect(surface, (0, 0, 0), pygame.Rect(0, 0, get_client().get_screen().get_width(), get_client().get_screen().get_height()))
        for elem in self.elems:
            elem.draw(surface)
