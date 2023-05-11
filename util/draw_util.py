from pygame import Surface

from util.instance import get_game


def draw_with_scroll(surface: Surface, to_draw: Surface, x: int, y: int):
    surface.blit(
        to_draw,
        (
            x + surface.get_width() // 2 + get_game().current_level.scroll - get_game().current_level.main_player.entity.width // 2,
            y
        )
    )
