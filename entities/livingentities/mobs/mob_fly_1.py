import random

from pygame import Surface

from core.chat.chat import entity_register
from core.world import Facing, World
from entities.livingentities.mob import Mob
from entities.projectiles.impl.remote_fireball import RemoteFireball
from util.draw_util import draw_with_scroll
from util.instance import get_client


@entity_register
class MobFly1(Mob):
    """Class 'MobFly1'.

        Extend 'Mob'.
        :ivar walk_sprites: The sprites used when the mob is walking.
        :type walk_sprites: tuple[Surface, Surface].
        :ivar i: The index of the sprite.
        :type i: int.
        :ivar cooldown: The cooldown of the mob.
        :type cooldown: int.
        :ivar distance_damage: Whether the mob can damage from a distance.
        :type distance_damage: bool.

    """
    sprite_selected_index: int
    walk_sprites: tuple[Surface, Surface, Surface, Surface, Surface, Surface]
    i: int
    distance_damage: bool

    def __init__(self, x: int, y: int, world: World, facing: Facing = Facing.SOUTH):
        """Constructor of the class 'MobFly1'.

            :param x: The x coordinate of the mob.
            :type x: int.
            :param y: The y coordinate of the mob.
            :type y: int.
            :param world: The world the mob is in.
            :type world: World.
            :param facing: The direction the mob is facing.
            :type facing: Facing.

        """
        self.sprite_selected_index = 1
        super().__init__(x, y, sprites_path=r"./resources/sprites/mobs/fly", facing=facing, world=world, health=100)
        self.walk_sprites = (self.sprites["1"], self.sprites["2"], self.sprites["3"], self.sprites["4"], self.sprites["5"], self.sprites["6"])
        self.i = 0
        self.cooldown = 30
        self.y = get_client().get_screen().get_height() - self.world.floor - self.height - random.randint(200, 300)
        self.has_gravity = False
        self.distance_damage = True

    def activity(self) -> None:
        """Object's activity function.

            This function is called every tick.

        """
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

    def attack(self) -> None:
        """Entity's attack function."""
        if random.randint(30, 100) > 50:
            RemoteFireball(0, 0, self, self.target)

    def draw(self, surface: Surface) -> None:
        """Draws the entity on the surface.

            :param surface: The surface to draw on.
            :type surface: Surface.

        """
        draw_with_scroll(surface, self.sprites[str(self.sprite_selected_index)], self.x, self.y)
        self.draw_health_bar(surface)
