from LivingBeings import LivingBeing, Lumberjack, Bear
from LivingBeings.PrintColors import PrintColors as textColor
from numpy import random


class Tree(LivingBeing.LivingBeing):
    default_monthly_energy = 0
    reproduction_chance = 0.1
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

    def reproduce(self):
        if random.rand() < self.reproduction_chance:
            super().reproduce(self.position)
