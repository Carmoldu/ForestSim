from numpy import random
import warnings
from LivingBeings.Interfaces.IDisplay import PrintColors as textColor

import Forest
from LivingBeings.Interfaces import IMove, IKill, IDisplay, IReproduce


class LivingBeing:
    default_monthly_energy = 0
    forest = None  # Set up to store forest reference. It will be needed for LivingBeing interaction with the world
    alive = []

    @classmethod
    def set_forest(cls, forest: Forest):
        cls.forest = forest

    @classmethod
    def spawn_in_empty_space(cls, quantity, around: tuple = None):
        print(textColor.GREEN + f"Trying to create {quantity} {cls.__name__} around {around}." + textColor.ENDC)

        empty_cells = cls.forest.get_empty_cells(around)

        if quantity > len(empty_cells):
            quantity = len(empty_cells)
            warnings.warn(f"Not enough empty spaces, reducing quantity to {len(empty_cells)}")

        for spawn in range(quantity):
            spawn_position = empty_cells.pop(random.randint(0, len(empty_cells), 1)[0])
            cls.forest.grid[spawn_position] = cls(position=spawn_position)

        print(textColor.GREEN + "\tCreated!" + textColor.ENDC)

    def __init__(self, position: tuple,
                 move_behaviour: IMove.IMove = None,
                 reproduce_behaviour: IReproduce.IReproduce = None,
                 kill_behaviour: IKill.IKill = None,
                 display_behaviour: IDisplay.IDisplay = None,
                 monthly_energy: int = default_monthly_energy):

        self.age = 0
        self.position = position
        self.monthly_energy = monthly_energy
        self.energy = 0

        self.move_behaviour = move_behaviour
        self.reproduce_behaviour = reproduce_behaviour
        self.kill_behaviour = kill_behaviour
        self.display_behaviour = display_behaviour

        LivingBeing.alive.append(self)

    def recover(self):
        self.energy = self.monthly_energy

    def move(self):
        return self.move_behaviour.move()

    def kill(self):
        return self.kill_behaviour.kill()

    def display(self):
        return self.display_behaviour.display()

    def reproduce(self):
        return self.reproduce_behaviour.reproduce()









