from LivingBeings import LivingBeing
from numpy import random


class IMove:
    def __init__(self, living_being: LivingBeing):
        self.living_being = living_being

    def move(self):
        pass


class CannotMove(IMove):
    def move(self):
        print(f"{self.living_being.__name__} cannot move!")


class CanMove(IMove):
    def move(self):
        if self.living_being.energy < 1:
            return

        empty_cells_around = self.living_being.forest.get_cells_with(None, self.living_being.position)
        new_random_position = empty_cells_around[random.randint(0, len(empty_cells_around), 1)[0]]

        self.living_being.forest.grid[new_random_position] = self.living_being
        self.living_being.forest.grid[self.living_being.position] = None
        self.living_being.position = new_random_position
