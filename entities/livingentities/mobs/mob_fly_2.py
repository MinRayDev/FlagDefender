import random

from pygame import Surface

from core.chat.chat import entity_register
from core.world import Facing, World
from entities.livingentities.mob import Mob
from entities.projectiles.impl.bomb_entity import BombEntity
from util.draw_util import draw_with_scroll
from util.instance import get_client
from util.world_util import area_contains


@entity_register
class MobFly2(Mob):
    """Class 'MobFly2'.

        Extend 'Mob'.
        :ivar i: The index of the sprite.
        :type i: int.
        :ivar sprite_selected_index: The index of the sprite.
        :type sprite_selected_index: int.
        :ivar offsets: The offsets of the sprites.
        :type offsets: dict[Surface, int].

    """
    i: int
    sprite_selected_index: int
    offsets: dict[Surface, int]

    def __init__(self, x: int, y: int, world: World, facing: Facing = Facing.SOUTH):
        """Constructor of the class 'MobFly2'.

            :param x: The x coordinate of the mob.
            :type x: int.
            :param y: The y coordinate of the mob.
            :type y: int.
            :param world: The world the mob is in.
            :type world: World.
            :param facing: The direction the mob is facing.
            :type facing: Facing.

        """
        super().__init__(x, y, sprites_path=r"./resources/sprites/mobs/fly2", facing=facing, world=world, health=100)
        self.cooldown = 30
        self.y = get_client().get_screen().get_height() - self.world.floor - self.height - random.randint(300, 600)
        self.has_gravity = False
        self.i = 0
        self.sprite_selected_index = 1
        self.offsets: dict[Surface, int] = {self.sprites["3"]: -13}

    def activity(self) -> None:
        """Object's activity function.

            This function is called every tick.

        """
        self.unlock()
        if self.target is not None and area_contains((self.x - self.width//3, None), (self.x + self.width + self.width//3, None), self.target):
            self.lock()
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

    def attack(self) -> None:
        """Entity's attack function."""
        if random.randint(30, 100) > 70:
            BombEntity(self.x + self.width // 2, self.y + self.height + 5, self, -15)

    def draw(self, surface: Surface) -> None:
        """Draws the entity on the surface.

            :param surface: The surface to draw the entity on.
            :type surface: Surface.

        """
        offset: int = 0
        if self.sprites[str(self.sprite_selected_index)] in self.offsets:
            offset = self.offsets[self.sprites[str(self.sprite_selected_index)]]
        draw_with_scroll(surface, self.sprites[str(self.sprite_selected_index)], self.x + offset, self.y)
        self.draw_health_bar(surface, offset)
