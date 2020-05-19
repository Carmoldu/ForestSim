from LivingBeings import LivingBeing, Bear, Tree
from LivingBeings.PrintColors import PrintColors as textColor


class Lumberjack(LivingBeing.LivingBeing):
    default_monthly_energy = 3
    lumber = 0
    alive = []
    can_kill = {}

    def __init__(self, position: tuple):
        super().__init__(position, monthly_energy=self.default_monthly_energy)
        Lumberjack.alive.append(self)

        if not Lumberjack.can_kill:
            Lumberjack.can_kill = {Tree.Tree}

    def kill(self):
        if super().kill():
            Lumberjack.lumber += 1

    def display(self):
        return textColor.PURPLE + "L" + textColor.ENDC

    @classmethod
    def reset_lumber(cls):
        cls.lumber = 0

    @classmethod
    def hire_or_fire_lumberjacks(cls):
        if cls.lumber > len(cls.alive):
            lumberjacks_hired = cls.lumber // len(cls.alive)
            print(f"{lumberjacks_hired} have been hired!")
            cls.spawn_in_empty_space(lumberjacks_hired)

        else:
            if len(cls.alive) > 1:
                fired_lumberjack = cls.select_random_alive()
                print(f"Lumberjack at {fired_lumberjack.position} has been fired!")
                cls.died(fired_lumberjack)

        cls.lumber = 0



