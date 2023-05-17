import pygame
from pygame import Surface

from util.input.controls import Inputs
from util.instance import get_game


class Menu:
    def __init__(self, name, prev):
        self.name = name
        self.inputs_queue = Inputs()
        self.prev = prev
        self.elems = []

    def activity(self):
        inputs = self.get_queue(False)
        if pygame.K_ESCAPE in inputs.get_codes():
            if self.prev is not None:
                get_game().set_menu(self.prev)
            else:
                get_game().reset_menu()

    def draw(self, surface: Surface) -> None:
        for elem in self.elems:
            elem.draw(surface)

    def add_queue(self, element):
        if element not in self.inputs_queue:
            self.inputs_queue.add(element)

    def add_raw_queue(self, element):
        if element not in self.inputs_queue.raw_inputs:
            self.inputs_queue.raw_add(element)

    def get_queue(self, reset: bool = True):
        temp = self.inputs_queue.copy()
        if reset:
            self.inputs_queue = Inputs()
        return temp
