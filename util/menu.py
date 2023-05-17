import time

from ui.impl.loading_menu import LoadingMenu

SLEEP_TIME = 0.25


def add_check(name: str, source: str, sleep_mult: float = 0.1) -> None:
    from util.instance import get_game
    menu = get_game().current_menu
    if isinstance(menu, LoadingMenu):
        menu.add_check(name, source)
        time.sleep(SLEEP_TIME*sleep_mult)


def append_check(index: int, name: str, source: str, sleep_mult: float = 0.1) -> None:
    from util.instance import get_game
    menu = get_game().current_menu
    if isinstance(menu, LoadingMenu):
        menu.append_check(index, name, source)
        time.sleep(SLEEP_TIME*sleep_mult)
