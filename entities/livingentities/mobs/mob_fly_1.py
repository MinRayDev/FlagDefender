import random

from pygame import Surface

from core.chat.chat import entity_register
from core.world import Facing
from entities.entity import EntityType
from entities.livingentities.mob import Mob
from entities.projectiles.impl.remote_fireball import RemoteFireball
from util import world_util
from util.draw_util import draw_with_scroll
from util.instance import get_client


@entity_register
class MobFly1(Mob):  # TODO tire custom vers target (vers le sol)
    def __init__(self, x, y, world, facing=Facing.SOUTH):
        self.sprite_selected_index = 1
        super().__init__(x, y, sprites_path=r"./resources/sprites/mobs/fly", facing=facing, world=world, health=100)
        self.walk_sprites = (self.sprites["1"], self.sprites["2"], self.sprites["3"], self.sprites["4"], self.sprites["5"], self.sprites["6"])
        self.i = 0
        self.cooldown = 30
        self.y = get_client().get_screen().get_height() - self.world.floor - self.height - random.randint(200, 300)
        self.has_gravity = False
        self.distance_damage = True

    def activity(self):
        super().activity()
        if self.i == 7:
            if self.facing == Facing.WEST:
                if self.sprite_selected_index > 2:
                    self.sprite_selected_index = 1
                else:
                    self.sprite_selected_index += 1
            elif self.facing == Facing.EAST:
                if self.sprite_selected_index > 5 or self.sprite_selected_index < 4:
                    self.sprite_selected_index = 4
                else:
                    self.sprite_selected_index += 1
            self.i = 0
        self.i += 1

    def attack(self):
        if random.randint(30, 100) > 50:
            to_attack = world_util.nearest_entity(self, EntityType.ALLY)
            if to_attack is not None:
                if self.x + self.width * 3 >= to_attack.x >= self.x + self.width // 2:
                    self.facing = Facing.EAST
                    RemoteFireball(0, 0, self, to_attack)
                elif self.x - self.width * 2 <= to_attack.x <= self.x + self.width // 2:
                    self.facing = Facing.WEST
                    RemoteFireball(0, 0, self, to_attack)

    def draw(self, surface: Surface) -> None:
        draw_with_scroll(surface, self.sprites[str(self.sprite_selected_index)], self.x, self.y)
        self.draw_health_bar(surface)
