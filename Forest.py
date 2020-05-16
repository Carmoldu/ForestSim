import numpy as np
import Trees, Bears, Lumberjacks


class Forest:
    initDefaultOptions = {"initial_percentage_lumberjacks": 0.1,
                          "initial_percentage_trees": 0.5,
                          "initial_percentage_bears": 0.2}

    def __init__(self, height: int = 20, width: int = 20, options=initDefaultOptions):
        self.grid = np.empty(shape=(height, width), dtype='object')
        self.height = height
        self.width = width

        number_of_cells = height * width
        number_of_trees = int(number_of_cells * options["initial_percentage_trees"])
        number_of_lumberjacks = int(number_of_cells * options["initial_percentage_lumberjacks"])
        number_of_bears = int(number_of_cells * options["initial_percentage_bears"])

        empty_cells = self.get_empty_cells()

        for tree_spawn in range(number_of_trees):
            tree_position = empty_cells.pop(np.random.randint(0, len(empty_cells), 1)[0])
            self.grid[tree_position] = Trees.Tree(position=tree_position)

        for lumberjack_spawn in range(number_of_lumberjacks):
            lumberjack_position = empty_cells.pop(np.random.randint(0, len(empty_cells), 1)[0])
            self.grid[lumberjack_position] = Lumberjacks.Lumberjack()

        for bear_spawn in range(number_of_bears):
            bear_position = empty_cells.pop(np.random.randint(0, len(empty_cells), 1)[0])
            self.grid[bear_position] = Bears.Bear()

    def get_empty_cells(self, around=None):
        if around is None:
            return [(y, x) for y in range(self.height) for x in range(self.width) if self.grid[y, x] is None]

        else:
            assert around[0] < self.height, "Row number must be lower than grid height! Remember numbering starts at 0"
            assert around[1] < self.width, "Column number must be lower than grid width! Remember numbering starts at 0"

            min_row = around[0] - 1 if around[0] > 0 else 0
            max_row = around[0] + 1 if around[0] < self.height - 1 else self.height - 1

            min_column = around[1] - 1 if around[1] > 0 else 0
            max_column = around[1] + 1 if around[1] < self.width - 1 else self.width - 1

            return[(y, x) for y in range(min_row, max_row+1) for x in range(min_column, max_column+1)
                   if self.grid[y, x] is None and (y, x) != around]

    def display_grid(self):
        display_string = ''
        for row in self.grid:
            for element in row:
                if element is not None:
                    display_string += element.display()
                else:
                    display_string += '.'

            display_string += '\n'

        print(display_string)