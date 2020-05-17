from LivingBeings import LivingBeing


class IMove:
    def __init__(self, living_being: LivingBeing):
        self.living_being = living_being

    def move(self):
        pass


class CannotMove(IMove):
    pass


class CanMove(IMove):
    pass
