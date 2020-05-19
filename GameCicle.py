import Forest
from LivingBeings import OutputUtilities
import random
import os


def tick(forest: Forest.Forest):
    random.shuffle(forest.get_living_beings_alive_list())
    for living_being in forest.get_living_beings_alive_list():
        living_being.move()

    random.shuffle(forest.get_living_beings_alive_list())
    for living_being in forest.get_living_beings_alive_list():
        living_being.kill()


def month(forest: Forest.Forest,
          current_tick=0,
          display_grid=True,
          display_grid_each_tick=False,
          display_statistics=True,
          stop_each_month=True):

    if stop_each_month:
        input("Press key to compute next month...")

    ticks_per_month = 5
    for t in range(current_tick, ticks_per_month):
        tick(forest)
        if display_grid_each_tick:
            print(f"-------------Tick {t}------------")
            forest.display_grid()

    for tree in forest.get_living_beings_alive_list(Forest.Tree.Tree):
        tree.reproduce()

    for living_being in forest.get_living_beings_alive_list():
        living_being.recover()

    if display_grid:
        forest.display_grid()

    if display_statistics:
        OutputUtilities.PrintPrefabs.population()
        OutputUtilities.PrintPrefabs.resources()


def year(forest: Forest.Forest,
         current_month=0,
         stop_each_month=True):
    months_per_year = 12

    for m in range(current_month, months_per_year):
        print(f"================= Month {m} ==================")
        month(forest,
              current_tick=0,
              display_grid=True,
              display_grid_each_tick=False,
              display_statistics=True,
              stop_each_month=stop_each_month)

    Forest.Lumberjack.Lumberjack.hire_or_fire_lumberjacks()
    Forest.Bear.Bear.introduce_or_expel()
    if not forest.get_living_beings_alive_list(Forest.Tree.Tree):
        Forest.Tree.Tree.spawn_in_empty_space(1)


def game_loop(height=20,
              width=20,
              init_default_options={"initial_percentage_lumberjacks": 0.1,
                                    "initial_percentage_trees": 0.5,
                                    "initial_percentage_bears": 0.02}):

    forest = Forest.Forest(height, width, init_default_options)
    forest.display_grid()

    year_count = 0

    while True:
        user_in = input("Press key to start next year! Press q to exit")
        if user_in == "q":
            break

        year_count += 1

        print("========================================================")
        print(f"================ YEAR {year_count} ==========================")
        print("========================================================")
        print("")
        year(forest)







