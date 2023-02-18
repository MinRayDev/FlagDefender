import pygame

from core.game import Game
from core.menus.animations.Test import Animation
from core.menus.elements.impl.button_text import ButtonText
from core.menus.elements.impl.notification import notify, alert
from core.menus.impl.multiplayer_join_menu import MPJoinMenu
from core.menus.impl.world_menu import WorldMenu
from core.menus.menu import Menu



class MainMenu(Menu):
    def __init__(self):
        super().__init__("Main Menu")
        self.solo_button = ButtonText(15, 30, 500 - 30, 80, "Solo", (44, 47, 51))
        self.solo_button.click = lambda: Game.instance.set_menu(WorldMenu())
        self.coop_button = ButtonText(15, 120, 500 - 30, 80, "Coop", (44, 47, 51))
        self.coop_button.click = lambda: Game.instance.reset_menu()
        self.multi_button = ButtonText(15, 210, 500 - 30, 80, "Multiplayer", (44, 47, 51))
        self.multi_button.click = lambda: Game.instance.set_menu(MPJoinMenu())
        self.settings_button = ButtonText(15, 300, 500 - 30, 80, "Settings", (44, 47, 51))
        self.settings_button.click = lambda: alert(self, "Les paramètres ne sont pas encore implémentés !")
        self.elems = [self.solo_button, self.coop_button, self.multi_button, self.settings_button]

    def activity(self):
        inputs = self.get_queue()
        for elem in self.elems:
            elem.activity(inputs)
            pass

        for elem in self.elems:
            if elem.hover() is not None and Game.instance.actual_menu is not None:
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if pygame.K_f in inputs.get_codes():
            print("a")

    def draw(self, surface):
        for elem in self.elems:
            elem.draw(surface)
