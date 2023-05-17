from core.player import Player
from util.time_util import has_elapsed


class Spell:
    """Class 'Spell'."""

    @staticmethod
    def is_launchable(class_, author: Player) -> bool:
        """Check if a spell is launchable.

            :param class_: Class to check.
            :param author: Spell's author.
            :type author: Player.

            :return: True if it can be launched else False.
            :rtype: bool.

        """
        return class_ not in author.cooldowns.keys() or (
                class_ in author.cooldowns.keys() and
                has_elapsed(author.cooldowns[class_], + class_.cooldown)
        )
