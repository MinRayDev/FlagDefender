from core.player import Player
from util.time_util import has_elapsed


class Spell:
    @staticmethod
    def is_launchable(class_, author: Player) -> bool:
        return class_ not in author.cooldowns.keys() or (
                class_ in author.cooldowns.keys() and
                has_elapsed(author.cooldowns[class_], + class_.cooldown)
        )
