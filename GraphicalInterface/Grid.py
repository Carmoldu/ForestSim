import pygame
import numpy as np
from pygame.locals import *
from GraphicalInterface.Static import RGBColors


class Grid:  # Grid is presented in isometric view, hence tile image should be isometric too
    static_elements = []

    def __init__(self,
                 display_surface: pygame.display,
                 grid_size: (int, int),
                 tile_img_source: str,
                 tile_pxl_size: (int, int) = None,
                 scroll_velocity: int = 10):
        self.display_surface = display_surface
        #self.zoom_surface = pygame.Surface((0, 0), self.display_surface.get_size())

        self.tile_source = pygame.image.load(tile_img_source)
        self.tile_rect = self.tile_source.get_rect()
        if tile_pxl_size is None:
            self.tile_height = abs(self.tile_rect.top - self.tile_rect.bottom)
            self.tile_width = abs(self.tile_rect.right - self.tile_rect.left)
        else:
            self.tile_height = tile_pxl_size[0]
            self.tile_width = tile_pxl_size[1]

        self.position = [self.display_surface.get_width() / 2, self.tile_height/2]

        self.tile_positions = np.empty(shape=(grid_size[0], grid_size[1]), dtype='object')
        self.update_tile_draw_position()

    def draw(self):
        for draw_position in self.tile_positions.flatten():
            self.display_surface.blit(self.tile_source, draw_position)

        for element in sorted(self.static_elements, key=lambda x: x.position):
            element.display_surface.blit(element.surface_base, self.draw_element(element))

    def update_tile_draw_position(self):
        draw_position = self.position
        for row_idx, row in enumerate(self.tile_positions):
            for tile_idx, tile in enumerate(row):
                self.tile_positions[row_idx, tile_idx] = draw_position
                draw_position = [draw_position[0] + self.tile_width / 2, draw_position[1] + self.tile_height / 2]
            draw_position = [row[0][0] - self.tile_width / 2, row[0][1] + self.tile_height / 2]

    def draw_element(self, element):
        return (int(element.position[0] - element.width / 2
                    + self.tile_width * (element.draw_offset[0] + 0.5)),
                int(element.position[1] + element.height / 2
                    - self.tile_height * (element.draw_offset[1] + 0.5)))

    @classmethod
    def compute_grid_pixel_size(cls, tiles: (int, int), source_image: str):
        tile_pixel_size = pygame.image.load(source_image).get_rect().size
        return ((int((tiles[0]+tiles[1])/2 + 1) * tile_pixel_size[0]),
                (int((tiles[0]+tiles[1])/2 + 1) * tile_pixel_size[1]))


if __name__ == "__main__":
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((900, 600))
    DISPLAYSURF.fill(RGBColors.White)
    pygame.display.set_caption('Grid test')
    grid = Grid(DISPLAYSURF, (20, 20), './Grid/tile.png')
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        DISPLAYSURF.fill(RGBColors.White)
        grid.draw()
        pygame.display.update()






