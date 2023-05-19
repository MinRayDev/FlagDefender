from ui.menu import Menu


class GameMenu(Menu):
    """Class 'GameMenu' is a base class for all game menus.

        Extends the class 'Menu'.
        :ivar game_input_filter: If True, the menu will filter the inputs (example: player's inputs will be ignored if the menu is open and this variable is True)
        :type game_input_filter: bool.

    """
    game_input_filter: bool

    def __init__(self, name: str):
        """Constructor of the class 'GameMenu'.

            :param name: Name of the menu.
            :type name: str.

        """
        super().__init__(name, None)
        self.game_input_filter = True
