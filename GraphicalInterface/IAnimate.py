import pygame
from GraphicalInterface.Grid import Grid

class IAnimate:
    main_folder = '.'
    draw_offset = (0, 0)
    default_source_images = {"base": None,
                             "kill": None,
                             "die": None,
                             "spawn": None}

    grid = None
    @classmethod
    def set_grid(cls, grid: Grid):
        cls.grid = grid

    @classmethod
    def set_main_folder(cls, folder: str):
        cls.main_folder

    def __init__(self,
                 position: (int, int),
                 base_img: str = default_source_images["base"],
                 kill_img: str = default_source_images["kill"],
                 die_img: str = default_source_images["die"],
                 spawn_img: str = default_source_images["spawn"]):

        if IAnimate.grid is None:
            raise Exception("Grid has not been set")
        if type(base_img) is not str:
            raise ValueError("base image should be a string with the path  to the base image")
        self.position = position

        self.surface_base = pygame.image.load(self.main_folder + base_img)
        base_rect = self.surface_base.get_rect()
        self.width = int(abs(base_rect.right - base_rect.left))
        self.height = int(abs(base_rect.bottom - base_rect.top))

        if kill_img is not None:
            self.surface_kill = pygame.image.load(self.main_folder + kill_img)

        if die_img is not None:
            self.surface_die = pygame.image.load(self.main_folder + die_img)

        if spawn_img is not None:
            self.surface_spawn = pygame.image.load(self.main_folder + spawn_img)

    def spawn(self):
        self.grid.static_elements.append(self)

    def move(self, cell_to_move: (int, int)):
        self.position = cell_to_move

    def kill(self):
        pass


class AnimationLumberjack(IAnimate):
    draw_offset = (-0.25, 0)
    default_source_images = {"base": "/LivingBeingGraphicSource/Lumberjack_base.png",
                             "kill": None,
                             "die": None,
                             "spawn": None}

    def __init__(self,
                 position: (int, int),
                 base_img: str = default_source_images["base"],
                 kill_img: str = default_source_images["kill"],
                 die_img: str = default_source_images["die"],
                 spawn_img: str = default_source_images["spawn"]):
        super().__init__(position, base_img, kill_img, die_img, spawn_img)

class AnimationBear(IAnimate):
    draw_offset = (0.25, 0)
    default_source_images = {"base": "/LivingBeingGraphicSource/Bear_base.png",
                             "kill": None,
                             "die": None,
                             "spawn": None}

    def __init__(self,
                 position: (int, int),
                 base_img: str = default_source_images["base"],
                 kill_img: str = default_source_images["kill"],
                 die_img: str = default_source_images["die"],
                 spawn_img: str = default_source_images["spawn"]):
        super().__init__(position, base_img, kill_img, die_img, spawn_img)

class AnimationTree(IAnimate):
    draw_offset = (0, 0)
    default_source_images = {"base": "/LivingBeingGraphicSource/Tree_base.png",
                             "kill": None,
                             "die": None,
                             "spawn": None}

    def __init__(self,
                 position: (int, int),
                 base_img: str = default_source_images["base"],
                 kill_img: str = default_source_images["kill"],
                 die_img: str = default_source_images["die"],
                 spawn_img: str = default_source_images["spawn"]):
        super().__init__(position, base_img, kill_img, die_img, spawn_img)
