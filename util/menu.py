import time

from ui.impl.loading_menu import LoadingMenu

SLEEP_TIME: float = 0.25


def add_check(name: str, source: str, sleep_mult: float = 0.1) -> None:
    """Adds a check to the loading menu.

        :param name: The name of the check.
        :type name: str.
        :param source: The source of the check.
        :type source: str.
        :param sleep_mult: The multiplier for the sleep time.
        :type sleep_mult: float.

    """
    from util.instance import get_game
    menu = get_game().current_menu
    if isinstance(menu, LoadingMenu):
        menu.add_check(name, source)
        time.sleep(SLEEP_TIME*sleep_mult)
