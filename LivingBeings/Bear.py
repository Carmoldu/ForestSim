from LivingBeings import LivingBeing, Lumberjack, Tree
from LivingBeings.PrintColors import PrintColors as textColor


class Bear(LivingBeing.LivingBeing):
    default_monthly_energy = 5
    kills = 0
    alive = []
    can_kill = {}

    def __init__(self, position: tuple):
        super().__init__(position, monthly_energy=self.default_monthly_energy)
        Bear.alive.append(self)

        if not Bear.can_kill:
            Bear.can_kill = {Lumberjack.Lumberjack}

    def kill(self):
        if super().kill():
            Bear.kills += 1

    def display(self):
        return textColor.RED + "B" + textColor.ENDC