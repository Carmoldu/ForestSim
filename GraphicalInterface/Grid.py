import pygame
import numpy as np
from pygame.locals import *
from GraphicalInterface.Static import RGBColors


class Grid:  # Grid is presented in isometric view, hence tile image should be isometric too
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

        self.velocity = scroll_velocity
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False
        self.moving = False
        self.mouse_pos_at_click = None
        self.position_at_click = None

        self.zoom_factor = 1
        self.zoom_velocity = 0.01

    def draw(self):
        if self.camera_is_moving():
            self.update_camera_position()

        for draw_position in self.tile_positions.flatten():
            self.display_surface.blit(self.tile_source, draw_position)

    def update_tile_draw_position(self):
        draw_position = self.position
        for row_idx, row in enumerate(self.tile_positions):
            for tile_idx, tile in enumerate(row):
                self.tile_positions[row_idx, tile_idx] = draw_position
                draw_position = [draw_position[0] + self.tile_width / 2, draw_position[1] + self.tile_height / 2]
            draw_position = [row[0][0] - self.tile_width / 2, row[0][1] + self.tile_height / 2]

    def update_camera_position(self):
        if self.moving_right:
            self.position[0] -= self.velocity
        if self.moving_left:
            self.position[0] += self.velocity
        if self.moving_up:
            self.position[1] += self.velocity
        if self.moving_down:
            self.position[1] -= self.velocity

        if self.moving:
            mouse_pos = pygame.mouse.get_pos()
            self.position[0] = self.position_at_click[0] - self.mouse_pos_at_click[0] + mouse_pos[0]
            self.position[1] = self.position_at_click[1] - self.mouse_pos_at_click[1] + mouse_pos[1]

        if self.camera_is_moving():
            self.update_tile_draw_position()

    def on_event(self, event):
        if event.type == KEYDOWN and event.key in [K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_RIGHT, K_LEFT]:
            if (event.key == K_w or event.key == K_UP) and self.moving_down is False:
                self.moving_up = True
            elif (event.key == K_a or event.key == K_LEFT) and self.moving_right is False:
                self.moving_left = True
            elif (event.key == K_s or event.key == K_DOWN) and self.moving_up is False:
                self.moving_down = True
            elif (event.key == K_d or event.key == K_RIGHT) and self.moving_left is False:
                self.moving_right = True
        elif event.type == KEYUP and event.key in [K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_RIGHT, K_LEFT]:
            if event.key == K_w or event.key == K_UP:
                self.moving_up = False
            elif event.key == K_a or event.key == K_LEFT:
                self.moving_left = False
            elif event.key == K_s or event.key == K_DOWN:
                self.moving_down = False
            elif event.key == K_d or event.key == K_RIGHT:
                self.moving_right = False

        if event.type == MOUSEBUTTONDOWN:
            self.moving = True
            self.mouse_pos_at_click = pygame.mouse.get_pos()
            self.position_at_click = list(self.position)

            if event.button == 4:
                if self.zoom_factor > 0:
                    self.zoom_factor -= self.zoom_velocity
            elif event.button == 5:
                self.zoom_factor += self.zoom_velocity

        if event.type == MOUSEBUTTONUP:
            self.moving = False

    def camera_is_moving(self):
        return self.moving_down or self.moving_left or self.moving_right or self.moving_right or self.moving_up \
               or self.moving


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

            grid.on_event(event)
        DISPLAYSURF.fill(RGBColors.White)
        grid.draw()
        pygame.display.update()






