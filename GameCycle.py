import pygame
from pygame.locals import *
import SimulationCycle
from GraphicalInterface import *


class GameCycle:
    def __init__(self, n: int = 20, m: int = 20):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

        self.grid_x = n
        self.grid_y = m
        self.simulation = SimulationCycle.SimulationCycle()
        self.simulation.initialize_forest()

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        pass

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


if __name__ == "__main__":
    game = GameCycle()
    game.on_execute()
