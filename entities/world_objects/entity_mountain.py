from core.world import Facing
from entities.entity import Entity
from util.sprites import resize


class Mountain(Entity):
    def __init__(self, x: int, world, facing: Facing):
        super().__init__(x, 0, r"./resources/sprites/world/mountain", world)
        if facing == Facing.EAST:
            self.sprite_selected = resize(self.sprites["1"], 10)
            self.width = self.sprite_selected.get_width()
            self.height = self.sprite_selected.get_height()
        elif facing == Facing.WEST:
            self.sprite_selected = resize(self.sprites["0"], 10)
            self.width = self.sprite_selected.get_width()
            self.height = self.sprite_selected.get_height()
        self.to_floor()

    def activity(self):
        super().activity()
