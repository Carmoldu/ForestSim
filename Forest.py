import numpy as np
import warnings
from LivingBeings import LivingBeing


class Forest:
    initDefaultOptions = {"initial_percentage_lumberjacks": 0.1,
                          "initial_percentage_trees": 0.5,
                          "initial_percentage_bears": 0.02}

    living_being_class = LivingBeing.LivingBeing

    def __init__(self, height: int = 20, width: int = 20,
                 options=initDefaultOptions):

        Forest.living_being_class.set_forest(self)

        self.grid = np.empty(shape=(height, width), dtype='object')
        self.height = height
        self.width = width

        number_of_trees = int(self.grid.size * options["initial_percentage_trees"])
        if number_of_trees == 0 and options["initial_percentage_trees"] != 0:
            number_of_trees = 1

        number_of_lumberjacks = int(self.grid.size * options["initial_percentage_lumberjacks"])
        if number_of_lumberjacks == 0 and options["initial_percentage_lumberjacks"] != 0:
            number_of_lumberjacks = 1

        number_of_bears = int(self.grid.size * options["initial_percentage_bears"])
        if number_of_bears == 0 and options["initial_percentage_bears"] != 0:
            number_of_bears = 1

        LivingBeing.Tree.spawn_in_empty_space(number_of_trees)
        LivingBeing.Lumberjack.spawn_in_empty_space(number_of_lumberjacks)
        LivingBeing.Bear.spawn_in_empty_space(number_of_bears)

    def get_cells_with(self, object=None, around: tuple = None):
        if around is None:
            return [(y, x) for y in range(self.height) for x in range(self.width) if self.grid[y, x] is object]
        else:
            surrounding_cells = self.get_cells_around(around)
            return[cell for cell in surrounding_cells if self.grid[cell] is object]

    def check_cell_in_forest_bounds(self, cell_position: (int, int)):
        assert cell_position[0] < self.height, \
            "Row number must be lower than grid height! Remember numbering starts at 0"

        assert cell_position[0] >= 0, \
            "Row number must be 0 or higher!"

        assert cell_position[1] < self.width, \
            "Column number must be lower than grid width! Remember numbering starts at 0"

        assert cell_position[1] >= 0, \
            "Column number must be 0 or higher!"

    def get_cells_around(self, around: tuple):
        self.check_cell_in_forest_bounds(around)

        min_row = around[0] - 1 if around[0] > 0 else 0
        max_row = around[0] + 1 if around[0] < self.height - 1 else self.height - 1

        min_column = around[1] - 1 if around[1] > 0 else 0
        max_column = around[1] + 1 if around[1] < self.width - 1 else self.width - 1

        return [(y, x) for y in range(min_row, max_row + 1) for x in range(min_column, max_column + 1)
                if (y, x) != around]

    def move_living_being(self, living_being: LivingBeing.LivingBeing, destination_cell: tuple):
        self.check_cell_in_forest_bounds(destination_cell)

        # Take out object from original cell. Set cell to None if empty
        origin_cell = living_being.position
        if origin_cell == destination_cell:
            warnings.warn("Tried to move living being to cell it is currently in!")
            return

        self.grid[origin_cell].remove(living_being)
        if not self.grid[origin_cell]:
            self.grid[origin_cell] = None

        # Move object to new cell. If destination cell is None, initialize element list.
        if self.grid[destination_cell] is None:
            self.grid[destination_cell] = [living_being]
        else:
            self.grid[destination_cell].append(living_being)

        living_being.position = destination_cell

    def get_living_beings_alive_list(self, living_being: LivingBeing = LivingBeing):
        return living_being.alive

    def display_grid(self):
        display_string = ''
        for row in self.grid:
            for cell in row:
                display_string += self.generate_cell_display(cell)
            display_string += '\n'

        print(display_string)

    def generate_cell_display(self, cell):
        if cell is None:
            return ".\t"

        display_string = ""
        for element in cell:
            display_string += element.display()

        display_string += "\t"
        return display_string
