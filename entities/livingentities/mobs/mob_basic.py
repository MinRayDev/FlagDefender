import random

from pygame import Surface

from core.chat.chat import entity_register
from core.world import Facing, World
from entities.livingentities.mob import Mob
from entities.projectiles.impl.fireball import Fireball


@entity_register
class MobBasic(Mob):
    """Class 'Mob'.

        Extend 'Mob'.
        :ivar attack_sprites: The sprites used when the mob is attacking.
        :type attack_sprites: tuple[Surface, Surface].
        :ivar walk_sprites: The sprites used when the mob is walking.
        :type walk_sprites: tuple[Surface, Surface].
        :ivar cooldown: The cooldown of the mob.
        :type cooldown: int.
        :ivar distance_damage: Whether the mob can damage from a distance.
        :type distance_damage: bool.

    """
    attack_sprites: tuple[Surface, Surface]
    walk_sprites: tuple[Surface, Surface]
    cooldown: int
    distance_damage: bool

    def __init__(self, x: int, y: int, world: World, facing: Facing = Facing.SOUTH):
        """Constructor of the class 'Mob'.

            :param x: The x coordinate of the mob.
            :type x: int.
            :param y: The y coordinate of the mob.
            :type y: int.
            :param world: The world the mob is in.
            :type world: World.
            :param facing: The direction the mob is facing.
            :type facing: Facing.

        """

        super().__init__(x, y, sprites_path=r"./resources/sprites/mobs/basic", facing=facing, world=world, health=100)
        self.attack_sprites = (self.sprites["1"], self.sprites["3"])
        self.walk_sprites = (self.sprites["2"], self.sprites["4"])
        self.cooldown = 31
        self.distance_damage = True

    def activity(self) -> None:
        """Object's activity function.

            This function is called every tick.

        """
        super().activity()
        if self.facing == Facing.WEST:
            if self.can_attack:
                self.sprite_selected = self.attack_sprites[0]
            else:
                self.sprite_selected = self.walk_sprites[0]
        elif self.facing == Facing.EAST:
            if self.can_attack:
                self.sprite_selected = self.attack_sprites[1]
            else:
                self.sprite_selected = self.walk_sprites[1]

    def attack(self) -> None:
        """Attack function."""
        if random.randint(30, 100) > 70:
            Fireball(self.x, self.y, self)
