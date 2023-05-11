import time

import pygame
from pygame import Surface

from core.chat.chat import MessageType, Message, cmd_complete, get_cmd_tab_index, item_complete, entity_complete
from core.ui.element.impl.textentry import TextEntry
from core.ui.game_menu import GameMenu
from core.chat.chat import Command
from util.instance import get_client
from util.instance import get_game


class ChatMenu(GameMenu):
    def __init__(self):
        super().__init__("Chat Menu")
        self.text_input = TextEntry('', 10, get_client().get_screen().get_height()-get_client().get_screen().get_height()//20 - 50, get_client().get_screen().get_width()/2.5, 50, (153, 170, 181))
        self.text_input.background_color = None
        self.text_input.selected = True
        self.text_input.unselect = False
        self.init_time = time.time()
        self.text_input.limit = 48
        self.elems = [self.text_input]
        self.message_index = 0
        self.tab_index = 0
        self.to_complete = None

    def activity(self):
        inputs = self.get_queue()
        if time.time() > self.init_time + 0.5:
            if pygame.K_RETURN in inputs.get_codes():
                self.reset_tab()
                if len(self.text_input.get_text()) > 0:
                    if Command.is_command(self.text_input.get_text()):
                        Command.execute(self.text_input.get_text())
                    else:
                        get_game().chat.write(self.text_input.get_text(), MessageType.SELF, None)
                    get_game().chat.client_messages.append(Message(self.text_input.get_text(), "(Moi)", MessageType.SELF))
                    get_game().reset_menu()
        if pygame.K_UP in inputs.get_codes():
            self.reset_tab()
            if self.message_index < len(get_game().chat.client_messages):
                self.message_index += 1
                self.text_input.text = get_game().chat.client_messages[-self.message_index].content
        if pygame.K_DOWN in inputs.get_codes():
            self.reset_tab()
            if self.message_index > 0:
                self.message_index -= 1
                self.text_input.text = get_game().chat.client_messages[-self.message_index].content
            if self.message_index == 0:
                self.text_input.text = ""
        if pygame.K_ESCAPE in inputs.get_codes():
            self.reset_tab()
            get_game().reset_menu()
        for elem_ in inputs.raw_inputs:
            if elem_.type == pygame.TEXTINPUT or (elem_.type == pygame.KEYDOWN and elem_.key == pygame.K_BACKSPACE) or (elem_.type == pygame.KEYUP and elem_.key == pygame.K_BACKSPACE) or (elem_.type == pygame.KEYDOWN and (elem_.__dict__["unicode"] == "\x03" or elem_.__dict__["unicode"] == "\x16")):
                self.reset_tab()
        if pygame.K_TAB in inputs.get_codes():
            if self.tab_index == 0 and self.to_complete is None:
                self.to_complete = self.text_input.get_text().split(" ")[-1]
            if self.to_complete.startswith("/"):
                word_completed = cmd_complete(self.to_complete, self.tab_index)
                if word_completed is not None:
                    self.text_input.text = word_completed
                    self.tab_index += 1
                    if self.tab_index >= get_cmd_tab_index(self.to_complete):
                        self.tab_index = 0
            elif self.text_input.get_text().startswith("/give"):
                word_completed = item_complete(self.to_complete, self.tab_index)
                if word_completed is not None:
                    self.text_input.text = " ".join(self.text_input.get_text().split(" ")[:-1]) + " " + word_completed
                    self.tab_index += 1
            elif self.text_input.get_text().split(" ")[0] in ["/summon"]:
                word_completed = entity_complete(self.to_complete, self.tab_index)
                if word_completed is not None:
                    self.text_input.text = " ".join(self.text_input.get_text().split(" ")[:-1]) + " " + word_completed
                    self.tab_index += 1
        for elem in self.elems:
            elem.activity(inputs)
            pass

        for elem in self.elems:
            if elem.hover() is not None and get_game().current_menu is not None:
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            if pygame.mouse.get_cursor() != pygame.SYSTEM_CURSOR_ARROW:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def draw(self, surface: Surface) -> None:
        self.alpha_draw(surface, (32, 32, 32, 163), self.text_input.rectangle)
        for elem in self.elems:
            elem.draw(surface)

    @classmethod
    def alpha_draw(cls, surface, color, rect: pygame.Rect):
        temp_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(temp_surface, color, temp_surface.get_rect())
        surface.blit(temp_surface, rect)

    def reset_tab(self):
        self.tab_index = 0
        self.to_complete = None
