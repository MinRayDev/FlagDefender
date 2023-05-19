from pygame import Surface

from ui.element.impl.button import Button
from ui.element.impl.text import Text
from util.colors import Colors
from util.input.controls import Inputs


class ButtonText(Button):
    """Class 'ButtonText' is a button with text.

        Extends: 'Button'
        :ivar text_content: The text content of the button.
        :type text_content: str.
        :ivar text_color: The text color of the button.
        :type text_color: tuple[int, int, int].
        :ivar hover_text_color: The hover text color of the button.
        :type hover_text_color: tuple[int, int, int].
        :ivar has_been_clicked: If the button has been clicked.
        :type has_been_clicked: bool.
        :ivar hover_color: The hover color of the button.
        :type hover_color: tuple[int, int, int].
    """
    color: tuple[int, int, int]
    text_color: tuple[int, int, int]
    text_content: str
    has_been_clicked: bool
    hover_color: tuple[int, int, int]
    hover_text_color: tuple[int, int, int]

    def __init__(self, x: int | str, y: int | str, width: int, height: int, text: str, color: tuple[int, int, int],
                 text_color: tuple[int, int, int] = Colors.white, hover_color: tuple[int, int, int] = None):
        """Constructor of the class 'ButtonText'.

            :param x: The x position of the button.
            :type x: int | str.
            :param y: The y position of the button.
            :type y: int | str.
            :param width: The width of the button.
            :type width: int.
            :param height: The height of the button.
            :type height: int.
            :param text: The text content of the button.
            :type text: str.
            :param color: The color of the button.
            :type color: tuple[int, int, int].
            :param text_color: The text color of the button.
            :type text_color: tuple[int, int, int].
            :param hover_color: The hover color of the button.
            :type hover_color: tuple[int, int, int].

        """
        super().__init__(x, y, width, height, color)
        self.color = color
        self.text_color = text_color
        self.text_content = text
        self.has_been_clicked = False
        if hover_color is not None:
            self.hover_color = hover_color
        self.hover_text_color = self.text_color

    def draw(self, surface: Surface) -> None:
        """Draws the button.

            :param surface: The surface to draw the button on.
            :type surface: pygame.Surface.

        """
        # Draw the button.
        super().draw(surface)

        # Draw the text.
        if self.is_hover:
            text_draw = Text(self.text_content, 0, 0, self.hover_text_color)
        else:
            text_draw = Text(self.text_content, 0, 0, self.text_color)
        text_draw.rectangle.center = (self.width // 2 + self.x, self.height // 2 + self.y)
        text_draw.draw(surface)

    def activity(self, inputs: Inputs) -> None:
        """Method 'activity' is called every tick to update the button.

            :param inputs: The inputs of the game.
            :type inputs: Inputs.

        """
        self.has_been_clicked = False
        super().activity(inputs)

    def click(self):
        """Method 'click' is called when the button is clicked."""
        self.has_been_clicked = True
