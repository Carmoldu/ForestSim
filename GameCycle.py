import Forest
from LivingBeings import OutputUtilities
import random
import matplotlib.pyplot as plt


class GameCycle:
    default_ticks_per_month = 5
    default_months_per_year = 12
    default_forest_initialization = {"initial_percentage_lumberjacks": 0.1,
                                     "initial_percentage_trees": 0.5,
                                     "initial_percentage_bears": 0.02}
    default_population_history = {"Tree": [],
                                  "Lumberjack": [],
                                  "Bear": [],
                                  "Ticks": [],
                                  "Month": {"Ticks": [],
                                            "MaxPopulation": []},
                                  "Year": {"Ticks": [],
                                           "MaxPopulation": []}}

    def __init__(self, forest=None,
                 initial_tick=0, initial_month=0, initial_year=0,
                 imported_population_history=default_population_history):
        self.population_history = imported_population_history
        self.forest = forest
        self.current_year = initial_year
        self.current_month = initial_month
        self.current_tick = initial_tick

        if not imported_population_history["Ticks"]:
            self.tick_count = 0
            self.max_population = 0
        else:
            self.tick_count = max(imported_population_history["Ticks"])
            self.max_population = max(imported_population_history["MonthMax"])

    def initialize_forest(self, height=15, width=15, init_default_options=default_forest_initialization):
        self.forest = Forest.Forest(height, width, init_default_options)
        self.display_current_time()
        self.forest.display_grid()
        OutputUtilities.PrintPrefabs.population()
        OutputUtilities.PrintPrefabs.resources()
        self.update_population_history()

    def update_population_history(self, is_month=False, is_year=False):
        self.population_history["Ticks"].append(self.tick_count)
        self.population_history["Tree"].append(len(Forest.Tree.Tree.alive))
        self.population_history["Bear"].append(len(Forest.Bear.Bear.alive))
        self.population_history["Lumberjack"].append(len(Forest.Lumberjack.Lumberjack.alive))

        if len(Forest.Tree.Tree.alive) > self.max_population:
            self.max_population = len(Forest.Tree.Tree.alive)
        if len(Forest.Bear.Bear.alive) > self.max_population:
            self.max_population = len(Forest.Bear.Bear.alive)
        if len(Forest.Lumberjack.Lumberjack.alive) > self.max_population:
            self.max_population = len(Forest.Lumberjack.Lumberjack.alive)

        if is_month and not is_year:
            self.population_history["Month"]["Ticks"].append(self.tick_count)
            self.population_history["Month"]["MaxPopulation"].append(self.max_population)
        elif is_year:
            self.population_history["Year"]["Ticks"].append(self.tick_count)
            self.population_history["Year"]["MaxPopulation"].append(self.max_population)

    def advance_tick(self):
        random.shuffle(self.forest.get_living_beings_alive_list())
        for living_being in self.forest.get_living_beings_alive_list():
            living_being.move()

        random.shuffle(self.forest.get_living_beings_alive_list())
        for living_being in self.forest.get_living_beings_alive_list():
            living_being.kill()

        self.update_population_history()

        self.tick_count += 1
        self.current_tick += 1
        if self.current_tick >= self.default_ticks_per_month:
            self.current_tick = 0
            self.advance_month()

    def advance_month(self):
        for tree in self.forest.get_living_beings_alive_list(Forest.Tree.Tree):
            tree.reproduce()

        for living_being in self.forest.get_living_beings_alive_list():
            living_being.recover()

        self.update_population_history(is_month=True)

        self.current_month += 1
        if self.current_month >= self.default_months_per_year:
            self.current_month = 0
            self.advance_year()

    def advance_year(self):
        Forest.Lumberjack.Lumberjack.hire_or_fire_lumberjacks()
        Forest.Bear.Bear.introduce_or_expel()
        if not self.forest.get_living_beings_alive_list(Forest.Tree.Tree):
            Forest.Tree.Tree.spawn_in_empty_space(1)

        self.update_population_history(is_year=True)

        self.current_year += 1

    def advance_to_next_tick(self, display=True):
        self.advance_tick()

        if display:
            self.display_current_time()
            self.forest.display_grid()
            OutputUtilities.PrintPrefabs.population()
            OutputUtilities.PrintPrefabs.resources()

    def advance_to_next_month(self, display=True):
        for tick in range(self.current_tick, self.default_ticks_per_month):
            self.advance_to_next_tick(display=False)

        if display:
            self.display_grid_and_info()

    def advance_to_next_year(self, display=True):
        for month in range(self.current_month, self.default_months_per_year):
            self.advance_to_next_month(display=False)

        if display:
            self.display_grid_and_info()

    def advance_x_years(self, years: int, display=True):
        end_month = self.current_month
        end_tick = self.current_tick

        for a in range(years):
            self.advance_to_next_year(False)

        self.advance_x_months(end_month, False)
        self.advance_x_ticks(end_tick, False)

        if display:
            self.display_grid_and_info()

    def advance_x_months(self, months: int, display=True):
        end_tick = self.current_tick

        for a in range(months):
            self.advance_to_next_month(False)
        self.advance_x_ticks(end_tick, False)

        if display:
            self.display_grid_and_info()

    def advance_x_ticks(self, ticks: int, display=True):
        for a in range(ticks):
            self.advance_to_next_tick(False)

        if display:
            self.display_grid_and_info()

    def display_current_time(self):
        print(f"Tick: {self.current_tick}\t"
              f"Month: {self.current_month}\t"
              f"Year: {self.current_year}\t"
              f"Total ticks: {self.tick_count}")

    def display_grid_and_info(self):
        self.display_current_time()
        self.forest.display_grid()
        OutputUtilities.PrintPrefabs.population()
        OutputUtilities.PrintPrefabs.resources()

    def plot_population_history(self, years_to_display=None, until_year=None, display_months=True, display_years=True):
        if until_year is None:
            last_tick_position = -1
            until_year = self.current_year
        else:
            last_tick_to_show = self.population_history["Year"]["Ticks"][until_year]
            last_tick_position = self.population_history["Ticks"].index(last_tick_to_show)

        if years_to_display is None or until_year - years_to_display <= 0:
            first_tick_position = 0
            first_year = 0
        else:
            first_year = until_year - years_to_display - 1
            first_tick_to_show = self.population_history["Year"]["Ticks"][first_year]
            first_tick_position = self.population_history["Ticks"].index(first_tick_to_show)

        plt.plot(self.population_history["Ticks"][first_tick_position:last_tick_position],
                 self.population_history["Tree"][first_tick_position:last_tick_position],
                 label="Trees")
        plt.plot(self.population_history["Ticks"][first_tick_position:last_tick_position],
                 self.population_history["Lumberjack"][first_tick_position:last_tick_position],
                 label="Lumberjacks")
        plt.plot(self.population_history["Ticks"][first_tick_position:last_tick_position],
                 self.population_history["Bear"][first_tick_position:last_tick_position],
                 label="Bears")
        '''
        if display_months:
            plt.vlines(self.population_history["Month"]["Ticks"],
                       [0] * len(self.population_history["Month"]["Ticks"]),
                       self.population_history["Month"]["MaxPopulation"],
                       linestyles="dotted", label="Months")
        '''
        if display_years:
            plt.vlines(self.population_history["Year"]["Ticks"][first_year:until_year],
                       [0] * len(self.population_history["Year"]["Ticks"][first_year:until_year]),
                       self.population_history["Year"]["MaxPopulation"][first_year:until_year],
                       label="Years")

        plt.grid(which="minor")
        plt.legend()
        plt.show()
