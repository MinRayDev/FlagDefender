import asyncio

import pygame
from catppuccin import Flavour

from core.client import Client
from core.ui.element.impl.button_text import ButtonText
from core.ui.element.impl.text import Text
from core.ui.impl.online_testmenu import OLTest
from core.ui.menu import Menu
from network import httpclient
from network.websocket_client import WsClient
from util.instance import get_client
from util.instance import get_game

def start_ws(party_id):
    get_client().is_party_host = True
    get_client().start_websocket(party_id)
    # get_client().game_websocket.send("Started")
    get_game().reset_menu()


class MPHostMenu(Menu):
    def __init__(self, prev):
        super().__init__("Multiplayer Menu", prev)
        self.client = get_client()
        self.party_info = asyncio.run(httpclient.create_party(get_game().main_player.user_id, get_client().id))
        print(self.party_info)
        self.on = False
        self.base_rect = pygame.Rect(15, 30, 500 - 30, 80)
        self.button = ButtonText(15, 30, 500 - 30, 80, "Copy code", (44, 47, 51))
        self.button.click = lambda: pygame.scrap.put(pygame.SCRAP_TEXT, str(self.party_info["code"]).encode("utf-8"))
        self.text = Text(str(self.party_info["code"]), 10, 175, (255, 255, 255))
        self.back_button = ButtonText(Client.get_screen().get_width() / 9 * 2 + Client.get_screen().get_width() / 3,
                                      Client.get_screen().get_height() - 100, Client.get_screen().get_width() / 3, 70,
                                      "Back", (44, 47, 51))
        self.back_button.click = lambda: get_game().set_menu(prev)
        self.start_button = ButtonText(Client.get_screen().get_width() / 9 * 2 + Client.get_screen().get_width() / 3,
                                       Client.get_screen().get_height() - 300, Client.get_screen().get_width() / 3, 70,
                                       "Start", (44, 47, 51))
        self.start_button.click = lambda: start_ws(str(self.party_info["uuid"]))
        self.elems = [self.text, self.button, self.back_button, self.start_button]
        get_client().party_id = str(self.party_info["uuid"])

    def activity(self):
        inputs = self.get_queue()
        for elem in self.elems:
            elem.activity(inputs)
            if elem.hover() is not None and get_game().actual_menu is not None:
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, surface):
        pygame.draw.rect(surface, Flavour.frappe().base.rgb, pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        for elem in self.elems:
            elem.draw(surface)
