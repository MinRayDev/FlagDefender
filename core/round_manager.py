import random
import time

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from entities.livingentities.mob import Mob


class Round:
    def __init__(self, number: int):
        self.number = number
        self.mobs: list[Mob] = []
        self.start_time = time.time()
        self.end_time = 0

    def is_finished(self):
        return len(self.mobs) == 0

    def finish(self):
        for mob in self.mobs.copy():
            mob.death()

    def generate_mobs(self, game_instance):
        from util.world_util import summon_mob
        from entities.livingentities.mobs.mob_fly_1 import MobFly1
        from entities.livingentities.mobs.mob_fly_2 import MobFly2
        from entities.livingentities.mobs.mob_tank import MobTank
        from entities.livingentities.mobs.mob_basic import MobBasic
        from entities.livingentities.mobs.mob_mortar import MobMortar
        from entities.livingentities.mobs.mob_speed import MobSpeed
        from entities.livingentities.mobs.mob_speed_physical import MobSpeedPhysical
        min_ = self.number
        max_ = self.number * 3
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

        mob_count = random.randint(min_, max_)
        hells = (game_instance.get_world_by_name("left_world"), game_instance.get_world_by_name("right_world"))
        for i in range(mob_count+1):
            mob = random.choice(types)
            if mob[1] != -1:
                while True:
                    count = 0
                    for mob_ in self.mobs:
                        if mob == type(mob_):
                            count += 1
                    if round((count/mob_count)*100, 0) <= mob[1]:
                        break
            if random.randint(0, 1) == 0:
                # left
                if hells[0].has_player():
                    entity = summon_mob(mob[0], -2000, hells[0])
                    self.mobs.append(entity)
                else:
                    entity = summon_mob(mob[0], 2000, game_instance.get_world_by_name("overworld"))
                    self.mobs.append(entity)
            else:
                if hells[1].has_player():
                    entity = summon_mob(mob[0], 0, hells[1])
                    self.mobs.append(entity)
                else:
                    entity = summon_mob(mob[0], 9000, game_instance.get_world_by_name("overworld"))
                    self.mobs.append(entity)


class RoundManager:
    def __init__(self, game_instance, summon: bool = True):
        self.round = Round(1)
        self.game_instance = game_instance
        self.can_summon = summon
        if summon:
            self.round.generate_mobs(game_instance)

        self.passed_rounds = []

    def get_round(self) -> Round:
        return self.round

    def next_round(self):
        self.passed_rounds.append(self.round)
        self.round = Round(self.round.number + 1)
        self.round.generate_mobs(self.game_instance)

    def start(self):
        self.can_summon = True
