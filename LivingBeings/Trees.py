from LivingBeings import LivingBeing


class Tree(LivingBeing):
    default_monthly_energy = 0

    def __init__(self, position: tuple):
        super().__init__(position,
                         move_behaviour=IMove.CannotMove(self),
                         reproduce_behaviour=IReproduce.Asexually(self),
                         kill_behaviour=IKill.DoNotKill(self),
                         display_behaviour=IDisplay.TreeDisplay(),
                         monthly_energy=self.default_monthly_energy)