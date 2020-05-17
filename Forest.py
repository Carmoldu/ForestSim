import numpy as np
from LivingBeings import LivingBeing


class Forest:
    initDefaultOptions = {"initial_percentage_lumberjacks": 0.1,
                          "initial_percentage_trees": 0.5,
                          "initial_percentage_bears": 0.02}

    def __init__(self, height: int = 20, width: int = 20,
                 options=initDefaultOptions,
                 living_being=LivingBeing.LivingBeing):

        living_being.set_forest(self)

        self.grid = np.empty(shape=(height, width), dtype='object')
        self.height = height
        self.width = width

        number_of_trees = int(self.grid.size * options["initial_percentage_trees"])
        number_of_lumberjacks = int(self.grid.size * options["initial_percentage_lumberjacks"])
        number_of_bears = int(self.grid.size * options["initial_percentage_bears"])

        LivingBeing.Tree.spawn_in_empty_space(number_of_trees)
        LivingBeing.Lumberjack.spawn_in_empty_space(number_of_lumberjacks)
        LivingBeing.Bear.spawn_in_empty_space(number_of_bears)

    def get_cells_with(self, object=None, around: tuple=None):
        if around is None:
            return [(y, x) for y in range(self.height) for x in range(self.width) if self.grid[y, x] is object]

        else:
            surrounding_cells = self.get_cells_around(around)

            return[cell for cell in surrounding_cells if self.grid[cell] is object]

    def get_cells_around(self, around: tuple):
        assert around[0] < self.height, "Row number must be lower than grid height! Remember numbering starts at 0"
        assert around[1] < self.width, "Column number must be lower than grid width! Remember numbering starts at 0"

        min_row = around[0] - 1 if around[0] > 0 else 0
        max_row = around[0] + 1 if around[0] < self.height - 1 else self.height - 1

        min_column = around[1] - 1 if around[1] > 0 else 0
        max_column = around[1] + 1 if around[1] < self.width - 1 else self.width - 1

        return [(y, x) for y in range(min_row, max_row + 1) for x in range(min_column, max_column + 1)
                if (y, x) != around]

    def display_grid(self):
        display_string = ''
        for row in self.grid:
            for element in row:
                if element is not None:
                    display_string += element.display()
                else:
                    display_string += '.  '

            display_string += '\n'

        print(display_string)
