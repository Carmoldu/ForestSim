from LivingBeings import LivingBeing


class IReproduce:
    def __init__(self, living_being: LivingBeing):
        self.living_being = living_being

    def reproduce(self):
        pass


class NoReproduction(IReproduce):
    def reproduce(self):
        pass


class Asexually(IReproduce):
    def reproduce(self):
        pass