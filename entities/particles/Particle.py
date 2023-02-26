import pygame

from core.world import Facing, World
from entities.Object import Object


class Particle(Object):
    def __init__(self, x: int, y: int, world: World, facing: Facing):
        width, height = 1, 1
        self.test_x = 0
        self.test_y = 0
        match facing:
            case Facing.NORTH:
                x += 78 // 2 - 2
                width = 4
                height = y
                y = 0
                self.test_y = -1
            case Facing.EAST:
                x = x + 78
                y += 20
                width = 500-x
                height = 4
                self.test_x = 1
            case Facing.SOUTH:
                x += 78 // 2 - 2
                y = y + 80
                width = 4
                height = 500-y
                self.test_y = 1
            case Facing.WEST:
                y += 20
                height = 4
                width = x
                x = 0
                self.test_x = -1
        super().__init__(x, y, world, width, height)
        self.time_life = 0
        self.test = (self.x, 0)
        # pygame.draw.rect(surface, color, pygame.Rect(30, 30, 60, 60))

    def activity(self, **_):
        self.time_life += 1
        if self.time_life > 60*5:
            del self.world.entities[self.world.entities.index(self)]

    def draw(self, surface):
        self.test = (self.test[0]+3, self.test[1] + self.test_y)
        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(self.test[0], self.y-2, 16, self.height+4))
        if self.test[0] > self.x + self.width:
            del self.world.entities[self.world.entities.index(self)]
