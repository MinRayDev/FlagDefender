from core.world import Facing, World
from entities.entity import Entity
from util.sprites import resize


class Mountain(Entity):
    """Class 'Mountain'.

        Extends 'Entity'.

    """
    def __init__(self, x: int, world: World, facing: Facing):
        """Constructor of the class 'Mountain'.

            :param x: The x coordinate of the entity.
            :type x: int.
            :param world: The world the entity is in.
            :type world: World.
            :param facing: The facing of the entity.
            :type facing: Facing.

        """
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
