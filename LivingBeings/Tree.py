from LivingBeings import LivingBeing, Lumberjack, Bear
from LivingBeings.PrintColors import PrintColors as textColor


class Tree(LivingBeing.LivingBeing):
    default_monthly_energy = 0
    alive = []

    def __init__(self, position: tuple):
        super().__init__(position, monthly_energy=self.default_monthly_energy)
        Tree.alive.append(self)

    def display(self):
        return textColor.GREEN + "T" + textColor.ENDC

    def kill(self):
        return

    def move(self):
        return
