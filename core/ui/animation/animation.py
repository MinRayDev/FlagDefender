import time

from core.ui.element.element import Element


class Animation:
    def __init__(self, element: Element, iterations: int):
        self.element: Element = element
        self.iterations: int = iterations
        self.__keys: dict[float, tuple[int, int]] = {}  # time (sec): pos (x, y)
        self.base: tuple[int, int] = (self.element.x, self.element.y)
        self.last_iteration: float = 0
        self.completed_iterations: int = 0
        self.start_animation: float = 0

    def add_key(self, time_: float, pos: tuple[int, int]) -> None:
        self.__keys[time_] = pos

    def activity(self) -> None:
        if self.completed_iterations < self.iterations:
            if self.last_iteration + 1/60 < time.time():
                self.last_iteration = time.time()
                self.completed_iterations += 1
                self.element.x += (self.get_key()[1][0] - self.base[0]) // self.get_key()[0]
                self.element.y += (self.get_key()[1][1] - self.base[1]) // self.get_key()[0]
                self.element.rectangle.x = self.element.x
                self.element.rectangle.y = self.element.y

    def start(self) -> None:
        self.start_animation = time.time()

    def is_started(self) -> bool:
        return self.start_animation > 0

    def get_key(self) -> tuple[float, tuple[int, int]]:
        if len(self.__keys) > 0:
            return sorted(self.__keys)[0], self.__keys[sorted(self.__keys)[0]]

    def remove_key(self, key) -> None:
        del self.__keys[key]

    def is_ended(self) -> bool:
        return self.completed_iterations >= self.iterations
