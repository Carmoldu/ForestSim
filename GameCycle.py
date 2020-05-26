import pygame
from pygame.locals import *
import SimulationCycle
from GraphicalInterface import *
import GraphicalInterface.GUI
import sys, os


class GameCycle:
    def __init__(self, n: int = 20, m: int = 20):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

        self.grid_x = n
        self.grid_y = m
        self.simulation = SimulationCycle.SimulationCycle()
        self.simulation.initialize_forest()
        self.gui = GraphicalInterface.GUI.GUI((self.grid_x, self.grid_y),
                                              self.simulation.advance_to_next_tick,
                                              self.simulation.advance_to_next_month,
                                              self.simulation.advance_to_next_year,
                                              os.path.dirname(sys.argv[0]) + "/GraphicalInterface"
                                              )
        self.ticks_shown = 0

    def on_init(self):
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        self.gui.on_event(event)

    def on_loop(self):
        self.gui.update_population_graph_data(self.adapt_population_history_to_plot())

    def on_render(self):
        self.gui.draw()
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init():
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()

    def adapt_population_history_to_plot(self):
        relative_position = self.gui.adjust_scale_scrollbar.relative_position()
        ticks = None

        if relative_position != 0:
            ticks = int(self.simulation.tick_count * (1 - relative_position) + self.simulation.default_months_per_year)

        if ticks != self.ticks_shown:
            self.gui.population_graph.clear()

        first_tick_idx, last_tick_idx, \
        fst_tick_idx_m, lst_tick_idx_m, \
        fst_tick_idx_y, lst_tick_idx_y = self.simulation.get_idxs_of_population_history(ticks)

        years_to_plot = (self.simulation.population_history["Ticks"][last_tick_idx]
                         - self.simulation.population_history["Ticks"][first_tick_idx])/\
                        (self.simulation.default_months_per_year * self.simulation.default_ticks_per_month)

        out = {"Trees": {"x": self.simulation.population_history["Ticks"][first_tick_idx:last_tick_idx],
                         "y": self.simulation.population_history["Tree"][first_tick_idx:last_tick_idx],
                         "style": "b", "orient": "h"},
               "Lumberjacks": {"x": self.simulation.population_history["Ticks"][first_tick_idx:last_tick_idx],
                               "y": self.simulation.population_history["Lumberjack"][first_tick_idx:last_tick_idx],
                               "style": "g", "orient": "h"},
               "Bears": {"x": self.simulation.population_history["Ticks"][first_tick_idx:last_tick_idx],
                         "y": self.simulation.population_history["Bear"][first_tick_idx:last_tick_idx],
                         "style": "r", "orient": "h"},
               "Months": {"x": self.simulation.population_history["Month"]["Ticks"][fst_tick_idx_m:lst_tick_idx_m],
                          "y": self.simulation.population_history["Month"]["MaxPopulation"][fst_tick_idx_m:lst_tick_idx_m],
                          "style": "dotted", "orient": "v"},
               "Years": {"x": self.simulation.population_history["Year"]["Ticks"][fst_tick_idx_y:lst_tick_idx_y],
                         "y": self.simulation.population_history["Year"]["MaxPopulation"][fst_tick_idx_y:lst_tick_idx_y],
                         "style": "solid", "orient": "v"}
               }

        if years_to_plot > 3:
            del out["Months"]
            self.gui.population_graph.clear()
        if years_to_plot > 50:
            del out["Years"]
            self.gui.population_graph.clear()

        return out


if __name__ == "__main__":
    game = GameCycle()
    game.on_execute()
