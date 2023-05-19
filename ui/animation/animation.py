import time

from ui.element.element import Element


class Animation:
    """Class 'Animation' is the animation of an element.

        :ivar element: The element.
        :type element: Element.
        :ivar iterations: The amount of iterations.
        :type iterations: int.
        :ivar __keys: The keys of the animation.
        :type __keys: dict[float, tuple[int, int]].
        :ivar base: The base position of the element.
        :type base: tuple[int, int].
        :ivar last_iteration: The last iteration.
        :type last_iteration: float.
        :ivar completed_iterations: The amount of completed iterations.
        :type completed_iterations: int.
        :ivar start_animation: The start of the animation.
        :type start_animation: float.

    """
    element: Element
    iterations: int
    __keys: dict[float, tuple[int, int]]
    base: tuple[int, int]
    last_iteration: float
    completed_iterations: int
    start_animation: float

    def __init__(self, element: Element, iterations: int):
        """Constructor of the class 'Animation'.

            :param element: The element.
            :type element: Element.
            :param iterations: The amount of iterations.
            :type iterations: int.

        """
        self.element = element
        self.iterations = iterations
        self.__keys = {}  # time (sec): pos (x, y)
        self.base = (self.element.x, self.element.y)
        self.last_iteration = 0
        self.completed_iterations = 0
        self.start_animation = 0

    def add_key(self, time_: float, pos: tuple[int, int]) -> None:
        """Adds a key to the animation.

            :param time_: The time of the key.
            :type time_: float.
            :param pos: The position of the key.
            :type pos: tuple[int, int].

        """
        self.__keys[time_] = pos

    def activity(self) -> None:
        """The activity of the animation."""
        if self.completed_iterations < self.iterations:
            if self.last_iteration + 1/60 < time.time():
                self.last_iteration = time.time()
                self.completed_iterations += 1
                self.element.x += (self.get_key()[1][0] - self.base[0]) // self.get_key()[0]
                self.element.y += (self.get_key()[1][1] - self.base[1]) // self.get_key()[0]
                self.element.rectangle.x = self.element.x
                self.element.rectangle.y = self.element.y

    def start(self) -> None:
        """Starts the animation."""
        self.start_animation = time.time()

    def is_started(self) -> bool:
        """Returns whether the animation is started or not."""
        return self.start_animation > 0

    def get_key(self) -> tuple[float, tuple[int, int]]:
        """Returns the key of the animation."""
        if len(self.__keys) > 0:
            return sorted(self.__keys)[0], self.__keys[sorted(self.__keys)[0]]

    def remove_key(self, key: float) -> None:
        """Removes a key from the animation.

            :param key: The key to remove.
            :type key: float.

        """
        del self.__keys[key]

    def is_ended(self) -> bool:
        """Returns whether the animation is ended or not."""
        return self.completed_iterations >= self.iterations
