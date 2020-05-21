This program simulates an environment (a grid of NxM tiles) with the following different types of living beings. The
time in the simulation is discrete and organised as follows:
    - Tick: basic unit of time
    - Month: 5 ticks
    - Year: 12 months

The types of living beings inhabiting the forest are:
    - Trees:
        * Cannot move
        * Grow: between 0-12 months they are saplings, between 1year and 10 years they are trees and over 10 years they
          become elders (TBD)
        * Reproduce: Every month, each tree will try to reproduce. Reproducing will generate a sapling to an adjacent
          empty cell (if there are no empty cells, it will not be able ot reproduce). Reproduction chance will depend on
          the growth stage of the tree (sapling: 0%, tree: 10%, elder= 20%).
        Note: If at the end of the year there are no trees remaining, a tree will be spawn in a random empty spot.

    - Lumberjacks:
        * Move: Will move 3 times per month to a random adjacent cell
        * Harvest (kill): if a lumberjack is in the same cell as a Tree or an Elder, it will cut it down. This will stop
          its movement for the month and will add 1 lumber to a yearly count of lumber collected.
        * Hire and fire: at the end of the year, a N lumberjacks will be hired (and spawn in a random empty spot), where
          N = #lumber // # lumberjacks. If N < 1, a random lumberjack will be fired.

    - Bear:
        * Move: will move 5 times per month to a random adjacent cell
        * Maw (kill): if a bear is in the same cell as a Lumberjack, the Lumberjack will be killed. The bear will stop
          wandering that month and will add 1 kill to a yearly count of kills
        * Enter/expel from map: at the end of the year, if there have been any kills, a random bear will be expeled from
          the map. Else, a new bear will be introduced to a random empty spot of the map.
