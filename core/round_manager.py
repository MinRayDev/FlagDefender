import random
import time

from typing import TYPE_CHECKING

from util.logger import log

if TYPE_CHECKING:
    from core.level import Level
    from entities.livingentities.mob import Mob


class Round:
    """Class 'Round'.

        :ivar number: Round number.
        :type number: int.
        :ivar mobs: Round's mobs.
        :type mobs: list[Mob].
        :ivar start_time: Time at start of round.
        :type start_time: float.
        :ivar end_time: Time at end of round.
        :type end_time: float.

    """
    number: int
    mobs: 'list[Mob]'
    start_time: float
    end_time: float

    def __init__(self, number: int):
        """Constructor function for Round class.

            :param number: Round number.
            :type number: int.

        """
        self.number = number
        self.mobs = []
        self.start_time = time.time()
        self.end_time = 0

    def is_finished(self) -> bool:
        """Check if the round is finished.

            :return: True if finished else False.
            :rtype: bool.

        """
        return len(self.mobs) == 0

    def finish(self) -> None:
        """Finish the round by killing all the mobs in 'mobs'."""
        for mob in self.mobs.copy():
            mob.death()

    def generate_mobs(self, game_instance) -> None:
        """Spawn mobs."""
        from util.world_util import summon_mob
        from entities.livingentities.mobs.mob_fly_1 import MobFly1
        from entities.livingentities.mobs.mob_fly_2 import MobFly2
        from entities.livingentities.mobs.mob_tank import MobTank
        from entities.livingentities.mobs.mob_basic import MobBasic
        from entities.livingentities.mobs.mob_mortar import MobMortar
        from entities.livingentities.mobs.mob_speed import MobSpeed
        from entities.livingentities.mobs.mob_speed_physical import MobSpeedPhysical
        from core.world import World
        min_: int = self.number
        max_: int = self.number * 3
        types: list[tuple[object, int]] = [(MobBasic, -1)]
        if 5 <= self.number:
            types.append((MobSpeed, -1))
            types.append((MobSpeedPhysical, -1))
        if 10 <= self.number:
            types.append((MobMortar, -1))
        if 20 <= self.number:
            types.append((MobFly1, 30))
        if 30 <= self.number:
            types.append((MobFly2, 30))
        if 40 <= self.number:
            types.append((MobTank, 10))
        if 50 > self.number > 25:
            max_ = self.number * 2
        elif self.number >= 50:
            min_ = self.number//2
            max_ = self.number

        mob_count: int = random.randint(min_, max_)
        hells: tuple[World, World] = (game_instance.get_world_by_name("left_world"), game_instance.get_world_by_name("right_world"))
        for i in range(mob_count+1):
            mob = random.choice(types)
            if mob[1] != -1:
                while True:
                    count: int = 0
                    for mob_ in self.mobs:
                        if mob == type(mob_):
                            count += 1
                    if round((count/mob_count)*100, 0) <= mob[1]:
                        break
            if random.randint(0, 1) or mob[0] == MobMortar:
                # Left world
                if hells[0].has_player():
                    entity = summon_mob(mob[0], -2000, hells[0])
                    self.mobs.append(entity)
                else:
                    entity = summon_mob(mob[0], -9000, game_instance.get_world_by_name("overworld"))
                    self.mobs.append(entity)
            else:
                # Right world
                if hells[1].has_player():
                    entity = summon_mob(mob[0], 0, hells[1])
                    self.mobs.append(entity)
                else:
                    entity = summon_mob(mob[0], 9000, game_instance.get_world_by_name("overworld"))
                    log("Entity: " + str(entity), '\33[0;31m')
                    self.mobs.append(entity)


class RoundManager:
    """Class 'RoundManager'.

        :ivar round_: Current round.
        :type round_: Round.
        :ivar __level: Current level.
        :type __level: Level.
        :ivar can_summon: If entities can be summoned.
        :type can_summon: bool.
        :ivar passed_rounds: List of all past rounds.
        :type passed_rounds: list[Round].

    """
    round_: Round
    __level: 'Level'
    can_summon: bool
    passed_rounds: list[Round]

    def __init__(self, level: 'Level', summon: bool = True):
        """Constructor function for RoundManager class.

            :param level: Current level.
            :type level: Level.
            :param summon: If entities can be summoned.
            :type summon: bool.

        """
        self.round_ = Round(1)
        self.__level = level
        self.can_summon = summon
        if summon:
            self.round_.generate_mobs(level)

        self.passed_rounds = []

    def next_round(self) -> None:
        """Change the round and spawn new monsters."""
        self.passed_rounds.append(self.round_)
        self.round_ = Round(self.round_.number + 1)
        self.round_.generate_mobs(self.__level)

    def start(self) -> None:
        """Allows the round manager to spawn monsters."""
        self.can_summon = True
