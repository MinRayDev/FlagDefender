from entities.entity import Entity
from entities.projectiles.impl.fireball import Fireball
from util.instance import get_game, get_client


class TurretBullet(Fireball):
    """Class 'TurretBullet'.

        Extends 'Fireball'.

    """
    def __init__(self, x: int, y: int, author: Entity, target_pos: tuple[int, int]):
        """Constructor of the class 'TurretBullet'.

            :param x: The x position of the bullet.
            :type x: int.
            :param y: The y position of the bullet.
            :type y: int.
            :param author: The author of the bullet.
            :type author: Entity.
            :param target_pos: The target position of the bullet.
            :type target_pos: tuple[int, int].

        """
        super().__init__(x, y, author)
        self.motion_x = int(((target_pos[0] - self.x) // get_game().TPS) * 2)
        self.motion_y = int(((target_pos[1] - self.y) // get_game().TPS) * 2)

    def activity(self) -> None:
        """Activity of the bullet."""
        self.x += self.motion_x
        self.y += self.motion_y

        self.do_damage()
        if self.x > get_client().get_screen().get_width()*5 or self.x+self.width < 0-get_client().get_screen().get_width()*5 or self.y > get_client().get_screen().get_height()*5 or self.y + self.height < 0:
            self.death()
