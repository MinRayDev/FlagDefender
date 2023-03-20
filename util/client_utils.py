from core.world import Facing
from entities.Entity import Entity
from util.instance import get_game, get_client


def get_out_of_screen() -> tuple[Entity, Facing]:
    x_min: int = get_game().main_player.entity.x + get_game().main_player.entity.width//2 - get_client().get_screen().get_width()//2
    x_max: int = get_game().main_player.entity.x + get_game().main_player.entity.width//2 + get_client().get_screen().get_width()//2
    for entity in get_game().main_player.entity.world.entities:
        if entity.x + entity.width < x_min - 1:
            yield entity, Facing.WEST
        elif entity.x > x_max + 1:
            yield entity, Facing.EAST
