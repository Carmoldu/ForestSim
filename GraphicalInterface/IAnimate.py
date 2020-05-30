import pygame


class IAnimate:
    draw_offset = (0, 0)
    default_source_images = {"base": None,
                             "kill": None,
                             "die": None,
                             "spawn": None}

    def __init__(self,
                 position: (int, int),
                 base_img: str = default_source_images["base"],
                 kill_img: str = default_source_images["kill"],
                 die_img: str = default_source_images["die"],
                 spawn_img: str = default_source_images["spawn"]):
        if type(base_img) is not str:
            raise ValueError("base image should be a string with the path  to the base image")
        self.position = position

        self.surface_base = pygame.image.load(base_img)
        base_rect = self.surface_base.get_rect()
        self.width = int(abs(base_rect.right - base_rect.left))
        self.height = int(abs(base_rect.bottom - base_rect.top))

        if kill_img is not None:
            self.surface_kill = pygame.image.load(kill_img)

        if die_img is not None:
            self.surface_die = pygame.image.load(die_img)

        if spawn_img is not None:
            self.surface_spawn = pygame.image.load(spawn_img)

    def spawn(self):
        pass

    def move(self):
        pass

    def kill(self):
        pass

    def move(self):
        pass
