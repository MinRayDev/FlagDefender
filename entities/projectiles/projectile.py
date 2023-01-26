from entities.Entity import Entity


class Projectile(Entity):
    def __init__(self, x: int, y: int, sprites_path: str, author: Entity):
        super().__init__(x, y, sprites_path, author.world, author.facing)
        self.author = author
