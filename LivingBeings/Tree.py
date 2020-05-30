from LivingBeings import LivingBeing, Lumberjack, Bear
from LivingBeings.PrintColors import PrintColors as textColor
from numpy import random
from GraphicalInterface import IAnimate


class Tree(LivingBeing.LivingBeing):
    default_monthly_energy = 0
    reproduction_chance = 0.1
    alive = []

    def __init__(self, position: tuple):
        super().__init__(position, self.default_monthly_energy, IAnimate.AnimationTree(position))
        Tree.alive.append(self)

    def display(self):
        return textColor.GREEN + "T" + textColor.ENDC

    def kill(self):
        return

    def move(self):
        return

    def reproduce(self):
        if random.rand() < self.reproduction_chance:
            self.spawn_in_empty_space(1, self.position)
