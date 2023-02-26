import asyncio

import pygame
from catppuccin import Flavour

from core.client import Client
from core.ui.element.impl.button_text import ButtonText
from core.ui.element.impl.notification import warn, alert
from core.ui.element.impl.text import Text
from core.ui.element.impl.textentry import TextEntry
from core.ui.impl.online_testmenu import OLTest
from core.ui.menu import Menu
from network.httpclient import get_party, get_party_by_code
from network.websocket_client import WsClient
from util.instance import get_client
from util.instance import get_game


def start_ws(party_id):
    get_client().start_websocket(party_id)
    # get_client().game_websocket.send("Started")


def join_party(code, menu):
    party_info = asyncio.run(get_party_by_code(code))
    if "can_join" in party_info and party_info["can_join"]:
        get_client().party_id = str(party_info["uuid"])
        start_ws(str(party_info["uuid"]))
        get_game().reset_menu()
    else:
        alert(menu, f"You are not allowed to join the party with code {code}")


class MPJoinMenu(Menu):
    def __init__(self, prev):
        super().__init__("Multiplayer Menu", prev)
        self.client = get_client()
        self.on = False
        self.button = ButtonText(15, 30, 500 - 30, 80, "Join", (44, 47, 51))
        self.button.click = lambda: join_party(self.text_input.get_text(), self)
        self.text_input = TextEntry('', 10, 175, 150, 50, (153, 170, 181))
        self.back_button = ButtonText(Client.get_screen().get_width() / 9 * 2 + Client.get_screen().get_width() / 3,
                                      Client.get_screen().get_height() - 100, Client.get_screen().get_width() / 3, 70,
                                      "Back", (44, 47, 51))
        self.back_button.click = lambda: get_game().set_menu(prev)
        self.text = Text("", 10, 250, (153, 170, 181))
        self.elems = [self.text_input, self.button, self.back_button, self.text]
        self.last_text = ""
        self.can_join = False

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
        if self.last_text != self.text_input.get_text():
            self.last_text = self.text_input.get_text()
            asyncio.run(self.check_code(self.text_input.get_text()))

    def draw(self, surface):
        pygame.draw.rect(surface, Flavour.frappe().base.rgb, pygame.Rect(0, 0, self.client.get_screen().get_width(), self.client.get_screen().get_height()))
        for elem in self.elems:
            elem.draw(surface)

    async def check_code(self, code_: str):
        if not code_.isnumeric():
            self.text.change("Invalid code")
            return
        party = await get_party_by_code(int(code_))
        print(party)
        if party is None:
            self.text.change("Party not found")
        elif "member_count" in party:
            self.text.change(str(party["member_count"]))
            self.can_join = party["can_join"]
        else:
            self.text.change("Party not found")

    def join(self):
        if self.can_join:
            print("--")