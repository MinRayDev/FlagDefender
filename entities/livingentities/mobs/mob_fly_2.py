import random

from pygame import Surface

from core.chat.chat import entity_register
from core.world import Facing
from entities.livingentities.mob import Mob
from entities.projectiles.impl.bomb_entity import BombEntity
from util.draw_util import draw_with_scroll
from util.instance import get_client


@entity_register
class MobFly2(Mob):
    def __init__(self, x, y, world, facing=Facing.SOUTH):
        super().__init__(x, y, sprites_path=r"./resources/sprites/mobs/fly2", facing=facing, world=world, health=100)
        self.cooldown = 30
        self.last_facing = self.facing
        self.y = get_client().get_screen().get_height() - self.world.floor - self.height - random.randint(100, 300)
        self.has_gravity = False
        self.i = 0
        self.sprite_selected_index = 1
        self.offsets: dict[Surface, int] = {self.sprites["3"]: -13}

    def activity(self):
        super().activity()
        if self.facing == Facing.WEST:
            if self.sprite_selected_index > 4:
                self.sprite_selected_index = 1
            elif self.i == 10:
                self.i = 0
                self.sprite_selected_index += 1
        elif self.facing == Facing.EAST:
            if self.sprite_selected_index > 9 or self.sprite_selected_index < 6:
                self.sprite_selected_index = 6
            elif self.i == 10:
                self.i = 0
                self.sprite_selected_index += 1
        self.i += 1

    def attack(self):
        if random.randint(30, 100) > 70:
            BombEntity(self.x + self.width // 2, self.y + self.height + 5, self, -20)

    def draw(self, surface: Surface) -> None:
        offset: int = 0
        if self.sprites[str(self.sprite_selected_index)] in self.offsets:
            offset = self.offsets[self.sprites[str(self.sprite_selected_index)]]
        draw_with_scroll(surface, self.sprites[str(self.sprite_selected_index)], self.x + offset, self.y)
        self.draw_health_bar(surface, offset)
