import pygame
from pygame.locals import *
from GraphicalInterface.Static import RGBColors

class Camera:
    def __init__(self,
                 display_surface: pygame.display,
                 scene_size: (int, int),
                 camera_velocity: int = 10,
                 zoom_velocity: int = 50,
                 reference_axis: int = 0,
                 subdisplay_size: (int, int) = None,
                 subdisplay_position: (int, int) = None,
                 move_with_mouse_wheel: bool = True,
                 move_with_wasd: bool = False,
                 move_with_arrow_keys: bool = False,
                 limit_camera_to_scene: bool = True):
        # Movement options
        self.move_with_mouse_wheel = move_with_mouse_wheel
        self.move_with_wasd = move_with_wasd
        self.move_with_arrow_keys = move_with_arrow_keys
        self.camera_velocity = camera_velocity
        self.zoom_velocity = zoom_velocity
        self.reference_axis = reference_axis  # 0 - x axis, 1 - y axis, -1 - re-scale both
        self.limit_camera_to_scene = limit_camera_to_scene

        # Set up surfaces
        self.display_surface = display_surface
        self.scene_surface = pygame.Surface(scene_size)


        if subdisplay_size is None or subdisplay_position is None:
            self.no_subdisplay = True
            self.subdisplay_surface = self.display_surface
            self.subdisplay_position = (0, 0)
        else:
            self.no_subdisplay = False
            self.subdisplay_surface = pygame.Surface(subdisplay_size)
            self.subdisplay_position = subdisplay_position

        self.scene_ratio = self.subdisplay_surface.get_size()[1] / self.subdisplay_surface.get_size()[0]
        self.zoom_size = [self.subdisplay_surface.get_size()[0], self.subdisplay_surface.get_size()[1]]
        self.in_camera_area = pygame.Rect(0, 0, *self.zoom_size)
        self.in_camera_area.center = self.scene_surface.get_rect().center
        self.retrieve_new_view()

        # Internal state
        self.moving = False
        self.moving_up = False
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.zoom_in = False
        self.zoom_out = False
        self.mouse_pos_at_click = None
        self.position_at_click = None
        self.camera_at_left_limit = False
        self.camera_at_right_limit = False
        self.camera_at_up_limit = False
        self.camera_at_bottom_limit = False
        self.zoom_in_limit = False
        self.zoom_out_limit = False
        self.over_display = False

    def draw(self):
        self.update_camera_position()
        self.retrieve_new_view()

    def retrieve_new_view(self):
        zoom_surf = pygame.Surface(self.in_camera_area.size)
        zoom_surf.blit(self.scene_surface, (0, 0), self.in_camera_area)
        if self.no_subdisplay:
            zoom_surf = self.rescale(zoom_surf, self.display_surface)
            self.display_surface.blit(zoom_surf, (0, 0))
        else:
            zoom_surf = self.rescale(zoom_surf, self.subdisplay_surface)
            self.subdisplay_surface.blit(zoom_surf, (0, 0))
            self.display_surface.blit(self.subdisplay_surface, self.subdisplay_position)

    def rescale(self, original_surface, display_surface):
        if self.reference_axis == 0:
            new_x = int(display_surface.get_size()[0])
            new_y = int(new_x * self.scene_ratio)
        elif self.reference_axis == 1:
            new_y = int(display_surface.get_size()[1])
            new_x = int(new_y / self.scene_ratio)
        else:
            new_x = int(display_surface.get_size()[0])
            new_y = int(display_surface.get_size()[1])

        return pygame.transform.scale(original_surface, (new_x, new_y))

    def update_camera_position(self):
        if self.limit_camera_to_scene:
            self.camera_at_limit()

        if self.moving_right and not self.camera_at_left_limit:
            self.in_camera_area = self.in_camera_area.move(-self.camera_velocity, 0)
        if self.moving_left and not self.camera_at_right_limit:
            self.in_camera_area = self.in_camera_area.move(self.camera_velocity, 0)
        if self.moving_up and not self.camera_at_bottom_limit:
            self.in_camera_area = self.in_camera_area.move(0, self.camera_velocity)
        if self.moving_down and not self.camera_at_up_limit:
            self.in_camera_area = self.in_camera_area.move(0, -self.camera_velocity)

        if self.moving:
            mouse_pos = pygame.mouse.get_pos()

            if (self.camera_at_up_limit and self.mouse_pos_at_click[1] - mouse_pos[1] < 0)\
                    or (self.camera_at_bottom_limit and self.mouse_pos_at_click[1] - mouse_pos[1] > 0):
                camera_vertical_movement = 0
            else:
                camera_vertical_movement = self.position_at_click[1] + self.mouse_pos_at_click[1] - mouse_pos[1] \
                                           - self.in_camera_area.center[1]

            if (self.camera_at_left_limit and self.mouse_pos_at_click[0] - mouse_pos[0] < 0)\
                    or (self.camera_at_right_limit and self.mouse_pos_at_click[0] - mouse_pos[0] > 0):
                camera_lateral_movement = 0
            else:
                camera_lateral_movement = self.position_at_click[0] + self.mouse_pos_at_click[0] - mouse_pos[0] \
                                           - self.in_camera_area.center[0]

            self.in_camera_area = self.in_camera_area.move(camera_lateral_movement, camera_vertical_movement)

    def update_camera_zoom(self):
        if self.zoom_in and not self.zoom_in_limit:
            self.in_camera_area = self.in_camera_area.inflate(-self.zoom_velocity, -self.zoom_velocity*self.scene_ratio)
        if self.zoom_out and not self.zoom_out_limit:
            self.in_camera_area = self.in_camera_area.inflate(self.zoom_velocity, self.zoom_velocity*self.scene_ratio)

    def on_event(self, event):
        if event.type == KEYDOWN and event.key in [K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_RIGHT, K_LEFT]:
            if (event.key == K_w and self.move_with_wasd
                or event.key == K_UP and self.move_with_arrow_keys) \
                    and self.moving_down is False:
                self.moving_up = True
            elif (event.key == K_a and self.move_with_wasd
                  or event.key == K_LEFT and self.move_with_arrow_keys) \
                    and self.moving_right is False:
                self.moving_left = True
            elif (event.key == K_s and self.move_with_wasd
                  or event.key == K_DOWN and self.move_with_arrow_keys) \
                    and self.moving_up is False:
                self.moving_down = True
            elif (event.key == K_d and self.move_with_wasd
                  or event.key == K_RIGHT and self.move_with_arrow_keys) \
                    and self.moving_left is False:
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
            if self.move_with_mouse_wheel and self.over_display and event.button == 2:
                self.moving = True
                self.mouse_pos_at_click = pygame.mouse.get_pos()
                self.position_at_click = list(self.in_camera_area.center)

            if event.button == 4:
                self.zoom_in = True
            elif event.button == 5:
                self.zoom_out = True
            self.update_camera_zoom()

        if event.type == MOUSEBUTTONUP:
            self.moving = False
            self.zoom_in = False
            self.zoom_out = False

        if event.type == MOUSEMOTION:
            if self.coordinate_is_over_display(pygame.mouse.get_pos()):
                self.over_display = True
            else:
                self.over_display = False

    def camera_is_moving(self):
        return self.moving_down or self.moving_left or self.moving_right or self.moving_right or self.moving_up \
               or self.moving

    def camera_at_limit(self):
        # Movement limits
        if self.in_camera_area.left - self.camera_velocity <= 0:
            self.camera_at_left_limit = True
            self.in_camera_area.left = 0
        else:
            self.camera_at_left_limit = False

        if self.in_camera_area.right + self.camera_velocity >= self.scene_surface.get_rect().size[0]:
            self.camera_at_right_limit = True
            self.in_camera_area.right = self.scene_surface.get_rect().size[0]
        else:
            self.camera_at_right_limit = False

        if self.in_camera_area.top - self.camera_velocity <= 0:
            self.camera_at_up_limit = True
            self.in_camera_area.top = 0
        else:
            self.camera_at_up_limit = False

        if self.in_camera_area.bottom + self.camera_velocity >= self.scene_surface.get_rect().size[1]:
            self.camera_at_bottom_limit = True
            self.in_camera_area.bottom = self.scene_surface.get_rect().size[1]
        else:
            self.camera_at_bottom_limit = False

        # Zoom limits
        if self.in_camera_area.size[0] - self.zoom_velocity < 0 or self.in_camera_area.size[1] - self.zoom_velocity < 0:
            self.zoom_in_limit = True
        else:
            self.zoom_in_limit = False

        if self.in_camera_area.size[0] + self.zoom_velocity > self.scene_surface.get_rect().size[0] \
                or self.in_camera_area.size[1] + self.zoom_velocity > self.scene_surface.get_rect().size[1]:
            self.zoom_out_limit = True
        else:
            self.zoom_out_limit = False

    def coordinate_is_over_display(self, coordinates: (int, int)):
        if self.subdisplay_surface.get_rect().right > coordinates[0] > self.subdisplay_surface.get_rect().left \
                and self.subdisplay_surface.get_rect().top < coordinates[1] < self.subdisplay_surface.get_rect().bottom:
            return True
        return False



if __name__ == "__main__":
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((900, 600))

    pygame.display.set_caption('Camera test')

    scene_example = pygame.image.load("SceneTest.png")
    camera = Camera(DISPLAYSURF, scene_example.get_rect().size,
                    subdisplay_size=(600, 500), subdisplay_position=(30, 30),
                    move_with_arrow_keys=True, move_with_wasd=True
                    )
    camera.scene_surface.blit(scene_example, (0, 0))

    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            camera.on_event(event)

        DISPLAYSURF.fill(RGBColors.White)
        camera.draw()
        pygame.display.update()



