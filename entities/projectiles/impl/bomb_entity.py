import math
import time

from pygame import Surface

from core.world import Facing
from entities.entity import Entity, DamageType
from entities.projectiles.projectile import Projectile
from util import sprites, audio
from util.draw_util import draw_with_scroll
from util.instance import get_client
from util.time_util import has_elapsed


class BombEntity(Projectile):
    """Class 'BombEntity'.

        Extends 'Projectile'.
        :ivar start_time: The time when the bomb was created.
        :type start_time: float.
        :ivar deceleration: The deceleration of the bomb.
        :type deceleration: float.
        :ivar creation_time: The time when the bomb was created.
        :type creation_time: float.
        :ivar is_explosing: Whether the bomb is exploding or not.
        :type is_explosing: bool.
        :ivar explosion_frame: The current frame of the explosion.
        :type explosion_frame: int.

    """
    start_time: float
    deceleration: float
    creation_time: float
    is_explosing: bool
    explosion_frame: int

    def __init__(self, x: int, y: int, author: Entity, inclinaison: int):
        """Constructor of the class 'BombEntity'.

            :param x: The x position of the bomb.
            :type x: int.
            :param y: The y position of the bomb.
            :type y: int.
            :param author: The author of the bomb.
            :type author: Entity.
            :param inclinaison: The inclinaison of the bomb.
            :type inclinaison: int.

        """
        super().__init__(x, y, sprites_path=r"./resources/sprites/spells/bomb", author=author, damage_value=60)
        self.gravity_value = 0 - inclinaison
        self.start_time = time.time()

        angle_target: float
        incline_factor: float
        incline_adjust = inclinaison * (9 / 10)
        if incline_adjust > 0:
            # 0 -> 10
            # sin(pi) -> sin(pi/2)
            incline_factor = (10 - incline_adjust) / 10
            angle_target = math.pi / 2 + ((math.pi / 2) * incline_factor)
        else:
            # 0 -> -15
            # sin(pi/2) -> sin(pi + pi / 2) (i.e pi / .6666)
            incline_factor = -incline_adjust / 15
            angle_target = math.pi + (math.pi / 2 * incline_factor)

        self.motion_x = int(10 * math.cos(angle_target))
        if self.facing == Facing.EAST:
            self.motion_x *= -1

        self.deceleration = 0.1
        match self.facing:
            case Facing.EAST:
                self.x += author.width
                self.y += 20
            case Facing.WEST:
                self.x -= self.width
                self.y += 20

        self.creation_time = time.time()
        self.has_gravity = False
        self.type = author.type
        self.has_collisions = False
        self.is_explosing = False
        self.explosion_frame = 0

    def draw(self, surface: Surface) -> None:
        """Draws the bomb.

            :param surface: The surface to draw the bomb on.
            :type surface: Surface.

        """
        if not self.is_explosing:
            draw_with_scroll(surface, self.sprite_selected, self.x, self.y)
        elif self.is_explosing and round(self.explosion_frame) < len(self.sprites):
            draw_with_scroll(surface, list(self.sprites.values())[round(self.explosion_frame)], self.x, self.y)
            self.explosion_frame += 0.4

    def activity(self) -> None:
        """The activity of the bomb."""
        if self.y + self.height + self.gravity_value < get_client().get_screen().get_height() - self.world.floor:
            self.x += self.motion_x
            self.y += self.gravity_value
            self.gravity_value += self.deceleration
            self.gravity_value = max(min(self.gravity_value, 10), -10)
        else:
            self.to_floor()
        if (has_elapsed(self.creation_time, 3) or self.health <= 30) and not self.is_explosing:
            self.explosion_start()
            for entity in self.world.entities:
                if entity.type != self.type and entity != self:
                    if self.x - self.width//2 <= entity.x + entity.width//2 <= self.x + self.width//2 + self.width and self.y - entity.height//4 <= entity.y <= self.y + entity.height:
                        entity.damage(entity.health, DamageType.EXPLOSION, self.author)
                    elif self.x - self.width//2 - self.width <= entity.x + entity.width//2 <= self.x + self.width//2 + self.width*2 and self.y - entity.height//2 <= entity.y <= self.y + entity.height:
                        entity.damage(50, DamageType.EXPLOSION, self.author)
                    elif self.x - self.width//2 - self.width - 50 <= entity.x + entity.width//2 <= self.x + self.width//2 + self.width*2 + 50 and self.y - entity.height <= entity.y <= self.y + entity.height:
                        entity.damage(30, DamageType.EXPLOSION, self.author)
        if self.is_explosing and not round(self.explosion_frame) < len(self.sprites):
            self.death()

    def explosion_start(self) -> None:
        """Starts the explosion."""
        self.sprites = sprites.load(r"./resources/sprites/spells/explosion")
        self.sprite_selected = list(self.sprites.values())[0]
        self.max_height = 0
        self.max_width = 0
        for sprite in self.sprites:
            if self.max_height < self.sprites[sprite].get_height():
                self.max_height = self.sprites[sprite].get_height()
            if self.max_width < self.sprites[sprite].get_width():
                self.max_width = self.sprites[sprite].get_width()
        self.is_explosing = True
        from entities.livingentities.player_entity import PlayerEntity
        if isinstance(self.author, PlayerEntity):
            audio.play_sound("explosion.wav")
