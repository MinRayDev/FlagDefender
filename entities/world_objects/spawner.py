from core.game import Game
from entities.Entity import Entity
from entities.Object import Object
from entities.livingentities.Mobtest import Mob
from utils import sprites
import random


class Spawner(Entity):
    def __init__(self, x, y, world):
        super().__init__(x, y, r"C:\Users\Gekota\Documents\Dev\Python\Game\resources\sprites\spawner", world)
        world.entities.append(self)
        self.y = Game.instance.screen.get_height() - Game.instance.actual_world.floor - self.height
        self.collisions = False

    def draw(self, surface):
        surface.blit(self.sprite_selected, (self.x+Game.instance.screen.get_width()//2 + Game.instance.scroll - Game.instance.main_player.entity.width//2, self.y))

    def activity(self):
        if random.randint(70, 5000) < 100:
            Mob(self.x, 0, Game.instance.actual_world)
