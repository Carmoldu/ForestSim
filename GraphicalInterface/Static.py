import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pygame
from pygame.locals import *


class RGBColors:
    Aqua = (0, 255, 255)
    Black = (0, 0, 0)
    Blue = (0, 0, 255)
    Fuchsia = (255, 0, 255)
    Gray = (128, 128, 128)
    Green = (0, 128, 0)
    Lime = (0, 255, 0)
    Maroon = (128, 0, 0)
    NavyBlue = (0, 0, 128)
    Olive = (128, 128, 0)
    Purple = (128, 0, 128)
    Red = (255, 0, 0)
    Silver = (192, 192, 192)
    Teal = (0, 128, 128)
    White = (255, 255, 255)
    Yellow = (255, 255, 0)
    Transparent = (0, 0, 0, 0)


class Button:
    def __init__(self,
                 display_surface: pygame.display,
                 position: (int, int),
                 path_to_base_image: str,
                 path_to_over_image: str = None,
                 path_to_pressed_image: str = None,
                 # button_description: str = None
                 ):
        self.display_surface = display_surface
        self.position = position

        self.surface_base = pygame.image.load(path_to_base_image)
        self.button_rectObj = self.surface_base.get_rect()

        if path_to_over_image is None:
            self.surface_over = None
        else:
            self.surface_over = pygame.image.load(path_to_over_image)

        if path_to_pressed_image is None:
            self.surface_pressed = None
        else:
            self.surface_pressed = pygame.image.load(path_to_pressed_image)

        '''self.button_description = button_description
        if button_description is not None:
            self.font = pygame.font.Font('freesansbold.ttf', 10)
            self.description_surface = self.font.render(self.button_description, True, RGBColors.Green, RGBColors.Blue)
            self.description_RectObj = self.description_surface.get_rect()
            self.description_RectObj.top = self.button_rectObj.bottom
            self.description_RectObj.left = self.button_rectObj.left'''

        self.over = False  # Tracks if the cursor is over the button
        self.pressed = False  # Tracks if the button is being pressed by the cursor

    def draw(self):
        if self.pressed and self.surface_pressed is not None:
            self.display_surface.blit(self.surface_pressed, self.position)
        elif self.over and self.surface_over is not None:
            self.display_surface.blit(self.surface_over, self.position)
        else:
            self.display_surface.blit(self.surface_base, self.position)

        '''if self.over and self.button_description is not None:
            self.display_surface.blit(self.description_surface, self.description_RectObj)'''

    def coordinate_is_over_button(self, coordinates: (int, int)):
        if self.button_rectObj.right > coordinates[0] - self.position[0] > self.button_rectObj.left \
                and self.button_rectObj.top < coordinates[1] - + self.position[1] < self.button_rectObj.bottom:
            return True
        return False


class ButtonOnOff(Button):
    def __init__(self,
                 display_surface: pygame.display,
                 position: (int, int),
                 path_to_off_image: str,
                 path_to_over_image_off: str = None,
                 path_to_over_image_on: str = None,
                 path_to_on_image: str = None,
                 # button_description: str = None
                 ):
        super().__init__(display_surface, position,
                         path_to_base_image=path_to_off_image,
                         path_to_pressed_image=path_to_on_image)
        self.surface_over_on = pygame.image.load(path_to_over_image_on)
        self.surface_over_off = pygame.image.load(path_to_over_image_off)

    def on_event(self, event):
        if event.type == MOUSEMOTION:
            if self.coordinate_is_over_button(pygame.mouse.get_pos()):
                self.over = True
            else:
                self.over = False

        if event.type == MOUSEBUTTONDOWN and self.over and not self.pressed:
            self.pressed = True
        elif event.type == MOUSEBUTTONDOWN and self.over and self.pressed:
            self.pressed = False

    def draw(self):
        if self.over \
                and (self.surface_over_off is not None) \
                and not self.pressed:
            self.display_surface.blit(self.surface_over_off, self.position)
        elif self.over \
                and (self.surface_over_on is not None) \
                and self.pressed:
            self.display_surface.blit(self.surface_over_on, self.position)
        elif self.pressed and self.surface_pressed is not None:
            self.display_surface.blit(self.surface_pressed, self.position)
        else:
            self.display_surface.blit(self.surface_base, self.position)

    def get_state(self):
        return self.pressed


class ButtonEvent(Button):
    def __init__(self,
                 linked_function,
                 display_surface: pygame.display,
                 position: (int, int),
                 path_to_base_image: str,
                 path_to_over_image: str = None,
                 path_to_pressed_image: str = None,
                 # button_description: str = None
                 ):
        self.linked_function = linked_function
        super().__init__(display_surface, position, path_to_base_image, path_to_over_image, path_to_pressed_image)

    def on_event(self, event, function_args=[]):
        if event.type == MOUSEMOTION:
            if self.coordinate_is_over_button(pygame.mouse.get_pos()):
                self.over = True
            else:
                self.over = False

        if event.type == MOUSEBUTTONDOWN and self.over:
            self.pressed = True
            self.linked_function(*function_args)
        else:
            self.pressed = False


class ScrollBar:
    def __init__(self,
                 display_surface: pygame.display,
                 position: (int, int),
                 path_to_base_image: str,
                 path_to_cursor_image: str = None,
                 # description: str = None,
                 initial_position: float = 0
                 ):
        self.display_surface = display_surface
        self.position = position

        self.base_surface = pygame.image.load(path_to_base_image)
        self.base_rectObj = self.base_surface.get_rect()
        self.base_rectObj.left = position[0]
        self.base_rectObj.top = position[1]

        self.cursor_surface = pygame.image.load(path_to_cursor_image)
        self.cursor_rectObj = self.cursor_surface.get_rect()

        self.cursor_rectObj.centery = self.base_rectObj.centery
        self.cursor_rectObj.left = self.base_rectObj.left
        self.cursor_width = self.cursor_rectObj.right - self.cursor_rectObj.left
        initial_cursor_position = self.base_rectObj.left + \
                                  (self.base_rectObj.right - self.base_rectObj.left) * initial_position
        self.move_cursor(initial_cursor_position)

        self.over_cursor = False
        self.pressed_cursor = False
        self.engaged = False

    def draw(self):
        self.display_surface.blit(self.base_surface, self.position)
        self.display_surface.blit(self.cursor_surface, self.cursor_rectObj)

    def coordinate_is_over_cursor(self, coordinates: (int, int)):
        if self.cursor_rectObj.right > coordinates[0] > self.cursor_rectObj.left \
                and self.cursor_rectObj.top < coordinates[1] < self.cursor_rectObj.bottom:
            return True
        return False

    def on_event(self, event):
        if event.type == MOUSEMOTION:
            if self.coordinate_is_over_cursor(pygame.mouse.get_pos()):
                self.over_cursor = True
            else:
                self.over_cursor = False
    
        if event.type == MOUSEBUTTONDOWN and self.over_cursor:
            self.engaged = True

        if event.type == MOUSEBUTTONUP and self.engaged:
            self.engaged = False

        if self.engaged:
            self.move_cursor(pygame.mouse.get_pos()[0])

    def move_cursor(self, new_position: int):
        if new_position < self.base_rectObj.left + self.cursor_width/2:
            new_position = self.base_rectObj.left + self.cursor_width/2
        elif new_position > self.base_rectObj.right - self.cursor_width/2:
            new_position = self.base_rectObj.right - self.cursor_width/2

        self.cursor_rectObj.centerx = new_position

    def relative_position(self):
        return abs(round((self.cursor_rectObj.centerx - self.cursor_width/2 - self.base_rectObj.left) /
                         (self.base_rectObj.right - self.base_rectObj.left - self.cursor_width), 2))


class Graph:
    def __init__(self,
                 display_surface,
                 position: (int, int),
                 size: [int, int]):
        self.display_surface = display_surface
        self.position = position

        self.fig = plt.figure(figsize=size)
        self.ax = self.fig.add_subplot(111)
        self.canvas = agg.FigureCanvasAgg(self.fig)

    def draw(self, data: dict):
        for key in data.keys():
            if data[key]["orient"] == "v":
                self.ax.vlines(data[key]["x"], [0] * len(data[key]["x"]), data[key]["y"], linestyles=data[key]["style"])
            else:
                self.ax.plot(data[key]['x'], data[key]['y'], data[key]['style'])
        self.canvas.draw()
        renderer = self.canvas.get_renderer()

        raw_data = renderer.tostring_rgb()
        size = self.canvas.get_width_height()

        self.display_surface.blit(pygame.image.fromstring(raw_data, size, "RGB"), self.position)

    def clear(self):
        self.ax.clear()


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((900, 600))
    pygame.display.set_caption('Static elements test')
    DISPLAYSURF.fill(RGBColors.White)

    def button_clicked(buttonState: bool):
        print(f"On/off button is {buttonState}")

    button1 = ButtonEvent(button_clicked,
                          DISPLAYSURF, (30, 30),
                          "./StaticSource/Button1_not_pressed.png",
                          "./StaticSource/Button1_over.png",
                          "./StaticSource/Button1_pressed.png")

    button2 = ButtonOnOff(DISPLAYSURF, (300, 30),
                          "./StaticSource/Button1_not_pressed.png",
                          "./StaticSource/Button1_over.png",
                          "./StaticSource/Button1_over.png",
                          "./StaticSource/Button1_pressed.png")

    scrollbar1 = ScrollBar(DISPLAYSURF, (120, 120),
                           "./StaticSource/Scrollbar_base.png",
                           "./StaticSource/Scrollbar_cursor.png", 1)

    graph1 = Graph(DISPLAYSURF, (300, 300), [3, 3])

    data = {"Banana": {"x": [], "y": [], "style": "b", "orient": ""},
            "Potato": {"x": [], "y": [], "style": "g", "orient": ""}}

    while True:  # main game loop
        data["Banana"]["x"].append(pygame.time.get_ticks()/1000)
        data["Potato"]["x"].append(pygame.time.get_ticks()/1000)
        data["Banana"]["y"].append(pygame.time.get_ticks()*2/1000)
        data["Potato"]["y"].append(pygame.time.get_ticks()/1000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            button1.on_event(event, [button2.get_state()])
            button2.on_event(event)
            scrollbar1.on_event(event)
        DISPLAYSURF.fill(RGBColors.White)
        button1.draw()
        button2.draw()
        scrollbar1.draw()
        graph1.draw(data)
        pygame.display.update()
        clock.tick(30)

