from LivingBeings import LivingBeing


class Bear(LivingBeing):
    default_monthly_energy = 5
    kills = 0

    def __init__(self, position: tuple):
        super().__init__(position,
                         move_behaviour=IMove.CanMove(self),
                         reproduce_behaviour=IReproduce.NoReproduction(self),
                         kill_behaviour=IKill.DoKill(self),
                         display_behaviour=IDisplay.BearDisplay(),
                         monthly_energy=self.default_monthly_energy)