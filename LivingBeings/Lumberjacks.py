from LivingBeings import LivingBeing


class Lumberjack(LivingBeing):
    default_monthly_energy = 3
    lumber = 0

    def __init__(self, position: tuple):
        super().__init__(position,
                         move_behaviour=IMove.CanMove(self),
                         reproduce_behaviour=IReproduce.NoReproduction(self),
                         kill_behaviour=IKill.DoKill(self),
                         display_behaviour=IDisplay.LumberjackDisplay(),
                         monthly_energy=self.default_monthly_energy)