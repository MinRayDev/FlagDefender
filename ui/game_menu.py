from ui.menu import Menu


class GameMenu(Menu):
    def __init__(self, name: str):
        super().__init__(name, None)
        self.game_input_filter = True
