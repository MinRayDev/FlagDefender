from ui.element.impl.button import Button
from ui.element.impl.text import Text
from util.colors import Colors


class ButtonText(Button):
    def __init__(self, x: int | str, y: int | str, width: int, height: int, text: str, color: tuple[int, int, int],
                 text_color: tuple[int, int, int] = Colors.white, hover_color: tuple[int, int, int] = None):
        super().__init__(x, y, width, height, color)
        self.color: tuple[int, int, int] = color
        self.text_color: tuple[int, int, int] = text_color
        self.text_content = text
        self.has_been_clicked: bool = False
        if hover_color is not None:
            self.hover_color = hover_color
        self.hover_text_color = self.text_color

    def draw(self, surface) -> None:
        super().draw(surface)
        if self.is_hover:
            text_draw = Text(self.text_content, 0, 0, self.hover_text_color)
        else:
            text_draw = Text(self.text_content, 0, 0, self.text_color)
        text_draw.rectangle.center = (self.width // 2 + self.x, self.height // 2 + self.y)
        text_draw.draw(surface)

    def activity(self, inputs) -> None:
        self.has_been_clicked = False
        super().activity(inputs)

    def click(self):
        self.has_been_clicked = True
