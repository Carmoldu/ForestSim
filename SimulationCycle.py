import Forest
from LivingBeings import OutputUtilities
import random
import matplotlib.pyplot as plt


class SimulationCycle:
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

        # Display the generated forest
        self.display_current_time()
        self.forest.display_grid()
        OutputUtilities.PrintPrefabs.population()
        OutputUtilities.PrintPrefabs.resources()
        self.update_population_history(is_year=True)

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

    def __advance_tick(self):
        """
        Advances time to next tick by running all the actions of a tick. Actions of tick are:
            - Shuffling list of living beings to ensure they are not in order hence a type has advantage over another
            - For each living being, move to adjacent cell and kill anything that it can kill in that cell
            - Updates the population history
            - Advances the tick count by one. If this was the last tick of the month, it calls the end-of-month actions
              by calling advance_month()
        :return: nothing
        """

        random.shuffle(self.forest.get_living_beings_alive_list())

        for living_being in self.forest.get_living_beings_alive_list():
            living_being.move()
            living_being.kill()

        self.update_population_history()

        self.tick_count += 1
        self.current_tick += 1
        if self.current_tick >= self.default_ticks_per_month:
            self.current_tick = 0
            self.__advance_month()

    def __advance_month(self):
        """
        Advances time to next month by running all the actions of the end of month. These actions are:
            - Trees reproducing
            - Living beings re-setting their energy
            - Updates the population history
            - Advances the month count by one. If this was the last month of the year, it calls the end-of-year actions
              by calling advance_year()
        :return: nothing
        """
        for tree in self.forest.get_living_beings_alive_list(Forest.Tree.Tree):
            tree.reproduce()

        for living_being in self.forest.get_living_beings_alive_list():
            living_being.recover()

        self.update_population_history(is_month=True)

        self.current_month += 1
        if self.current_month >= self.default_months_per_year:
            self.current_month = 0
            self.__advance_year()

    def __advance_year(self):
        """
        Advances time to next year by running all the actions of the end of year. These actions are:
            - Hire or fire lumberjacks
            - Introduce or expel bear
            - Spawn one tree if there are none
            - Updates the population history
            - Advances the year count by one.
        :return: nothing
        """
        Forest.Lumberjack.Lumberjack.hire_or_fire_lumberjacks()
        Forest.Bear.Bear.introduce_or_expel()
        if not self.forest.get_living_beings_alive_list(Forest.Tree.Tree):
            Forest.Tree.Tree.spawn_in_empty_space(1)

        self.update_population_history(is_year=True)

        self.current_year += 1

    def advance_to_next_tick(self, display: bool = True):
        self.__advance_tick()

        if display:
            self.display_current_time()
            self.forest.display_grid()
            OutputUtilities.PrintPrefabs.population()
            OutputUtilities.PrintPrefabs.resources()

    def advance_to_next_month(self, display: bool = True):
        for tick in range(self.current_tick, self.default_ticks_per_month):
            self.advance_to_next_tick(display=False)

        if display:
            self.display_grid_and_info()

    def advance_to_next_year(self, display: bool = True):
        for month in range(self.current_month, self.default_months_per_year):
            self.advance_to_next_month(display=False)

        if display:
            self.display_grid_and_info()

    def advance_x_years(self, years: int, display: bool = True):
        # Since we want to end at the same month and tick as the current ones but X years ahead, we save these
        end_month = self.current_month
        end_tick = self.current_tick

        # Advance to current year+X (note this will leave us at tick 0 and month 0 of that year)
        for a in range(years):
            self.advance_to_next_year(False)

        # Now, advance to the desired tick and month
        self.advance_x_months(end_month, False)
        self.advance_x_ticks(end_tick, False)

        if display:
            self.display_grid_and_info()

    def advance_x_months(self, months: int, display=True):
        # Since we want to end at the same tick as the current one but X months ahead, we save this
        end_tick = self.current_tick

        # Advance to current month+X (note this will leave us at tick 0 of that month)
        for a in range(months):
            self.advance_to_next_month(False)

        # Now, advance to the desired tick
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

    def plot_population_history(self,
                                ticks_to_display: int = None,
                                until_tick: int = None,
                                display_months: bool = True,
                                display_years: bool = True):

        # if until_tick was not introduced, set last tick to be the last simulated tick
        if until_tick is None:
            last_tick_idx = -1
            until_tick = self.tick_count
        else:
            # Find the index of the last occurrence of the last tick to show in the Ticks list
            last_tick_idx = self.index_of_last_occurrence_in_list(until_tick, self.population_history["Ticks"])

        # If the amount of ticks to display were not specified or if it was larger than the amount of ticks existing
        # from the beginning of the simulation to the last tick to display, set the first tick to show to be the first
        # of the simulation
        if ticks_to_display is None or until_tick - ticks_to_display <= 0:
            first_tick_idx = 0
            first_tick = 0
        else:
            first_tick = until_tick - ticks_to_display
            first_tick_idx = self.index_of_first_occurrence_in_list(first_tick, self.population_history["Ticks"])

        # Plot the line plots of the populations of living beings
        plt.plot(self.population_history["Ticks"][first_tick_idx:last_tick_idx],
                 self.population_history["Tree"][first_tick_idx:last_tick_idx],
                 label="Trees")
        plt.plot(self.population_history["Ticks"][first_tick_idx:last_tick_idx],
                 self.population_history["Lumberjack"][first_tick_idx:last_tick_idx],
                 label="Lumberjacks")
        plt.plot(self.population_history["Ticks"][first_tick_idx:last_tick_idx],
                 self.population_history["Bear"][first_tick_idx:last_tick_idx],
                 label="Bears")

        if display_months:
            # Find the first month line that should be shown
            first_tick_idx = self.index_of_closest_upper_value(first_tick, self.population_history["Month"]["Ticks"])
            last_tick_idx = self.index_of_closest_upper_value(until_tick, self.population_history["Month"]["Ticks"])

            # Plot them
            plt.vlines(self.population_history["Month"]["Ticks"][first_tick_idx:last_tick_idx],
                       [0] * len(self.population_history["Month"]["Ticks"][first_tick_idx:last_tick_idx]),
                       self.population_history["Month"]["MaxPopulation"][first_tick_idx:last_tick_idx],
                       linestyles="dotted", label="Months")

        if display_years:
            # Find the first month line that should be shown
            first_tick_idx = self.index_of_closest_upper_value(first_tick, self.population_history["Year"]["Ticks"])
            last_tick_idx = self.index_of_closest_upper_value(until_tick, self.population_history["Year"]["Ticks"])
            # Plot them
            plt.vlines(self.population_history["Year"]["Ticks"][first_tick_idx:last_tick_idx],
                       [0] * len(self.population_history["Year"]["Ticks"][first_tick_idx:last_tick_idx]),
                       self.population_history["Year"]["MaxPopulation"][first_tick_idx:last_tick_idx],
                       label="Years")

        # Graph options and show
        plt.grid(which="minor")
        plt.legend()
        plt.show()

    def plot_last_months(self,
                         months_to_display: int,
                         display_months: bool = True,
                         display_years: bool = True):
        ticks_to_display = months_to_display * self.default_ticks_per_month
        self.plot_population_history(ticks_to_display, None, display_months, display_years)

    def plot_last_years(self,
                        years_to_display: int = None,
                        display_months: bool = True,
                        display_years: bool = True):
        ticks_to_display = years_to_display * self.default_ticks_per_month * self.default_months_per_year
        self.plot_population_history(ticks_to_display, None, display_months, display_years)

    @classmethod
    def index_of_last_occurrence_in_list(cls, x, lst: list) -> int:
        return len(lst) - lst[::-1].index(x) - 1

    @classmethod
    def index_of_first_occurrence_in_list(cls, x, lst: list) -> int:
        return lst.index(x)

    @classmethod
    def index_of_closest_upper_value(cls, x, lst: list):
        for indx, element in enumerate(lst):
            if x <= element:
                return indx
        return None


