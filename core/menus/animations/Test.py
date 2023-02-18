import time

from core.menus.elements.element import Element


class Animation:
    def __init__(self, element: Element, iterations: int):
        self.element = element
        self.iterations = iterations
        self.__keys = {}  # time (sec): pos (x, y)

        self.last = 0
        self.test = 0

    def add_key(self, time_: float, pos: tuple[int, int]):
        self.__keys[time_] = pos
        print(sorted(self.__keys))

    def aa(self):
        self.last = time.time()
        self.test += 1
        self.element.y += self.element.height // self.iterations
        self.element.rectangle.y = self.element.y