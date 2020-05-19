from LivingBeings import LivingBeing, Bear, Tree
from LivingBeings.PrintColors import PrintColors as textColor


class Lumberjack(LivingBeing.LivingBeing):
    default_monthly_energy = 3
    lumber = 0
    alive = []
    can_kill = {}

    def __init__(self, position: tuple):
        super().__init__(position, monthly_energy=self.default_monthly_energy)
        Lumberjack.alive.append(self)

        if not Lumberjack.can_kill:
            Lumberjack.can_kill = {Tree.Tree}

    def kill(self):
        if super().kill():
            Lumberjack.lumber += 1

    def display(self):
        return textColor.PURPLE + "L" + textColor.ENDC
