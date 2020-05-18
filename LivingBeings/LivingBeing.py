from numpy import random
import warnings
from LivingBeings.PrintColors import PrintColors as textColor

import Forest


class LivingBeing:
    default_monthly_energy = 0
    forest = None  # Set up to store forest reference. It will be needed for LivingBeing interaction with the world
    alive = []

    def __init__(self, position: tuple,
                 monthly_energy: int = default_monthly_energy):

        self.age = 0
        self.position = position
        self.monthly_energy = monthly_energy
        self.energy = monthly_energy

        LivingBeing.alive.append(self)

    def recover(self):
        self.energy = self.default_monthly_energy

    def move(self):
        if self.energy <= 0:
            return

        cells_around = LivingBeing.forest.get_cells_around(self.position)
        cell_to_move = cells_around[random.randint(0, len(cells_around), 1)[0]]
        LivingBeing.forest.move_living_being(self, cell_to_move)
        self.energy -= 1

    def kill(self):
        pass

    def display(self):
        pass

    def reproduce(self):
        pass

    @classmethod
    def set_forest(cls, forest: Forest):
        cls.forest = forest

    @classmethod
    def spawn_in_empty_space(cls, quantity, around: tuple = None):
        print(textColor.GREEN + f"Trying to create {quantity} {cls.__name__} around {around}." + textColor.ENDC)

        empty_cells = cls.forest.get_cells_with(None, around)

        if quantity > len(empty_cells):
            quantity = len(empty_cells)
            warnings.warn(f"Not enough empty spaces, reducing quantity to {len(empty_cells)}")

        for spawn in range(quantity):
            spawn_position = empty_cells.pop(random.randint(0, len(empty_cells), 1)[0])
            cls.forest.grid[spawn_position] = [cls(position=spawn_position)]

        print(textColor.GREEN + "\tCreated!" + textColor.ENDC)


class Lumberjack(LivingBeing):
    default_monthly_energy = 3
    lumber = 0
    alive = []

    def __init__(self, position: tuple):
        super().__init__(position, monthly_energy=self.default_monthly_energy)
        Lumberjack.alive.append(self)

    def display(self):
        return textColor.PURPLE + "L" + textColor.ENDC


class Bear(LivingBeing):
    default_monthly_energy = 5
    kills = 0
    alive = []

    def __init__(self, position: tuple):
        super().__init__(position, monthly_energy=self.default_monthly_energy)
        Bear.alive.append(self)

    def display(self):
        return textColor.RED + "B" + textColor.ENDC


class Tree(LivingBeing):
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
