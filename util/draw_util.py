from pygame import Surface

from util.instance import get_game


def draw_with_scroll(surface: Surface, to_draw: Surface, x: int, y: int) -> None:
    """Draws a surface with the scroll of the current level.

        :param surface: The surface to draw on.
        :type surface: Surface.
        :param to_draw: The surface to draw.
        :type to_draw: Surface.
        :param x: The x position to draw at.
        :type x: int.
        :param y: The y position to draw at.
        :type y: int.

    """
    surface.blit(
        to_draw,
        (
            x + surface.get_width() // 2 + get_game().current_level.scroll - get_game().current_level.main_player.entity.width // 2,
            y
        )
    )
