from numpy import random
import warnings
from LivingBeings.PrintColors import PrintColors as textColor

import Forest


class LivingBeing:
    default_monthly_energy = 0
    forest = None  # Set up to store forest reference. It will be needed for LivingBeing interaction with the world
    alive = []
    can_kill = {}

    def __init__(self, position: (int, int),
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
        has_killed = False

        living_beings_in_cell = LivingBeing.forest.grid[self.position]
        for living_being in living_beings_in_cell:
            if (living_being is not self) and (type(living_being) in self.can_kill):
                type(living_being).died(living_being)
                self.energy = 0
                # print(f"{type(self).__name__} killed a {type(living_being).__name__} at {self.position}")
                has_killed = True

        return has_killed

    def display(self):
        pass

    @classmethod
    def set_forest(cls, forest: Forest):
        cls.forest = forest

    @classmethod
    def spawn_in_empty_space(cls, quantity=1, around: (int, int) = None):
        # print(textColor.GREEN + f"Trying to create {quantity} {cls.__name__} around {around}." + textColor.ENDC)
        empty_cells = cls.forest.get_cells_with(None, around)

        if not empty_cells:
            # print("\tNo space to spawn!")
            return

        if quantity > len(empty_cells):
            quantity = len(empty_cells)
            # warnings.warn(f"Not enough empty spaces, reducing quantity to {len(empty_cells)}")

        for spawn in range(quantity):
            spawn_position = empty_cells.pop(random.randint(0, len(empty_cells), 1)[0])
            cls.forest.grid[spawn_position] = [cls(position=spawn_position)]

        # print(textColor.GREEN + "\tCreated!" + textColor.ENDC)

    @classmethod
    def died(cls, living_being):
        LivingBeing.forest.grid[living_being.position].remove(living_being)
        cls.alive.remove(living_being)
        if living_being in LivingBeing.alive:
            LivingBeing.alive.remove(living_being)

    @classmethod
    def select_random_alive(cls):
        return cls.alive[random.randint(len(cls.alive))]



