import pygame
import GraphicalInterface.Camera
import GraphicalInterface.Grid
import GraphicalInterface.Static
from GraphicalInterface.Static import RGBColors
from GraphicalInterface.IAnimate import IAnimate


class GUI:
    def __init__(self,
                 grid_size: (int, int) = (20, 20),
                 tick_function=None,
                 month_function=None,
                 year_function=None,
                 main_folder="."
                 ):
        IAnimate.main_folder = main_folder
        pygame.init()
        self.display_surf = pygame.display.set_mode((1200, 600))

        size = GraphicalInterface.Grid.Grid.compute_grid_pixel_size((20, 20), main_folder + '/Grid/tile.png')
        self.camera = GraphicalInterface.Camera.Camera(self.display_surf, size,
                                                       subdisplay_size=(800, 600), subdisplay_position=(0, 0),
                                                       move_with_arrow_keys=True, move_with_wasd=True,
                                                       camera_velocity=100, zoom_velocity=100
                                                       )

        self.grid = GraphicalInterface.Grid.Grid(self.camera.scene_surface, grid_size, main_folder + '/Grid/tile.png')
        IAnimate.set_grid(self.grid)

        self.button_play_pause = GraphicalInterface.Static.ButtonOnOff(
            self.display_surf, (170, 500),
            main_folder + "/StaticSource/button_play.png",
            main_folder + "/StaticSource/button_play_over.png",
            main_folder + "/StaticSource/button_pause_over.png",
            main_folder + "/StaticSource/button_pause.png")
        self.button_tick = GraphicalInterface.Static.ButtonEvent(
            tick_function,
            self.display_surf, (270, 500),
            main_folder + "/StaticSource/button_tick.png",
            main_folder + "/StaticSource/button_tick_over.png",
            main_folder + "/StaticSource/button_tick_click.png")
        self.button_month = GraphicalInterface.Static.ButtonEvent(
            month_function,
            self.display_surf, (370, 500),
            main_folder + "/StaticSource/button_month.png",
            main_folder + "/StaticSource/button_month_over.png",
            main_folder + "/StaticSource/button_month_click.png")
        self.button_year = GraphicalInterface.Static.ButtonEvent(
            year_function,
            self.display_surf, (470, 500),
            main_folder + "/StaticSource/button_year.png",
            main_folder + "/StaticSource/button_year_over.png",
            main_folder + "/StaticSource/button_year_click.png")

        self.population_graph = GraphicalInterface.Static.Graph(self.display_surf, (820, 0), [3.5, 3])

        self.scrollbar_adjust_scale = GraphicalInterface.Static.ScrollBar(
            self.display_surf, (870, 300),
            main_folder + "/StaticSource/scrollbar_base_adjust_scale.png",
            main_folder + "/StaticSource/scrollbar_cursor_adjust_scale.png")
        self.scrollbar_adjust_offset = GraphicalInterface.Static.ScrollBar(
            self.display_surf, (870, 350),
            main_folder + "/StaticSource/scrollbar_base_adjust_scale.png",
            main_folder + "/StaticSource/scrollbar_cursor_adjust_scale.png",
            1)

        self.data = None

    def on_event(self, event):
        self.camera.on_event(event)
        self.button_play_pause.on_event(event)
        self.button_tick.on_event(event)
        self.button_month.on_event(event)
        self.button_year.on_event(event)
        self.scrollbar_adjust_scale.on_event(event)
        self.scrollbar_adjust_offset.on_event(event)

    def draw(self):
        self.display_surf.fill(RGBColors.White)
        self.camera.scene_surface.fill(RGBColors.Green)
        self.grid.draw()
        self.camera.draw()
        self.button_play_pause.draw()
        self.button_tick.draw()
        self.button_month.draw()
        self.button_year.draw()
        self.population_graph.draw(self.data)
        self.scrollbar_adjust_scale.draw()
        self.scrollbar_adjust_offset.draw()

    def update_population_graph_data(self, data):
        self.data = data


if __name__ == "__main__":
    gui = GUI()
    clock = pygame.time.Clock()
    data = {"Banana": {"x": [], "y": [], "style": "b", "orient": ""},
            "Potato": {"x": [], "y": [], "style": "g", "orient": ""}}

    while True:  # main game loop
        data["Banana"]["x"].append(pygame.time.get_ticks() / 1000)
        data["Potato"]["x"].append(pygame.time.get_ticks() / 1000)
        data["Banana"]["y"].append(pygame.time.get_ticks() * 2 / 1000)
        data["Potato"]["y"].append(pygame.time.get_ticks() / 1000)
        gui.update_population_graph_data(data)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            gui.on_event(event)

        gui.draw()
        pygame.display.update()
