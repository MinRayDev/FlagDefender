from __future__ import annotations

import os
import shutil
import threading
import time
from typing import Optional, Any

import pygame
from pygame import Surface

from core.level import Level
from ui.element.element import Element
from ui.element.impl.button_text import ButtonText
from ui.element.impl.notification import alert, info, warn
from ui.element.impl.rectangle import Rectangle
from ui.element.impl.scrollpane import ScrollPane
from ui.element.impl.textentry import TextEntry
from ui.impl.loading_menu import LoadingMenu
from ui.menu import Menu
from util import files
from util.colors import Colors
from util.input.controls import Inputs
from util.instance import get_game, get_client
from util.menu import add_check


def load_and_set_level(name: str, json_fp: str, menu: WorldMenu) -> bool:
    """Load and set the current level.

        :param name: The name of the level.
        :type name: str.
        :param json_fp: The path of the level.
        :type json_fp: str.
        :param menu: The world menu.
        :type menu: WorldMenu.

        :return: True if the level has been loaded and set, False otherwise.
        :rtype: bool.

    """
    try:
        get_game().set_level(Level.load(name, json_fp))
    except:
        warn(menu, "Error loading world.")
    return True


def create_new_level(name: str, parent, new_world_menu) -> None:
    """Create a new level and save it.

        :param name: The name of the level.
        :type name: str.
        :param parent: The parent menu.
        :type parent: WorldMenu.
        :param new_world_menu: The new world menu.
        :type new_world_menu: CreateNewWorld.

    """
    level: Level = Level(name)
    level.save()
    add_check("Level saved.", __name__ + "create_new_level")

    parent.saves = {}
    for i, save in enumerate(files.get_saves()):
        if save.endswith(".json"):
            new_world_menu.parent.saves[save.split("\\")[-1][:-5]] = save
    parent.new_creation = False
    del parent.elems[parent.elems.index(new_world_menu)]
    parent.reload()
    time.sleep(0.5)
    info(parent, f"The save '{name}' has been successfully created.")


class CreateNewWorld(Element):
    """Class 'CreateNewWorld' is an element to create a new world.

            Extends 'Element'.
            :ivar parent: The parent menu.
            :type parent: WorldMenu.
            :ivar s_width: The width of the screen.
            :type s_width: int.
            :ivar s_height: The height of the screen.
            :type s_height: int.
            :ivar rect: The rectangle.
            :type rect: Rectangle.
            :ivar text_entry: The text entry.
            :type text_entry: TextEntry.
            :ivar intern_elems: The internal elements.
            :type intern_elems: list[Element].


    """
    parent: WorldMenu
    s_width: int
    s_height: int
    rect: Rectangle
    text_entry: TextEntry
    intern_elems: list[Element]

    def __init__(self, parent: WorldMenu):
        """Constructor of the class 'CreateNewWorld'.

            :param parent: The parent menu.
            :type parent: WorldMenu.

        """
        self.parent = parent
        self.s_width, self.s_height = get_client().instance.get_screen().get_width(), get_client().instance.get_screen().get_height()
        super().__init__("CENTER", "CENTER", self.s_width // 3, self.s_height // 6)
        self.rect = Rectangle("CENTER", "CENTER", self.s_width // 3, self.s_height // 6, Colors.surface1,
                              Colors.surface1)
        self.text_entry = TextEntry("World Name", "CENTER", self.s_height // 2 - (self.s_height // 16) // 2 - 7,
                                    self.s_width // 4, self.s_height // 16, Colors.text,
                                    Colors.surface1)
        self.text_entry.limit = 20
        self.intern_elems: list[Element] = [self.rect, self.text_entry]

    def activity(self, inputs: Inputs) -> None:
        """Activity of the element.

            :param inputs: The inputs.
            :type inputs: Inputs.

        """
        if pygame.K_ESCAPE in inputs.get_codes():
            if self in self.parent.elems:
                self.parent.new_creation = False
                del self.parent.elems[self.parent.elems.index(self)]
                return
        elif pygame.K_RETURN in inputs.get_codes():
            try:
                f = open(os.path.join(files.get_save_path(), self.text_entry.text + ".json"), "x")
                f.close()
                get_game().set_menu(LoadingMenu(self.parent, 32, "Initiating game.", after=lambda: get_game().set_menu(self.parent)))
                # A thead is used to avoid the game to freeze while loading the level
                # A daemon thread is used to avoid the thread to prevent the program from closing.
                threading.Thread(target=create_new_level, args=(self.text_entry.text, self.parent, self), daemon=True).start()
                return
            except OSError:
                alert(self.parent, f"Error: {self.text_entry.text} is invalid")
                self.parent.new_creation = False
                del self.parent.elems[self.parent.elems.index(self)]
                self.parent.reload()
                return
        for elem in self.intern_elems:
            elem.activity(inputs)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the element."""
        for elem in self.intern_elems:
            elem.draw(surface)

    def hover(self) -> None:
        """Function called when the mouse is over the element."""
        for elem in self.intern_elems:
            if elem.hover() is not None and get_game().current_menu is not None and not isinstance(elem, Rectangle):
                if pygame.mouse.get_cursor() != elem.hover():
                    pygame.mouse.set_cursor(elem.hover())
                    break
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class WorldMenu(Menu):
    """Class 'WorldMenu' is the menu to load a world.

        Extends 'Menu'.
        :ivar base_color: The base color.
        :type base_color: tuple[int, int, int].
        :ivar button_base_color: The button base color.
        :type button_base_color: tuple[int, int, int].
        :ivar button_hover_color: The button hover color.
        :type button_hover_color: tuple[int, int, int].
        :ivar text_color: The text color.
        :type text_color: tuple[int, int, int].
        :ivar selected_button: The selected button.
        :type selected_button: Optional[ButtonText].
        :ivar sp: The scroll pane.
        :type sp: ScrollPane.
        :ivar saves: The saves.
        :type saves: dict[str, dict[str, Any]].
        :ivar new_creation: If a new world is being created.
        :type new_creation: bool.

    """
    base_color: tuple[int, int, int]
    button_base_color: tuple[int, int, int]
    button_hover_color: tuple[int, int, int]
    text_color: tuple[int, int, int]
    selected_button: Optional[ButtonText]
    sp: ScrollPane
    saves: dict[str, str]
    new_creation: bool

    def __init__(self, prev: Menu):
        """Constructor of the class 'WorldMenu'.

            :param prev: The previous menu.
            :type prev: Menu.

        """
        super().__init__("World Menu", prev)
        self.base_color = Colors.base_color
        self.button_base_color = Colors.button_base_color
        self.button_hover_color = Colors.hover_color
        self.text_color = Colors.text_color
        self.selected_button: Optional[ButtonText] = None
        self.sp = ScrollPane(10, 10, get_client().get_screen().get_width() - 20, get_client().get_screen().get_height() - 200,
                             self.base_color)
        self.saves = {}
        for i, save in enumerate(files.get_saves()):
            if save.endswith(".json"):
                bt = ButtonText(get_client().get_screen().get_width() // 7, 30 + (80 + 15) * i,
                                get_client().get_screen().get_width() - (get_client().get_screen().get_width() // 7) * 2, 80,
                                save.split("\\")[-1][:-5], self.button_base_color, self.text_color,
                                self.button_hover_color)
                self.saves[save.split("\\")[-1][:-5]] = save
                self.sp.elems.append(bt)
        elem0: Rectangle = Rectangle(0, get_client().get_screen().get_height() - 190, get_client().get_screen().get_width(), 190,
                                     Colors.mantle)
        elem1: Rectangle = Rectangle(0, 0, get_client().get_screen().get_width(), 10, self.base_color)
        elem2: Rectangle = Rectangle(0, 0, 10, self.sp.height + self.sp.y, self.base_color)
        elem3: Rectangle = Rectangle(self.sp.width + self.sp.x, 0, 10, self.sp.height + self.sp.y, self.base_color)
        base_x: int = get_client().get_screen().get_width() // 7
        base_y: int = get_client().get_screen().get_height() - get_client().get_screen().get_height() // 6
        width: int = ((get_client().get_screen().get_width() - (get_client().get_screen().get_width() // 7) * 2) // 2) - 10
        height: int = get_client().get_screen().get_height() // 15
        self.new_button = ButtonText(base_x, base_y, width, height, "New", self.button_base_color, self.text_color,
                                     self.button_hover_color)
        self.new_button.click = self.new
        self.dup_button = ButtonText(base_x, base_y + height + 20, width, height, "Duplicate", self.button_base_color,
                                     self.text_color, self.button_hover_color)
        self.dup_button.click = self.duplicate
        self.del_button = ButtonText(base_x + width + 20, base_y, width, height, "Delete", self.button_base_color,
                                     self.text_color, self.button_hover_color)
        self.del_button.click = self.delete
        self.back_button = ButtonText(base_x + width + 20, base_y + height + 20, width, height, "Back",
                                      self.button_base_color, self.text_color, self.button_hover_color)
        self.back_button.click = lambda: get_game().set_menu(prev)
        self.elems += [self.sp, elem0, elem1, elem2, elem3, self.del_button, self.dup_button, self.new_button,
                       self.back_button]
        self.new_creation: bool = False

    def activity(self) -> None:
        """Activity of the menu."""
        if not self.new_creation:
            super().activity()
        inputs = self.get_queue()
        if not self.new_creation:
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
            for elem in self.sp.elems:
                if isinstance(elem, ButtonText):
                    if elem.has_been_clicked and self.selected_button != elem:
                        self.selected_button = elem
                    elif elem.has_been_clicked and self.selected_button == elem:
                        # A thread is used to load the level in the background
                        # A daemon thread is used to avoid the thread to prevent the program from closing.
                        get_game().set_menu(LoadingMenu(self, 36, "Initiating game."))
                        threading.Thread(target=load_and_set_level,
                                         args=(elem.text_content, self.saves[elem.text_content], self),
                                         daemon=True).start()

        else:
            if pygame.mouse.get_cursor().data[0] != pygame.SYSTEM_CURSOR_ARROW and pygame.mouse.get_cursor().data[0] != pygame.SYSTEM_CURSOR_IBEAM:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            for elem in self.elems:
                if isinstance(elem, CreateNewWorld):
                    elem.activity(inputs)
                    elem.hover()

    def draw(self, surface: Surface) -> None:
        """Draw the menu.

            :param surface: The surface on which the menu is drawn.
            :type surface: Surface.

        """
        for elem in self.elems:
            if self.new_creation:
                elem.is_hover = False
            elem.draw(surface)
            if isinstance(elem, ScrollPane):
                for child in elem.elems:
                    if self.new_creation:
                        child.is_hover = False
                    if self.selected_button == child and isinstance(child, ButtonText) and self.new_creation is False:
                        pygame.draw.rect(surface, Colors.surface2,
                                         pygame.Rect(child.x - 4, child.y - 4, child.width + 8, child.height + 8))
                        child.draw(surface)

    def delete(self) -> None:
        """Delete the selected save."""
        if self.selected_button is not None and os.path.exists(os.path.join(files.get_save_path(), self.selected_button.text_content + ".json")):
            os.remove(os.path.join(files.get_save_path(), self.selected_button.text_content + ".json"))
            info(self, f"The save '{self.selected_button.text_content}' has been successfully deleted.")
        self.reload()

    def duplicate(self) -> None:
        """Duplicate the selected save."""
        if self.selected_button is not None:
            text: str = os.path.join(files.get_save_path(), self.selected_button.text_content)
            shutil.copyfile(text + ".json",
                            text + " - Copy.json")
            self.saves[(text + " - Copy.json").split("\\")[-1][:-5]] = text + " - Copy.json"
            print(self.saves)
            info(self, f"The save '{self.selected_button.text_content}' has been successfully duplicated.")

        self.reload()

    def reload(self) -> None:
        """Reload the saves."""
        self.sp.elems.clear()
        for i, save in enumerate(files.get_saves()):
            if save.endswith(".json"):
                bt = ButtonText(get_client().get_screen().get_width() // 7, 30 + (80 + 15) * i,
                                get_client().get_screen().get_width() - (get_client().get_screen().get_width() // 7) * 2, 80,
                                save.split("\\")[-1][:-5], self.button_base_color, self.text_color,
                                self.button_hover_color)
                self.sp.elems.append(bt)

    def new(self) -> None:
        """Create a new save."""
        self.new_creation = True
        self.elems.append(CreateNewWorld(self))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
