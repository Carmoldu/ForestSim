from LivingBeings import LivingBeing, Lumberjack, Tree
from LivingBeings.PrintColors import PrintColors as textColor
from GraphicalInterface import IAnimate


class Bear(LivingBeing.LivingBeing):
    default_monthly_energy = 5
    kills = 0
    alive = []
    can_kill = {}

    def __init__(self, position: tuple):
        super().__init__(position, self.default_monthly_energy, IAnimate.AnimationBear(position))
        Bear.alive.append(self)

        if not Bear.can_kill:
            Bear.can_kill = {Lumberjack.Lumberjack}

    def kill(self):
        if super().kill():
            Bear.kills += 1

    def display(self):
        return textColor.RED + "B" + textColor.ENDC

    @classmethod
    def reset_kills(cls):
        cls.kills = 0

    @classmethod
    def introduce_or_expel(cls):
        if cls.kills > 0.2*len(Lumberjack.Lumberjack.alive):
            expelled_bear = cls.select_random_alive()
            print(f"Bear at {expelled_bear.position} has been expelled")
            cls.died(expelled_bear)
        else:
            print("A new bear has entered the map!")
            cls.spawn_in_empty_space()

        cls.kills = 0
