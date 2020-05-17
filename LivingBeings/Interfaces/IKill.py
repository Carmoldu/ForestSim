from LivingBeings import LivingBeing


class IKill:
    def __init__(self, living_being: LivingBeing):
        self.living_being = living_being

    def kill(self):
        pass


class DoKill(IKill):
    pass


class DoNotKill(IKill):
    def kill(self):
        pass