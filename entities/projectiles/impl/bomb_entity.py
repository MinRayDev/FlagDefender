import time

from pygame import Surface

from core.world import Facing
from entities.entity import Entity, DamageType
from entities.projectiles.projectile import Projectile
from util import sprites, audio
from util.draw_util import draw_with_scroll
from util.instance import get_client


class BombEntity(Projectile):
    def __init__(self, x, y, author: Entity, inclinaison: int):
        super().__init__(x, y, r"./resources/sprites/spells/bomb", author, 60)
        self.creation_time = time.time()
        self.has_gravity = False
        self.type = author.type
        self.gravity_value = 0 - inclinaison  # vitesse verticale, negative : vers le haut, positive : vers le bas (-50 max, 0, 5)
        self.strength = 1
        self.has_collisions = False
        self.is_explosing = False
        self.explosion_frame = 0
        if inclinaison > 0:
            self.motion_x = (10 / (inclinaison + 1)) * 1.25 * self.strength  # vitesse horizontale
        else:
            self.motion_x = 10 * self.strength / 2
        self.acceleration = 0.1  # acceleration verticale
        match self.facing:
            case Facing.EAST:
                self.x += author.width
                self.y += 20
            case Facing.WEST:
                self.motion_x = -self.motion_x
                self.x -= self.width
                self.y += 20

    def draw(self, surface: Surface) -> None:
        if not self.is_explosing:
            draw_with_scroll(surface, self.sprite_selected, self.x, self.y)
        elif self.is_explosing and round(self.explosion_frame) < len(self.sprites):
            draw_with_scroll(surface, list(self.sprites.values())[round(self.explosion_frame)], self.x, self.y)
            self.explosion_frame += 0.4

    def activity(self):
        if self.y + self.height + self.gravity_value < get_client().get_screen().get_height() - self.world.floor:
            self.x += self.motion_x
            self.y += self.gravity_value
            self.gravity_value += self.acceleration
        if (time.time() > self.creation_time + 3 or self.health <= 30) and not self.is_explosing:
            self.explosion_start()
            for entity in self.world.entities:
                if entity.type != self.type and entity != self:
                    if self.x - self.width//2 <= entity.x <= self.x + self.width//2 + self.width and self.y - entity.height//4 <= entity.x <= self.y + entity.height:
                        entity.damage(entity.health, DamageType.EXPLOSION, self.author)
                    elif self.x - self.width//2 - self.width <= entity.x <= self.x + self.width//2 + self.width*2 and self.y - entity.height//2 <= entity.x <= self.y + entity.height:
                        entity.damage(50, DamageType.EXPLOSION, self.author)
                    elif self.x - self.width//2 - self.width - 50 <= entity.x <= self.x + self.width//2 + self.width*2 + 50 and self.y - entity.height <= entity.x <= self.y + entity.height:
                        entity.damage(30, DamageType.EXPLOSION, self.author)
        if self.is_explosing and not round(self.explosion_frame) < len(self.sprites):
            self.death()

    def explosion_start(self):
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
        from entities.livingentities.entity_player import PlayerEntity
        if isinstance(self.author, PlayerEntity):
            audio.play_song("explosion.wav")
