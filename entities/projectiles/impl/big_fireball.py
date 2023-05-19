from pygame import Surface

from core.world import Facing
from entities.entity import Entity, DamageType
from entities.projectiles.projectile import Projectile
from util.draw_util import draw_with_scroll
from util.instance import get_client


class BigFireball(Projectile):
    """Class 'BigFireball'.

        Extends 'Projectile'.
        :ivar frame: The current frame of the fireball.
        :type frame: int.
        :ivar start_x: The x position of the fireball when it was created.
        :type start_x: int.

    """
    frame: int
    start_x: int

    def __init__(self, x: int, y: int, author: Entity):
        """Constructor of the class 'BigFireball'.

            :param x: The x position of the fireball.
            :type x: int.
            :param y: The y position of the fireball.
            :type y: int.
            :param author: The author of the fireball.
            :type author: Entity.

        """
        super().__init__(x, y, sprites_path=r"./resources/sprites/projectiles/big_fireball", author=author, damage_value=50)
        self.frame = 0
        self.start_x = self.x
        match self.facing:
            case Facing.NORTH:
                self.motion_y = -5
                self.x += 78 // 2 - self.width // 2
                self.y -= 16
            case Facing.EAST:
                self.motion_x = 5
                self.x += 78
                self.y += 20
            case Facing.SOUTH:
                self.motion_y = 5
                self.x += 78 // 2 - self.width // 2
                self.y += 80 - 30
            case Facing.WEST:
                self.motion_x = -5
                self.x -= 16
                self.y += 20

    def draw(self, surface: Surface) -> None:
        """Draws the fireball.

            :param surface: The surface to draw the fireball on.
            :type surface: Surface.
        """

        if round(self.frame) < len(self.sprites):
            draw_with_scroll(surface, list(self.sprites.values())[round(self.frame)], self.x, self.y)
        else:
            self.frame = 0
            draw_with_scroll(surface, list(self.sprites.values())[self.frame], self.x, self.y)
        self.frame += 0.2

    def activity(self) -> None:
        """The activity of the fireball."""
        super().activity()
        self.x += self.motion_x
        self.y += self.motion_y

        self.do_damage()
        if self.x > get_client().get_screen().get_width() * 5 or self.x + self.width < 0 - get_client().get_screen().get_width() * 5 or self.y > get_client().get_screen().get_height() * 5 or self.y + self.height < 0:
            self.death()
        if abs(self.x - self.start_x) > 1000:
            self.death()

    def do_damage(self) -> None:
        """Does damage to entities."""
        for entity in self.world.entities:
            if self.can_damage(entity):
                self.health -= entity.health
                entity.damage(self.damage_value, DamageType.PROJECTILE, self.author)
